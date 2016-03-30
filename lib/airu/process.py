import os
from subprocess import Popen, PIPE
import sys

class Process():
  def __init__(self, cmd):
    """
    Sets up a process to execute a command. The command to execute must be an
    array containing all arguments for the command.

    cmd -- command and arguments as an array that is to be executed
    """
    self.cmd = cmd

  def run(self):
    """
    Executes a program and passes to it any accompanied arguments.
    Input args must be an array with the path to the program executable in the first index.
    """
    self.ps    = Popen(self.cmd, stdout=PIPE)
    (out, err) = self.ps.communicate()
    exit_code  = self.ps.wait()
    self.out   = out
    self.err   = err

  def output(self):
    """
    Returns output result from executed process.
    """
    return self.out
