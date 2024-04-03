# gpuart.net website python script to accept image gen reqs and post to mysql db

import os
from gradio.processing_utils import encode_pil_to_base64
from random import random, seed, gauss
from skimage.metrics import structural_similarity
from skimage.restoration import estimate_sigma, rolling_ball
import pymysql
import pymysql.cursors
from globals import *
from sdui import *
from time import sleep
import socket

####################################################################################################
####################################################################################################
####################################################################################################
#cd ~/git/stabl*; export CUDA_VISIBLE_DEVICES=0; ./webui.sh --port 7860 --api --no-half-vae
#cd ~/git/stabl*; export CUDA_VISIBLE_DEVICES=1; ./webui.sh --port 7861 --api --no-half-vae
#create 60fps HD video
#ffmpeg -pattern_type glob -framerate 60 -i '*.png' -vcodec mpeg4 -b:v 8000k $(echo $(($(date +%s%N)/1000000))).mp4

####
#Sometimes it needs to reload fresh checkpoint
#response = requests.post(url=f'{Globals.gpus[0]}/sdapi/v1/options', json={"sd_model_checkpoint": "uberRealisticPornMerge_urpmv13FULL.safetensors"})
#if not response.ok:
#  err(f"{response.reason}")

#test_video_by_img2img_score()

#https://pypi.org/project/pymysql/

class Globals:
   # if getting error ensure that /etc/hosts contains only a single entry for localhost.
  db_host = 'localhost'
  db_user = 'root'
  db_password = 'password'
  db_schema = 'STABLE_DIFFUSION_ONLINE'
  gpus = [
    "http://127.0.0.1:7860",
    "http://127.0.0.1:7861"
  ]
  root = "gpuart"
Globals.tempdir = os.path.join(Globals.root, "tmp")
Globals.outdir = os.path.join(Globals.root, "output")

class txn:
  def __init__(self):
    self.trans=None
    try:
      self.trans = pymysql.connect( host=Globals.db_host, user=Globals.db_user, password=Globals.db_password,
                                  database=Globals.db_schema, cursorclass=pymysql.cursors.DictCursor)
    except  Exception as e:
      err(f"DB: Failed connect h'{Globals.db_host}' u'{Globals.db_user}' p'{Globals.db_password}' s'{Globals.db_schema}' {printExcept(e)}")
      raise e    
  def commit(self): self.trans.commit()
  def rollback(self): self.trans.rollback()
  def close(self): 
    if self.trans.open:
      self.trans.close()
  def __enter__(self):
    pass
  def __exit__(self):
    self.close()

class datatable:
  #data is an array of associative arrays [{'colname': value,..},..]
  def rows(self):
    return self.data
  def row_count(self):
    if self.data!=None:
      return len(self.data)
    return 0
  def col_count(self):
    if self.data!=None and len(self.data)>0:
      return len(self.data[0])
    return 0
  def __str__(self) -> str:
    return f"{self.data}"
  def __init__(self, dat):
    self.data=dat

class db:
  @staticmethod
  def query(sql:str, parms:list=[], trans:txn=None, suppress_msgs=False) -> datatable : 
    res : datatable = None
    temptrans:txn = None

    if trans == None:
      temptrans = txn()
    else:
      temptrans = trans

    try:
      with temptrans.trans.cursor() as cursor:
        if not suppress_msgs:
          msg(f"Executing:\n {sql}")
          msg(f"len parms={len(parms)}")
          parm_str=''
          parm_delim=""
          for parm in parms:
            fparm = f"{parm}"
            if len(fparm) > 20:
              fparm = fparm[:20]+".."
            parm_str += parm_delim + fparm
            parm_delim=","
          msg(f"Params:\n {parm_str}")
        cursor.execute(sql, parms)
        if trans == None:
          temptrans.trans.commit()
        res = datatable(cursor.fetchall())
    except Exception as e1:
      err(f"Query Failed")
      try:
        temptrans.trans.rollback()
      finally:
        if temptrans.trans.open:
          temptrans.trans.close()
      raise e1

    return res
  
def get_sdui_payload(prompt, negative_prompt, width, height, seed=-1, subseed=-1, include_init_images=False,
                    init_images=[], sampler_name="Euler a", cfg_scale=7, steps=20, restore_faces=True, denoising_strength=0.6):
  payload = {
    "prompt": prompt,
    "negative_prompt": negative_prompt,
    "batch_size": 1,
    "cfg_scale": cfg_scale,
    "denoising_strength": denoising_strength,
    "enable_hr": False,
    "eta": 0,
    "firstphase_height": 0,
    "firstphase_width": 0,
    "height": height,
    "n_iter": 1,
    "restore_faces": restore_faces,
    "s_churn": 0,
    "s_noise": 1,
    "s_tmax": 0,
    "s_tmin": 0,
    "sampler_index": sampler_name,
    "seed": seed,
    "seed_resize_from_h": -1,
    "seed_resize_from_w": -1,
    "steps": steps,
    "styles": [],
    "subseed": subseed,
    "subseed_strength": 0,
    "tiling": False,
    "width": width,
    "include_init_images":include_init_images,
    "init_images": init_images  
  }  

  return payload

class ReqStatus:
  Queued = 1
  InProgress = 2
  Cancelled=3
  Failed=4

class ImgUsage:
  Output=1
  Mask_Input=2
  Inpaint_Input=3
  Img2Img_Input=4

def get_next_req():
  
    #do db thing to get next request
    res = db.query("SELECT "
                   "ID, "
                   "REQ_TYPE, "
                   "POS_PROMPT, "
                   "NEG_PROMPT, "
                   "SEED, "
                   "SUBSEED, "
                   "WIDTH, "
                   "HEIGHT, "
                   "SAMPLER_NAME, "
                   "CFG_SCALE, "
                   "STEPS, "
                   "RESTORE_FACES, "
                   "MASK_BLUR, "
                   "N_ITER, "
                   "INPAINTING_FILL, "
                   "INPAINT_FULL_RES, "
                   "DENOISE_STRENGTH,   "
                   "BATCH_COUNT, "
                   "OUTPUT_FORMAT, "
                   "CHECKPOINT, "
                   "USER_ID "
                   "FROM REQ "
                   "WHERE PROCESSED=0 ORDER BY CREATED DESC LIMIT 1", [],None, True)
    if res != None and res.row_count() == 1: 
      row = res.rows()[0]
      reqid = row['ID']
      try:
        do_request(row)
      except Exception as ex:
        printExcept(ex)
      finally:
        db.query("UPDATE REQ SET PROCESSED=%s WHERE ID=%s", [True, reqid]) 

def process_img(imgdata:Image, outdir:str, fmt:int=ImgFmt.Png, jpgquality:int=80, test=False):
  iimg = 0
  ext=""
  if fmt == ImgFmt.Png: 
    ext=".png"
  elif fmt == ImgFmt.Jpg: 
    ext=".jpg"
  else: 
    raise Exception(f"Invalid Image format {fmt}")
  
  from io import BytesIO
  with BytesIO() as f:
    imgdata.save(f, format='PNG' if fmt==ImgFmt.Png else 'JPEG', quality=jpgquality)
    #imgdata = imgdata.convert('RGB') for jpg which stores as YCbCr
    imgdata = Image.open(f)
    img_bytes = base64.b64encode(f.getvalue())

    if test == True:
      fpath = "./gpuart/___TEST{ext}"
    else:
      ms = milliseconds()
      fname = f"{ms}_{iimg}{ext}" 
      fpath = os.path.join(outdir, fname)
      while os.path.exists(fpath):
        iimg +=1
        fname = f"{ms}_{iimg}{ext}" 
        fpath = os.path.join(outdir, fname)

    if not os.path.exists(outdir):
      os.makedirs(outdir)
    fpath = os.path.abspath(fpath)
    imgdata.save(fpath)

  return (fpath, img_bytes)

def do_request(row):
  assert(row['OUTPUT_FORMAT']==ImgFmt.Png or row['OUTPUT_FORMAT']==ImgFmt.Jpg)

  reqid = row['ID']
  
  if row['REQ_TYPE'] != 1 and row['REQ_TYPE'] != 2:
    err(f"Invalid REQ_TYPE {row['REQ_TYPE']}")
  elif row['REQ_TYPE'] == 1:
    include_init_images = False;
    #, row['BATCH_COUNT'] - TODO
    payload = get_sdui_payload(row['POS_PROMPT'], row['NEG_PROMPT'],row['WIDTH'],row['HEIGHT'],row['SEED'],row['SUBSEED'],
                              include_init_images,[],row['SAMPLER_NAME'],row['CFG_SCALE'],row['STEPS'],row['RESTORE_FACES'],
                              row['DENOISE_STRENGTH'])
    #note all RPC are in api.py
    #all cmd args are in cmd_args.py
    #NOTE: you'll get a 404 if the payload is incorrect
    db.query("UPDATE REQ SET STATUS=%s WHERE ID=%s", [ReqStatus.InProgress, reqid]) 
    imgs = []
    startms = milliseconds()
    # TODO: /sdapi/v1/progress
    msg("dispatching..")
    dispatch_img(payload, imgs, "http://127.0.0.1:7861",row['REQ_TYPE'])
    gen_time_ms = milliseconds()-startms
    for i in range(0,len(imgs)):
      img = imgs[i]
      #fpath = saveimg(img, Globals.outdir, row['OUTPUT_FORMAT'], 50)
      #msg(f"fpath={fpath}")
      (fpath, img_bytes) = process_img(img, Globals.outdir, row['OUTPUT_FORMAT'], 70)
      imgsize_disk = os.path.getsize(fpath)
      imgsize_raw = img.tell() #len(img.getdata())
      img_name = os.path.basename(fpath)
      img_out_fmt = row['OUTPUT_FORMAT']
      img_req_fk = row['ID']
      img_userid_fk = row['USER_ID']

      #msg(f"")
      #with open(fpath, 'rb') as f:
      #  img_bytes= base64.b64encode(f.read())
    #  msg(f"output size = {os.path.getsize(fpath)} AND b64 = {len(img_bytes)}")

      try:
        trans = txn()
        db.query(   "INSERT INTO IMG ("
                    "IMG_WIDTH, " 
                    "IMG_HEIGHT, " 
                    "BATCH_INDEX, " 
                    "GEN_TIME_MS, " 
                    "IMG_SIZE_DISK,  " 
                    "IMG_SIZE_RAW, " 
                    "IMG_FORMAT, "
                    "IMG_NAME, " 
                    "IMG_USAGE, " 
                    "IS_COMPRESSED, "
                    "IMG_DATA, " 
                    "USER_ID, " 
                    "REQ_ID, " 
                    "RES_ID) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FROM_BASE64(%s), %s, %s, %s)", 
                    [ img.width, img.height, i,
                      gen_time_ms, imgsize_disk, imgsize_raw, img_out_fmt, 
                      img_name, ImgUsage.Output, 0, img_bytes, img_userid_fk, img_req_fk, None ],
                    trans)
        #LOAD_FILE only works on same server and has tons of permissions issues
        #from_base64 for mysql works but
        #its advised to store filepaths and just store the files in the OS
        #also store a hash of the file contents too
        #how to get them from PHP well...
        #perhaps move to /var/www/html/out_imgs
        #db.query("UPDATE IMG SET IMG_DATA =  WHERE ID = LAST_INSERT_ID()", [img_bytes], trans)
        trans.commit()
      finally:
        trans.close()

def is_server_up(host:str,port:int)->bool:
  #return true if server is running (works with sdui)
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  result = sock.connect_ex((host,port))
  return result == 0

def start_server():
  active_gpus = []
  while True:
    BProc.poll_all(active_gpus, True, True)
    if is_server_up("localhost", 7861)== False: #testing with 1 gpu
      if len(active_gpus) > 0: 
        #should have been removed and died if this happend
        raise "Gpu down but .. ?"
      else:
        msg("Gpu was down, starting GPU")
        #sudo rmmod nvidia_uvm
        # sudo modprobe nvidia_uvm
        #
        #export CUDA_VISIBLE_DEVICES=1 && ./webui.sh --port 7861 --api --no-half-vae

        args = "cd ~/git/stable-diffusion-webui && export CUDA_VISIBLE_DEVICES=1 && ./webui.sh --port 7861 --api --no-half-vae --lowvram --precision full --no-half"
      #  bp = BProc(args, True, True)
      #  active_gpus.append(bp)
    
    #todo make async
    if is_server_up("localhost", 7861)==True:
      get_next_req()
    sleep(2) #debug, so we can debug it 

      #args = [ 'export CUDA_VISIBLE_DEVICES=1', './webui.sh --port 7861' ]
    # args = '''
    #   export CUDA_VISIBLE_DEVICES=1
    #   ./webui.sh --port 786
    # '''
    #args = [ 'export' ,'CUDA_VISIBLE_DEVICES=1', './webui.sh', '--port' ,'7861' ]


start_server()

