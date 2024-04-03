# functions for stable_diffusion_webui and interfacing
import os
import time
import sys
import traceback
import builtins
import inspect
import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin, JpegImagePlugin
from gradio.processing_utils import encode_pil_to_base64
import time
from random import random, seed, gauss
import math
import cv2
from skimage.metrics import structural_similarity
import matplotlib.pyplot as plt
import numpy
from typing import Union
from skimage.restoration import estimate_sigma, rolling_ball
from globals import *
import threading

class SDUIMode:
  Text2Img=1
  Img2Img=2

def inclusive_stepi(ii, iimax, smin, smax):
  if iimax <= 1:
    steps = smin
  else:
    steps = smin + int(float(ii) / float(iimax-1) * (smax - smin))
  return steps

def inclusive_stepf(ii, iimax, smin, smax):
  if iimax <= 1:
    steps = float(smin)
  else:
    steps = float(smin) + (float(ii) / float(iimax-1)) * float(smax - smin)
  return float(steps)

# class Img:
#   def __init__(self):
#     self.width=0
#     self.height=0
#     self.data=None
#     self.size=0

def dispatch_img(payload:any, imgs:list, url:str, mode=SDUIMode.Text2Img):
  if mode == SDUIMode.Text2Img:
    modestr="txt2img"
  elif mode == SDUIMode.Img2Img:
    modestr="img2img"
  else:
    raise "Mode string invalid"

  theurl=f'{url}/sdapi/v1/{modestr}'
  response = requests.post(url=theurl, json=payload)
  if response.ok: # .status_code==200
    r = response.json()
    for i in r['images']:
      
      # png_payload = {
      #  "image": "data:image/png;base64," + i
      # }
      # response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)
      # pnginfo = PngImagePlugin.PngInfo()
      # pnginfo.add_text("parameters", response2.json().get("info"))
      
      image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
      imgs.append(image)
  else:
    #NOTE: you'll get a 404 if the payload is incorrect
    err(f"HTTP request error url='{theurl}' code={response.status_code}:\n {response.reason}")


def gen_img_arr(initimg, pr1:str, npr1:str, noisemin:float, noisemax:float, nimgs_noise:int, stepmin:int, stepmax:int, 
                nimgs_step:int, cfgmin:int, cfgmax:int, nimgs_cfg:int, w:int, h:int, seed:int, subseed:int, mode:int, gpus:list, stepfn=None):
  #test gen array of images.
  imgs = []
  threads = []
  igpu = 0
  iimg = 0
  for iimg_noise in range(0,nimgs_noise):
    for iimg_step in range(0,nimgs_step):
      for iimg_cfg in range(0,nimgs_cfg):
        if stepfn == None:
          steps = inclusive_stepi(iimg_step, nimgs_step, stepmin, stepmax)
          cfg = inclusive_stepf(iimg_cfg, nimgs_cfg, cfgmin, cfgmax)
          noise = inclusive_stepf(iimg_noise, nimgs_noise, noisemin, noisemax)
        else:
          (steps, cfg) = stepfn(iimg_cfg, iimg_step, nimgs_cfg, nimgs_step, stepmin,stepmax, cfgmin,cfgmax)
        iimg+=1
        steps = int(steps)
        #cfg=int(cfg)
        #TODO: replace with get_sdui_paylod
        payload = {
          "prompt": pr1,
          "negative_prompt": npr1,
          "seed": seed,
          "subseed": subseed,
          "include_init_images": False if initimg==None else True,
          "init_images": [initimg] if initimg!=None else [],
          "width": w,
          "height": h,
          "sampler_name": 'DPM++ SDE Karras', #"Euler a",
          #"sampler_index": 'DPM++ SDE Karras', #"Euler a",
          "cfg_scale": cfg,
          "steps": steps,
          "restore_faces": False,
          "denoising_strength": noise,
          #"resize_mode": 0,

        }

        thread = threading.Thread(target=dispatch_img, args=(payload, imgs, gpus[igpu], mode))
        thread.start()
        threads.append(thread)
        igpu = (igpu + 1) % len(gpus)
  for th in threads:
    th.join()

  return imgs

def load_dict_arr(path):
  ret = []
  with open(path) as my_file:
    for line in my_file:
      ret.append(line.strip())
  #dbg(f"loaded '{path}'\n {ret}")
  return ret

def stitch_imgs_urls(files):
  assert(len(files)>0)
  dim = int(math.ceil(math.sqrt(float(len(files)))))
  assert(dim>0)

  def calc_or_paste(pasteimg=None):
    imgs = []
    maxx = 0
    maxy = 0
    for iy in range(0,dim):
      mw=0
      mh=0
      for ix in range(0,dim):
        filidx = iy*dim+ix
        if filidx < len(files):
          imgurl = files[filidx]
          img = Image.open(imgurl)
          imgs.append(img)

          if pasteimg:
            result.paste(im=img, box=(mw, maxy))

          (iw, ih) = imgs[len(imgs)-1].size
          mw += iw
          mh = max(ih, mh)

      maxx = max(maxx, mw)
      maxy += mh
    return (maxx, maxy)

  (maxx, maxy) = calc_or_paste( None)
  result = Image.new('RGB', (maxx, maxy))
  calc_or_paste(result)
  return result

def mutate_prompt(prompt,terms, min_terms, max_terms, rep_max):
  #replace, add , delete terms from prmopt random
  rep_min = 0
  deli = rrangei(rep_min, rep_max)
  addi = rrangei(rep_min, rep_max)

  if len(prompt) - deli <= min_terms:
    deli = len(prompt) - min_terms

  if len(prompt) + addi - deli >= max_terms:
    addi = max_terms - (len(prompt) - deli)

  if addi == 0 and deli == 0:
    if len(prompt) < max_terms:
      addi = 1
    elif len(prompt) > min_terms:
      deli = 1

  for ti in range(0, deli):
    pidx = rrangei(0, len(prompt)-1)
    del prompt[pidx]

  for ti in range(0, addi):
    term_idx = rrangei(0, len(terms)-1)
    prompt.append(terms[term_idx])

  return prompt

def mutate_prompts(ph, nh,  terms):
  parr = [x.strip() for x in ph.split(',')]
  narr = [x.strip() for x in nh.split(',')]

  parr = mutate_prompt(parr, terms, 1, 30, 3)
  narr = mutate_prompt(narr, terms, 0, 10, 1)

  ph = ','.join(parr)
  nh = ','.join(narr)

  return (ph, nh)

def mutate_size(area, minw, maxw):
  #gen an image max 512 512 area
  rw = int(round(minw + (maxw - minw) * (gauss(0, 0.4)+1)/2))
  rh = int(round(area / rw))
  return (rw, rh)

def linearfn(x, y, maxx, maxy, smin, smax, cmin, cmax):
  #make it linear not combinatorial
  inc = float(maxx*y+x) / float(maxx*maxy-1)
  sx = smin+float(smax-smin)*inc
  cx = cmin+float(cmax-cmin)*inc
  return (sx, cx)

def compute_variance(img):
  nextgray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  lap = cv2.Laplacian(nextgray, cv2.CV_64F, ksize=3)
  v = cv2.mean(cv2.convertScaleAbs(lap))[0]
  return v

def compute_v_and_ss_and_e(before, after):
  ss=0
  # SS
  if type(before) != type(None):
    before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
    after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)
    (ss, diff) = structural_similarity(before_gray, after_gray, full=True)

  #V
  v = compute_variance(after)

  #E
  e= 0 #estimate_sigma(nextgray, average_sigmas=True)

  #background intensity
  #xx = after.std()
  # Y = cv2.cvtColor(after, cv2.COLOR_BGR2YUV)[:,:,0]
  # minx = numpy.min(Y)
  # maxx = numpy.max(Y)
  # contrast = (maxx-minx)/(maxx+minx)

  return (ss, v, e)

def get_files_bydate(dir):
  files = []
  for f in os.listdir(dir):
    fp = os.path.join(dir, f)
    if os.path.isfile(fp):
      _,ext = os.path.splitext(fp)
      ext = ext.lower().strip()
      if ext == '.png' or ext == '.jpg':
        files.append(fp)
  files.sort(key=lambda x: os.stat(x).st_mtime)
  return files

def show_image(img:Union[PngImagePlugin.PngImageFile,JpegImagePlugin.JpegImageFile,numpy.array]):
  #cant get this to work without blocing
  #if not plt.isinteractive():
  #  plt.ion()
  #plt.ioff

  cvimg = None
  if type(img) is PngImagePlugin.PngImageFile or type(img) is JpegImagePlugin.JpegImageFile:
    cvimg = numpy.array(img)
  else: # assume numpy.array
    cvimg = img

  plt.imshow(cvimg)
  plt.show()

def inpaint_zoom(img, p, np, zs, seed):
  #test inpainting the border as it's causing issues
  mw = img.size[0]
  mh = img.size[1]
  if zs == 0:
    return img
  elif zs < 0:
    zs = -zs
    img = img.resize((mw + zs*2, mh + zs*2)) #Image.ANTIALIAS , Image.LANCZOS
    img = img.crop((zs, zs, img.size[0] - zs, img.size[1] - zs))

  else:
    img2 = img.copy()
    img2 = img2.resize((mw - zs*2, mh - zs*2)) #, Image.ANTIALIAS
    img.paste(img2, (zs, zs))
    #show_image(img2)

    maskimg = Image.new(mode='RGB', size = (mw, mh), color =(255, 255, 255))
    mask_skip = Image.new(mode='RGB', size = (mw - zs*2, mh - zs*2), color =(0, 0, 0))
    maskimg.paste(mask_skip, (zs,zs))
    #show_image(maskimg)

    img = inpaint_image(img, maskimg, p, np, seed)
  #show_image(img)
  return img

def inpaint_pan(img, p, np, dx, dy, url, seed):
  #url = gpu eg 127.../txt2img
  mw = img.size[0]
  mh = img.size[1]
  img2 = img.copy()
  img.paste(img2, (dx, dy))
  #show_image(img2)

  maskimg = Image.new(mode='RGB', size = (mw, mh), color =(255, 255, 255))
  mask_skip = Image.new(mode='RGB', size = (mw , mh), color =(0, 0, 0))
  maskimg.paste(mask_skip, (dx,dy))
  #show_image(maskimg)

  img = inpaint_image(img, maskimg, p, np, url, seed)
  show_image(img)
  return img

def inpaint_image(dimg, dmask, p, np, url, seed):
  #url = Globals.gpus[0]

  base64img = encode_pil_to_base64(dimg)
  maskimg64 = encode_pil_to_base64(dmask)

  payload = {
    "width": dimg.size[0],
    "height": dimg.size[1],
    "prompt": p,
    "negative_prompt": np,
    "steps": 20,
    "sampler_name": 'DPM++ SDE Karras', #sampler_index..?
    "mask": maskimg64,
    "mask_blur": 20,
    "n_iter": 1,
    "inpainting_fill": 2, # 'fill', 'original', 'latent noise', 'latent nothing'
    "denoising_strength": 1,
    "cfg_scale": 7,
    "init_images": [base64img],
    "seed": -1,
    "subseed": -1,
    "restore_faces": False,
    "inpaint_full_res": True,
    #"inpainting_mask_invert": True,
  }
  #fname = f"{milliseconds()}.png"
  response = requests.post(url=f'{url}/sdapi/v1/img2img', json=payload)
  if not response.ok:
    err(response.text)
  r = response.json()
  i = r['images'][0]
  image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
  return image

def move_camera_random(img, p, np, seed):
  rr = random()
  if rr < 0.25:
    zs = 1+int(round(random()*6))
    if rr < 0.125:
      zs=-zs
    img = inpaint_zoom(img, p, np, zs, seed)

  panx=0
  pany=0
  rr = random()
  if rr < 0.5:
    panx=1+int(round(random()*4))
    if rr >= 0.25:
      panx = -panx

  rr = random()
  if rr < 0.5:
    pany=1+int(round(random()*4))
    if rr >= 0.25:
      pany=-pany

  if panx!=0 or pany!=0:
    img = inpaint_zoom(img, p, np, 2, seed)

  #rotate
  #img2 = nextimg.rotate(-1, Image.NEAREST, expand = 0)
  #nextimg.paste(img2, (0, 0))

class ImgFmt:
  Png=1
  Jpg=2


def saveimg(imgdata:Image, outdir:str, fmt:int=ImgFmt.Png, jpgquality:int=80, test=False):
  iimg = 0
  ext=""
  if fmt == ImgFmt.Png: 
    ext=".png"
  elif fmt == ImgFmt.Jpg: 
    ext=".jpg"
    imgdata = imgdata.convert('RGB')
  else: 
    raise Exception(f"Invalid Image format {fmt}")

  if test == True:
    fpath = "./gpuart/___TEST{ext}"
  else:
    ms = milliseconds()
    fname = f"{ms}_{iimg}{ext}" 
    fpath = os.path.join(outdir, fname)
    while os.path.exists(fpath):
      iimg+=1
      fname = f"{ms}_{iimg}{ext}" 
      fpath = os.path.join(outdir, fname)

  if not os.path.exists(outdir):
    os.makedirs(outdir)
  fpath = os.path.abspath(fpath)
  imgdata.save(fpath, quality=jpgquality)
  return fpath

def test_video_by_img2img_score(tempdir:str):
  #test video by doing img2img overf and over
  #use a score to dtermine spatial coherence

  class vc_state:
    iimg=0
    imgs_avg = []
    imgs_avg_max = 10
    salt1 = ""
    salt2 = ""
    pidx = 0 #int(int(round(random()*len(pm))) % len(pm))
    iprompt_change = 0
    vc_d2s = []
    max_imgs = 60 * 60 * 10
    seed =  int(milliseconds()/10000)
    subseed = -1 #114092904
    sampler = 'DPM++ SDE Karras' # 'Euler a' #see samplers_k_diffusion
    noise_mid = 0.3
    noise_min = 0.25
    noise_max = 1.0
    cfg = 7.0
    last_v = 0
    base_v = 0
    last_s = 0
    step = 20
    step_min = 20
    step_max = 80
    salt1_steps = 30 #60*1 #frames
    salt2_steps = 60 #60*3 #in frames
    isalt2_step = salt2_steps
    isalt1_step = salt1_steps
    prompt_steps = 60*4 #4sec
    vc_low_low = 10.0
    vc_low_high = 20.0
    vc_high_low = 40.0
    vc_high_high = 60.0
    vc_noise_delta_steps = 30.0 # worst case - achieve median entropy in X frames
    vc_d2_count = 5 # average image variance over N images
    vc_delta_min = 0.01
    zoompx_accum_max = 50 #max zoom/frame only when rectifying image
    zoompx_delta_min = 0.0
    zoompx_delta_max = 0.5
    score_max = 0.98
    score_min = 0.93
    bp = "extreme realism, real picture "
    bnp = "blurry, cartoon, fake, cgi, abstract, anime, monochrome"
    pm = [
      ""
    ]
    npm = [
      "",
    ]

  state = vc_state()
 # dict_arr = load_dict_arr('gpuart/dict.txt')
  dict2_arr = load_dict_arr('gpuart/dict_nouns.txt')

  #nextimg_url = ""
  last_img=None
  last_img_cv=None
  cur_img = None
  d_noise = state.noise_mid
  d_step = state.step
  last_v =0
  noise_frames_max = 30
  inoise_frames = noise_frames_max
  avg_noise = 0
  avg_noise_samples_max = 20
  avg_noise_samples = []
  assert(len(state.pm) == len(state.npm))
  while state.iimg < state.max_imgs:
    state.iimg+=1
    #salt
    state.isalt1_step+=1
    if state.isalt1_step >= state.salt1_steps:
      rrword = rrangei(0,len(dict2_arr)-1)
      state.salt1 = dict2_arr[rrword]
      state.isalt1_step=0
    state.isalt2_step+=1
    if state.isalt2_step >= state.salt2_steps:
      rrword = rrangei(0,len(dict2_arr)-1)
      state.salt2 = dict2_arr[rrword]
      state.isalt2_step=0

    p = state.bp + "," + state.salt1 + "," + state.salt2
    np = state.bnp

    #camera movement
    #move_camera_random(nextimg, p, np, seed)

    #image
    if cur_img == None:
      files = get_files_bydate(tempdir)
      if len(files) == 0:
        imgs = gen_img_arr(None, p, np, 1.0, 1.0, 1, state.step, state.step, 1, state.cfg, state.cfg, 1, 600, 400, state.seed, state.subseed, SDUIMode.Text2Img)
        assert(len(imgs)==1)
        fpath = saveimg(imgs[0], tempdir)
        files = get_files_bydate(tempdir)
      cur_img = Image.open(files[len(files)-1])
      last_img = cur_img
      curimg_cv = pil_to_cv(cur_img)
      dbg_s_, start_v, dbg_e_ = compute_v_and_ss_and_e(None, curimg_cv)

      if start_v < 20:
        start_v = 20
      if start_v > 50:
        start_v = 50
      state.last_v = start_v
      state.base_v = start_v

    lastimg_cv = curimg_cv
    curimg_cv = pil_to_cv(cur_img)
    
    #This seems to work. we could also create a drag of some kidn with N previous images weighted 
    ####test this out - weighted transfer of images
    #beta = 0.05
    beta = 0.1 # 1.0 / state.imgs_avg #0.5 #0.05
    #for iimgav in state.imgs_avg:
    curimg_cv = cv2.addWeighted(curimg_cv, 1.0-beta, lastimg_cv, beta, 0.0)
    #curimg_cv = cv2.addWeighted(curimg_cv, beta, lastimg_cv, 1.0-beta, 0.0)
    cur_img = Image.fromarray(cv2.cvtColor(curimg_cv, cv2.COLOR_BGR2RGB))
    saveimg(cur_img, "./gpuart/", True)
    #####

    curimg_base64 = encode_pil_to_base64(cur_img)

    #noise avg
    avg_noise_samples.append(d_noise)
    if len(avg_noise_samples) > avg_noise_samples_max:
      del avg_noise_samples[0]
    avg_noise=0
    for s in avg_noise_samples:
      avg_noise+=s
    avg_noise /= float(len(avg_noise_samples))

    #noise median
    nmod = -(avg_noise - state.noise_mid) / float(len(avg_noise_samples))
   # d_noise = min(state.noise_max, max(state.noise_min, d_noise + nmod  ))

    state.seed += 1
    passidx = 0

    d_step = state.step_min + (state.step_max - state.step_min) * random()

    imgs = gen_img_arr(curimg_base64, p, np, d_noise, d_noise+0.05, 2, int(round(d_step)), int(round(d_step)), 1, state.cfg, state.cfg, 1, cur_img.size[0], cur_img.size[1], -1, -1, SDUIMode.Img2Img)

    mvstr=""
    final_img = None
    minval = 9999.0
    iimgid=0
    selid=0
    value=0
    for imgt in imgs:
      imgt_cv = pil_to_cv(imgt)
      v = compute_variance(imgt_cv)
      value = (state.base_v - v)/state.base_v
      mvstr += f" {fmt3d(value)}"
      if abs(value) < minval:
        final_img = imgt
        minval = abs(value)
        selid=iimgid
      iimgid+=1

    dbg(f"  {mvstr}")
    msg(f"{state.iimg}:{passidx} | minval={fmt3d(minval)} selid={selid} | ns={fmt3d(d_noise)} nsa={fmt3d(avg_noise)} nm={fmt3d(nmod)} st={fmt3d(d_step)} | s1={state.salt1} s2={state.salt2}")

   # d_noise = min(state.noise_max, max(state.noise_min, d_noise + value/20.0  ))

    passidx += 1

    #save
    saveimg(final_img, tempdir)
    last_img = cur_img
    cur_img = final_img

def pil_to_cv(pil):
  return cv2.cvtColor(numpy.array(pil), cv2.COLOR_RGB2BGR)

def score_image(last_img, next_img, state, base_variance):

  #multiplier = (base_variance - 20.0) / 50.0 * .8

  #return a score of +/- 1.0 based on the variance
  _, cur_v, _ = compute_v_and_ss_and_e(None, next_img)
  #score_s = -clamp01( max(state.score_min - cur_s, 0) / state.score_min )

  #cur_s = 0.0
  #base_variance = 30.0
  # if cur_v < base_variance:
  #   score_v = +clamp01(max(base_variance - cur_v, 0) / base_variance) #from 0 -> 150 typically 5-60
  # else:
  #   score_v = +clamp01(1-max((base_variance+30.0) - cur_v, 1) / ((base_variance+30.0)-base_variance))

  score_v = (base_variance - cur_v) / base_variance

  # if cur_e < 1.0:
  #   score_e = +clamp01(max(1.0 - cur_e, 0) / 1.0) # about 2-7 7 being extreme
  # else:
  #   score_e = +clamp01(1-max(5.0 - cur_e, 1) / (5.0-1.0))

  # score_e = 0# +clamp01(max(cur_e-2, 0)/5.0)

  # score_sv = score_v #score_s + score_v
  # final_score = score_v #(score_sv + score_e) * 0.5

 # dbg(f" v={fmt3d(cur_v)} sv={fmt3d(score_v)} ")

  return score_v

def adjust_contrast(image):
  alpha = 1.2 # Contrast control (1.0-3.0)
  beta = 0 # Brightness control (0-100)
  image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
  return image

def sp_noise(image,prob):
    '''
    Add salt and pepper noise to image
    prob: Probability of the noise
    '''
    output = numpy.zeros(image.shape,numpy.uint8)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output
