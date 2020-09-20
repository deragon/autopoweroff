#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import logging
import time
import re
import os

from ApoLibrary import *

class ApoObserverDiskManager(threading.Thread):

  def __init__(self, configuration):
    threading.Thread.__init__(self, name="ApoObserverDisk")
    self.configuration = configuration
    self.lastDiskEventTime = time.time()
    self.DiskFile = '/proc/diskstats'
    self.disksToWatch = configuration.disksToWatch
    self.logger             = logging.getLogger("apo.observer.device.manager")
    self.setDaemon(True)

  global diskstats
  def diskstats(fd,diskname):
      line = fd.readline()
      y=0
      while line:
        if re.search(diskname,line):
          data = line.split()
          for x in range(3, 13):
            y += int(data[x],10)
        line = fd.readline()
      fd.seek(0)
      return y
  def status(self):
    elapsedTimeSinceLastEvent = time.time() - self.lastDiskEventTime
    condition = elapsedTimeSinceLastEvent > self.configuration.idletime * 60
#    print(" disk status " + str(elapsedTimeSinceLastEvent) + " " + str(self.lastDiskEventTime) + " " +str(condition))
    self.logger.debug(f"elapsedTimeSinceLastEvent = {elapsedTimeSinceLastEvent:0.2f} condition = {condition}")

    # Converting to minutes to make it eaiser 
    elapsedTimeSinceLastEvent = elapsedTimeSinceLastEvent / 60.0
    if condition :
      return ( True,  "DiskTime", f"✓ Last event time happened over {elapsedTimeSinceLastEvent:0.1} mins, greater than configuration IdleTime parameter set to {self.configuration.idletime:0} mins." )
    else:
      return ( False, "DiskTime", f"✘ Last event time happened over {elapsedTimeSinceLastEvent:0.1} mins, lower than configuration IdleTime parameter set to {self.configuration.idletime:0} mins." )
  def run(self):
    st = open('/proc/thread-self/stat','r')
    tid, junk = (st.readline(9)).split()
    sendmsg("Disk Thread Id = " + str(tid))
    st.close()
    fd = open(self.DiskFile, 'r')
    sendmsg("ApoObserverDisk.run():  Check on " +
                     str(self.disksToWatch) + " started.")
    self.finish = False
    diskActivity = {} 
    cnt=0
    for diskname in self.disksToWatch:
      diskActivity[diskname]=0
    while not self.finish:
      y=0
      time.sleep(60)

      for diskname in self.disksToWatch:
        y = diskstats(fd,diskname)
        if (cnt % 10) == 0:
          sendmsg(f"diskstats {diskname} = {y} ")
        cnt+=1
        if y > diskActivity[diskname]: 
          diskActivity[diskname] = y
          currentTime = time.time()
      # print currentTime-lastDiskEventTime
      # To reduce the quantity of output, we print only a few
      # of the events, for logger.debugging purposes.  Else, it is simply
      # to much.
      if currentTime > self.lastDiskEventTime + 0.01:
        self.logger.debug(
            "ApoObserverDisk.run():  Activity detected on " + \
            str(self.disksToWatch) + " at " + str(currentTime))
      self.lastDiskEventTime = currentTime
    fd.close()

  def terminate(self):
    self.finish = True

  def sleep(self, timeout):
    self.sleep = timeout
