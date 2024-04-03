#import argparse
#import os
#import sys
#from functools import partial
#import numpy as np
#import pytorch_lightning as pl
#import torch
#from pytorch_lightning.trainer import Trainer
#from torch.utils.data import random_split, DataLoader
#import dreambooth_helpers.dreambooth_trainer_configurations as db_cfg
#from dreambooth_helpers.arguments import parse_arguments
#from dreambooth_helpers.dataset_helpers import WrappedDataset, ConcatDataset
#from dreambo oth_helpers.joepenna_dreambooth_config import JoePennaDreamboothConfigSchemaV1
#from dreambooth_helpers.copy_and_name_checkpoints import copy_and_name_checkpoints
#from ldm.data.base import Txt2ImgIterableBaseDataset
#from ldm.util import instantiate_from_config, load_model_from_config

#https://github.com/microsoft/LoRA/blob/main/loralib/layers.py

import os
import math
import numpy as np
import matplotlib.pyplot as plt
import torch
from torch import nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor
from torchvision.utils import make_grid
from torchvision.io import read_image
from torchvision.transforms import Grayscale, CenterCrop, ToPILImage, GaussianBlur
from globals import *
import torch.optim as optim

######################################################################################
#region AiTest 

'''
color images that will have three channels – red, green, and blue
  Firstly, a larger number of out_channels allows the layer to potentially learn more useful features about the input data, though this is not a hard rule.
  Secondly, the size of your CNN is a function of the number of in_channels/out_channels in each layer of your network and the number of layers.
'''

class AiTest(nn.Conv2d):
  def __init__(self) -> None:
    super().__init__(3,3,4)
    self._device_id=1 #device num also CUDA_VISIBLE_DEVICES
    self._device=None
    self._model=None
  
    self.select_device()
    self.init_tutorial_nn()

  def select_device(self):
    msg(f"{logcol.magentab}torch version:{torch.__version__}{logcol.reset}")

    dbg(f"torch config:\n{torch.__config__.show()}")

    msg(f"Available gpus:")
    [msg(" " + str(torch.cuda.get_device_name(i))) for i in range(torch.cuda.device_count())]

    assert(self._device_id == -1 or self._device_id < torch.cuda.device_count())

    if torch.cuda.is_available():
      self._device = "cuda:"+str(self._device_id)
    elif torch.backends.mps.is_available():
      self._device = device("mps")
    else:
      self._device = device("cpu")
    
    msg(f"Using device: {self._device}")

    AiTest.dbg_print_gpu_info(self._device_id)

  def dbg_print_gpu_info(deviceid) -> None:
    props=torch.cuda.get_device_properties(deviceid)
    dbg(f"{props.name} {deviceid}")
    dbg(f"  VRAM: {fmt2d(props.total_memory/1073741824)}GB")
    dbg(f"  Version: {props.major}.{props.minor}")
    dbg(f"  Processor Count: {props.multi_processor_count}")
    dbg(f"  Integrated: {yesno(props.is_integrated)}")
    dbg(f"  MultiGPU: { yesno(props.is_multi_gpu_board) }")

  def init_tutorial_nn(self):
    self.flatten = nn.Flatten()
    self.linear_relu_stack = nn.Sequential(
      nn.Linear(28*28, 512),
      nn.ReLU(),
      nn.Linear(512, 512),
      nn.ReLU(),
      nn.Linear(512, 10),
    )
  def forward(self, x):
      x = self.flatten(x)
      logits = self.linear_relu_stack(x)
      return logits    
  def train(self, steps):
    model = self.to(self._device)
    nn.Embedding.train(model, True)
    print(model)

    #save ckpt
    #Model.state_dict << the state
    #torch.save(lora.lora_state_dict(model, bias='all'), checkpoint_path)

    #img = img.detach() # detach the tensor from the graph
    #img = ToPILImage()(img.to('cpu')) 

  #   # Send to GPU
  #   self._model = self.to(self._device)
  #   print(self._model)

  #   # Data
  #   X = torch.rand(1, 28, 28, device=self._device)
  #   logits = self._model(X)
  #   pred_probab = nn.Softmax(dim=1)(logits)
  #   y_pred = pred_probab.argmax(1)
  #   print(f"Predicted class: {y_pred}")

  # def forward(self, x):
  #     x = self.flatten(x)
  #     logits = self.linear_relu_stack(x)
  #     return logits


#relu = argmax(0,x)
# gradient is inexpensive with relu (which is just max() function)

# Define model
class NeuralNetwork(nn.Module):
  def __init__(self) -> None:
    super().__init__()
    self.flatten = nn.Flatten()
    self.linear_relu_stack = nn.Sequential(
      nn.Linear(28*28, 512),
      nn.ReLU(),
      nn.Linear(512, 512),
      nn.ReLU(),
      nn.Linear(512, 10)
    )
  def forward(self, x):
    x = self.flatten(x)
    logits = self.linear_relu_stack(x)
    return logits

#endregion
######################################################################################
#region Utils
torch.manual_seed(17)

#endregion
######################################################################################
#region AiTest embedder class

# # Data
# X = torch.rand(1, 28, 28, device=network._device)
# logits = model(X)
# pred_probab = nn.Softmax(dim=1)(logits)
# y_pred = pred_probab.argmax(1)
# print(f"Predicted class: {y_pred}")

# input_image = torch.rand(3,28,28)
# print(input_image.size())

# flatten = nn.Flatten()
# flat_image = flatten(input_image)
# print(flat_image.size())

# layer1 = nn.Linear(in_features=28*28, out_features=20)
# hidden1 = layer1(flat_image)
# print(hidden1.size())

# print(f"Before ReLU: {hidden1}\n\n")
# hidden1 = nn.ReLU()(hidden1)
# print(f"After ReLU: {hidden1}")

# seq_modules = nn.Sequential(
#     flatten,
#     layer1,
#     nn.ReLU(),
#     nn.Linear(20, 10)
# )
# input_image = torch.rand(3,28,28)
# logits = seq_modules(input_image)

# softmax = nn.Softmax(dim=1) # 1/ (1+e^-k)
# pred_probab = softmax(logits)

# print(f"Model structure: {model}\n\n")

# for name, param in model.named_parameters():
#   print(f"Layer: {name} | Size: {param.size()} | Values : {param[:2]} \n")

#endregion
######################################################################################
#region Batch image cropping Test

imgs = []
imgcount=0

def load_and_crop_imgs():
  transforms = torch.nn.Sequential(
    #Grayscale(),
    CenterCrop((512,512)),
    #RandomCrop((512,512)),
    GaussianBlur(kernel_size=9, sigma=(15.7,26)) #[, sigma]
    # transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
  )
  for dir_name, _, file_list in os.walk('/home/mario/Desktop/tamil'):
    for file in file_list:
      if file :
        imgpath=os.path.join(dir_name, file)
        msg(f"Reading image: {imgpath}") # Instead of print, you can do your stuff here. 
        img = read_image(imgpath)
        img = transforms(img)
        imgs.append(img)
        imgcount+=1

def show_imgs():
  msg(f"{len(imgs)} images")
  grid = make_grid(imgs, nrow=math.ceil(math.sqrt(len(imgs))))
  plt.imshow(grid.permute(1, 2, 0))
  plt.show()

#https://github.com/huggingface/safetensors
# from safetensors import safe_open
# from safetensors.torch import save_file
# save_file(tensors, "tamil.safetensors")
# tensors = {}
# with safe_open("model.safetensors", framework="pt", device="cpu") as f:
#   for key in f.keys():
#     tensors[key] = f.get_tensor(key)

load_and_crop_imgs()

test = AiTest()
test.train(100)

#nn.Linear
#nn.Conv2d
#Module.named_parameters

#Saving
# ** Loading a .pt file -> torch.load(checkpoint_file, map_location=map_location or shared.weight_load_location)
#   map location: "cuda:2"
# We only wnat to save the LoRA layer ()
#  my_state_dict = model.state_dict() < (layer name, tensor) < maps layers to ensors
   #     return {k: my_state_dict[k] for k in my_state_dict if 'lora_' in k}
#optimizer and model have different state dicts
#optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
#for var_name in optimizer.state_dict():
#  print(var_name, "\t", optimizer.state_dict()[var_name])

#plt.imshow(tensor_image)

#endregion






#plt.imshow(  tensor_image.permute(1, 2, 0)  )

#torchvision.
#transforms.CenterCrop(10)

#transform(img)

#show grid


