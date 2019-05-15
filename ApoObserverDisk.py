#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import logging
import time
import re
import os
import errno

from ApoLibrary import *

class ApoObserverDisk(threading.Thread):
  def __init__(self, disksToWatch):
    self.logger = logging.getLogger("apo.observer.Disk.thread")
    self.logger.info("Initializing")
    threading.Thread.__init__(self, name="disksToWatch")
    self.setDaemon(True)
    self.DiskFile = '/proc/diskstats'
    self.disksToWatch = disksToWatch
    self.sleep = 0

  global diskstats
  def diskstats(fd,diskname):
      line = fd.readline()
      while line:
        if re.search(diskname,line):
          data = line.split()
          y = 0
          for x in range(3, 13):
            y += int(data[x],10)
        line = fd.readline()
      return y

  def run(self):
    fd = open(self.DiskFile, 'r')
    sendmsg("ApoObserverDisk.run():  Check on " +
                     str(self.disksToWatch) + " started.")
    self.finish = False
    lastEventTime = 0.0
    global gOldDiskCount
    diskActivity = {} 
    gOldDiskCount = 0
    time.sleep(60)
    for diskname in self.disksToWatch:
      diskActivity[diskname]=0
    while not self.finish:
      y=0
      global gLastDiskEventTime
      time.sleep(60)

      for diskname in self.disksToWatch:
        y = diskstats(fd,diskname)
        if y > diskActivity[diskname]: 
          diskActivity[diskname] = y
          currentTime = time.time()
          gLastDiskEventTime = currentTime
      fd.seek(0)
      if y > gOldDiskCount:
        gOldDiskCount=y
      # print currentTime-lastEventTime
      # To reduce the quantity of output, we print only a few
      # of the events, for logger.debugging purposes.  Else, it is simply
      # to much.
      if currentTime > lastEventTime + 0.01:
        self.logger.debug(
            "ApoObserverDisk.run():  Activity detected on " + \
            str(self.disksToWatch) + " at " + str(currentTime))
      lastEventTime = currentTime
    fd.close()

  def terminate(self):
    self.finish = True

  def sleep(self, timeout):
    self.sleep = timeout
