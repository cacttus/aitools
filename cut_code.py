

#      # payload = {
      #   "width": nextimg.size[0],
      #   "height": nextimg.size[1],
      #   "prompt": p,
      #   "negative_prompt": np,
      #   "steps": state.step,
      #   "sampler_index": state.sampler,
      #   "denoising_strength": d_noise,
      #   "cfg_scale": state.cfg,
      #   "init_images": [base64img],
      #   "seed": state.seed,
      #   "subseed": state.subseed,
      #   "restore_faces": False,
      # }
      # fname = f"{milliseconds()}.png"
      # urls=[]
      # dispatch_img(payload, fname, urls, Globals.gpus[0], Globals.tempdir, Mode.Img2Img)
      # nextimg_url = urls[0]

    #img mod

      #Testing increasing variance
    #   if last_v>0.2 and inoise_frames == 0:
    #     img = cv2.imread(nextimg_url)
    #     #img = sp_noise(img, 0.001 * (1-last_v))
        
    #     #img = adjust_contrast(img)
        
    #     #sharpen
    #     kernel = numpy.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    #     img_sharp = cv2.filter2D(img, -1, kernel)
    #     beta = 0.03 * (last_v - 0.2)/0.8 + 0.01
    #     img_res = cv2.addWeighted(img, 1.0-beta, img_sharp, beta, 0.0)

    #     #we still need to control the histogram blowing out

    #     noisyimg_url =os.path.join(Globals.tempdir, "__temp.png")
    #     assert(cv2.imwrite(noisyimg_url, img_res))
    #     nextimg = Image.open(noisyimg_url)

    #     inoise_frames = noise_frames_max

    #   inoise_frames = max(0, inoise_frames-1)

    #try:

    # except Exception as ex:
    #   dbg(f"exception: {ex}")
    #   lastimg = Image.open(nextimg_url)
    #   base64img = encode_pil_to_base64(lastimg)

      
    #increase variance by resizeing image 
    # if last_v > 0.2:
    #   payload = {
    #     "prompt": "",
    #     "negative_prompt": "",
    #     "seed": -1,
    #     "subseed": -1,
    #     #"include_init_images": True,
    #     "init_images": [base64img],
    #     "width": nextimg.size[0]*1.5,
    #     "height": nextimg.size[1]*1.5,
    #     "sampler_name": 'DPM++ SDE Karras', #"Euler a",
    #     "cfg_scale": 7,
    #     "steps": 80,
    #     "restore_faces": False,
    #     "denoising_strength": 0.6,
    #     "resize_mode": 3, #"Just resize (latent upscale)",  #"Just resize", "Crop and resize", "Resize and fill", "Just resize (latent upscale)"
    #     "seed_resize_from_h": -1,
    #     "seed_resize_from_w": -1,        
    #     #"script_name": "sd upscale",
    #     #"script_args": ["", 8, "Lanczos", 2.0]
    #   }
    #   urls = []
    #   dispatch_img(payload, "__temp.png", urls, Globals.gpus[0], Globals.tempdir, Mode.Img2Img)
    #   noised = Image.open(urls[0])
    #   noised = noised.resize((nextimg.size[0], nextimg.size[1])) #Image.ANTIALIAS , Image.LANCZOS
    #   noisyimg_url  = os.path.join(Globals.tempdir, "__temp2.png")
    #   noised.save(noisyimg_url)
    #   base64img = encode_pil_to_base64(noised)


    # with trans:
    #   with trans.cursor() as cursor:
    #     sql = "SELECT * FROM REQ WHERE `ID`=%s"
    #     cursor.execute(sql, 1)
    #     result = cursor.fetchone()
    #     print(result)
    #result = cursor.fetchone()
    #print(result)