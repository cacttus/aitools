import os
import time
import sys
import traceback
import builtins
import inspect
from random import random, seed, gauss
import subprocess
from threading import Thread
from queue import Queue, Empty  # Python 3.x

@staticmethod
def fmt2d(arg): return '{0:.2f}'.format(arg)
@staticmethod
def yesno(arg): return 'yes' if arg == 0 else 'no'
@staticmethod
def _log_fn():
  return os.path.basename(inspect.getframeinfo(inspect.currentframe().f_back.f_back).filename)
@staticmethod
def _log_ln():
  return inspect.getframeinfo(inspect.currentframe().f_back.f_back).lineno
@staticmethod
def msg(args): _msg(f"{logcol.yellow}{_log_fn()}{logcol.reset}:{logcol.green}{_log_ln()} {logcol.reset}{str(args)}{logcol.reset}")
@staticmethod
def dbg(args): _msg(f"{logcol.yellow}{_log_fn()}{logcol.reset}:{logcol.green}{_log_ln()} {logcol.cyan }{str(args)}{logcol.reset}")
@staticmethod
def err(args): _msg(f"{logcol.yellow}{_log_fn()}{logcol.reset}:{logcol.green}{_log_ln()} {logcol.redb }{str(args)}{logcol.reset}")
@staticmethod
def pr(var):  
  dbg(f"{logcol.greenb}{inspect.getframeinfo(inspect.currentframe().f_back).code_context[0].strip()}:{logcol.cyanb}{var}{logcol.reset}")
@staticmethod
def _msg(args):
  builtins.print(args)
  sys.stdout.flush()
  time.sleep(0)
@staticmethod
def printExcept(e):
  extype = type(e)
  tb = e.__traceback__
  traceback.print_exception(extype, e, tb)
  return  
@staticmethod
def throw(ex):
  raise Exception(logcol.redb + "" + ex + logcol.reset)
@staticmethod
def trap():
  pdb.pm()
class logcol:
  _bold = "\033[1;24;27;"
  _normal = "\033[0;24;27;"
  black = _normal+"30m"
  red = _normal+"31m"
  green = _normal+"32m"
  yellow = _normal+"33m"
  blue = _normal+"34m"
  magenta = _normal+"35m"
  cyan = _normal+"36m"
  white = _normal+"37m"
  blackb = _bold+"30m"
  redb = _bold+"31m"
  greenb = _bold+"32m"
  yellowb = _bold+"33m"
  blueb = _bold+"34m"
  magentab = _bold+"35m"
  cyanb = _bold+"36m"
  whiteb = _bold+"37m"
  reset = "\033[0m"
  # fmt: on
  # autopep8: on

@staticmethod
def fmt2d(number):
  return '{:.2f}'.format(number)
@staticmethod
def fmt3d(number):
  return '{:.3f}'.format(number)
@staticmethod
def milliseconds():
  return int(round(time.time()*1000))
@staticmethod
def rrangei(min,max):
  assert(min <= max)
  return int(min + round(float(max-min)*random()))
@staticmethod
def clamp01(x):
  return min(1,max(0,x))
@staticmethod
def printExcept(e):
  extype = type(e)
  tb = e.__traceback__
  traceback.print_exception(extype, e, tb)
  return
  msg(str(e))
  exc_tb = sys.exc_info()  # in python 3 - __traceback__
  print(str(exc_tb))
  fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
  print("fname=" + fname)
  msg(fname + " line " + str(exc_tb.tb_lineno))
  msg(traceback.format_exc())
  sys.exc_clear()
@staticmethod
def get_image_size(fname):
  with open(fname, 'rb') as fhandle:
    head = fhandle.read(24)
    if len(head) != 24:
      return
    if imghdr.what(fname) == 'png':
      check = struct.unpack('>i', head[4:8])[0]
      if check != 0x0d0a1a0a:
        return
      width, height = struct.unpack('>ii', head[16:24])
    elif imghdr.what(fname) == 'gif':
      width, height = struct.unpack('<HH', head[6:10])
    elif imghdr.what(fname) == 'jpeg':
      try:
        fhandle.seek(0)  # Read 0xff next
        size = 2
        ftype = 0
        while not 0xc0 <= ftype <= 0xcf:
          fhandle.seek(size, 1)
          byte = fhandle.read(1)
          while ord(byte) == 0xff:
            byte = fhandle.read(1)
          ftype = ord(byte)
          size = struct.unpack('>H', fhandle.read(2))[0] - 2
        # We are at a SOFn block
        fhandle.seek(1, 1)  # Skip `precision' byte.
        height, width = struct.unpack('>HH', fhandle.read(4))
      except Exception:  # IGNORE:W0703
        return
    else:
      throw("invalid image type for '"+fname+"'")
    return width, height


'''
** BProc
** async process class for Python read input and output async
** EXAMPLE:
      bprocs=[]
      def asyncExportBlend(fpath):
        if fpath != self._libFile:
          dbg(f"Exporting: '{fpath}'")
          cmd = BProc.getargs(fpath)
          dbg(f"Cmd={cmd}")
          bpr = BProc(cmd)
          bprocs.append(bpr)
          
      Utils.loopFilesByExt(args.inpath, '.blend', asyncExportBlend)
    
      finished = False
      while not finished:
        finished = True
        for bp in bprocs:
          if bp.waiting():
            if self._verbose:
              so = bp.get_stdout()
              if so:
                _msg(so)
            se = bp.get_stderr()
            if se:
              _msg(se)
            finished = False
            time.sleep(0.1)
            break
'''
class BProc:
  def __init__(self, cmd, queue = True, use_shell=False):
    #queue = False: print output to console
    #queue = True: queue output for get_stdout(). do not print
    # if use_shell is True then the cmd must be a single string and it's also unsafe without shell then cmd must be an array of args

    self.queue_output = queue
    self._process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=use_shell)
    def enqueue_output(_queue, _proc):
      for line in iter(_proc.readline, b''):
        if queue == False:
          print(line)
        else:
          _queue.put(line)
      #_queue.close()

    self._out_queue = Queue()
    self._err_queue = Queue()

    self._stdout_async = Thread(target = enqueue_output, args=(self._out_queue, self._process.stdout))
    self._stderr_async = Thread(target = enqueue_output, args=(self._err_queue, self._process.stderr))

    self._stdout_async.daemon = True
    self._stderr_async.daemon = True

    self._stdout_async.start()
    self._stderr_async.start()

  @staticmethod
  def wait_all(procs:list, verbose:bool, remove_completed:bool):
    #wait for all BProcs in an array
    finished = False
    while not finished:
      finished = BProc.poll_all(procs,verbose, remove_completed)
      time.sleep(0.1)
      break

  @staticmethod
  def poll_all(procs:list, verbose:bool, remove_completed:bool) -> bool:
    #poll for all BProcs in an array and log their output to stdout
    finished = True
    for i in range(len(procs)-1,-1,-1):
      bp = procs[i]
      if bp.waiting():
        if verbose:
          so = bp.get_stdout()
          if so:
            msg(so)
        se = bp.get_stderr()
        if se:
          msg(se)
        finished = False
      elif remove_completed:
        procs.pop(i)
    return finished
        
  @staticmethod
  def get_app_args(fpath):
    #parse a command line into arguments for bproc
    as_str=False
    cmd=f"{sys.argv[0]}"
    if not as_str:
      cmd = [sys.argv[0]]
    userarg = False
    for i in range(1, len(sys.argv)):
      lastarg = sys.argv[i - 1]
      arg = sys.argv[i]
      if lastarg == "--":
        userarg = True
      elif userarg == True and lastarg == Bake26.c_argInput:
        if as_str:
          cmd += " " + lastarg + " " + fpath
        else:
          cmd.append(f"{lastarg}")
          cmd.append(f"{fpath}")
      elif userarg == True and (arg == Bake26.c_argPack or arg == Bake26.c_argPackOnly):
        pass
      else:
        if as_str:
          cmd += " " + sys.argv[i]
        else:
          cmd.append(f"{sys.argv[i]}")
    return cmd

  def get_stdout(self) -> str:
    outStr = ''
    try:
      while True:
        outStr += self._out_queue.get_nowait().decode('utf-8')
    except Empty:
      return outStr

  def get_stderr(self) -> str:
    outStr = ''
    try:
      while True:
        outStr += self._err_queue.get_nowait().decode('utf-8')
    except Empty:
      return outStr

  def print(self, wait : bool = True) -> None:
    if wait:
      self.wait()
    so = self.get_stdout()
    se = self.get_stderr()        
    if so!="": print(so) 
    if se!="": print(se) 

  def kill(self):
    self._process.kill()

  def waiting(self) -> bool:
    return self._process.poll() == None
