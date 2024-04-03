#Open an external console that accepts commands
# 1.
#
# e=ExtCon()
# e.exec("echo 'hi'")
#
# 2.
#
# e=ExtCon(True)
# e.exec("echo 'hi'")
# print(e.stdout())
# print(e.stderr())

import sys
import select
import subprocess
from threading import Thread
from queue import Queue, Empty  # Python 3.x

from globals import *

class ExtCon:
  def __enter__(self):
    return self
  def __exit__(self, exc_type, exc_val, exc_tb):
    pass
  def __init__(self, queue = False):
    #queue = False: print output to console
    #queue = True: queue output for get_stdout(). do not print

    self.queue_output = queue
    self._process = subprocess.Popen(["bash"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, universal_newlines=True)
    self._donestr = f"&{self._process.pid}"
    self._waiting = 0
    def enqueue_output(_queue, _proc):
      for line in iter(_proc.readline, b''):
        if line.strip() == f"{self._donestr}":
          self._waiting -= 1
        elif queue == False:
          print(line)
        else:
          _queue.put(line)
      _queue.close()

    self._out_queue = Queue()
    self._err_queue = Queue()

    self._stdout_async = Thread(target = enqueue_output, args=(self._out_queue, self._process.stdout))
    self._stderr_async = Thread(target = enqueue_output, args=(self._err_queue, self._process.stderr))

    self._stdout_async.daemon = True
    self._stderr_async.daemon = True

    self._stdout_async.start()
    self._stderr_async.start()

  def exec(self, command : str) -> None:
    if not command.endswith("\n"):
      command += "\n"
    command += f"echo '{self._donestr}'"+"\n"
    self._waiting+=1
    self._process.stdin.write(command)
    self._process.stdin.flush()

  def get_stdout(self) -> str:
    outStr = ''
    try:
      while True:
        outStr += self._out_queue.get_nowait()
    except Empty:
      return outStr

  def get_stderr(self) -> str:
    outStr = ''
    try:
      while True:
        outStr += self._err_queue.get_nowait()
    except Empty:
      return outStr

  def wait(self, timeout_seconds : float = -1, poll_seconds : float = 0.01):
    start = time.time()
    while self._waiting:
      if self._waiting == 0:
        break
      if timeout_seconds >= 0 and (time.time() - start) > timeout_seconds:
        print(f"wait() timed out after {timeout_seconds}")
        break
      time.sleep(poll_seconds)

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
    return self._waiting != 0
    
def test1():
  print("Test 1")
  ec = ExtCon()
  ec.exec("echo 'sleeping for 1'; sleep 1; echo 'done';")
  ec.print()

def test2():
  print("Test 2")
  ec = ExtCon(True)
  ec.exec("echo 'sleeping for 1'; sleep 1; echo 'done';")
  ec.print()

def run_tests():
  test1()
  test2()
  sys.stdin.read(1)