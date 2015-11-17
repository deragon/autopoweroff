#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import logging
import time

class ApoDeviceObserverThread(threading.Thread):
  def __init__(self, sDevice):
    threading.Thread.__init__(self, name=sDevice)
    self.logger = logging.getLogger(__name__)
    self.setDaemon(True)
    self.sDevice = sDevice
    self.sleep = 0

  def run(self):
    global gLastInputEventTime
    fd = open(self.sDevice, 'r')
    self.logger.info("ApoDeviceObserverThread.run():  Check on " +
                     self.sDevice + " started.")
    self.finish = False
    lastEventTime = 0.0
    while not self.finish:
      if self.sleep > 0:
        time.sleep(self.sleep)
        self.sleep = 0

      try:
        fd.read(1)
      except IOError, ioerror:
        if ioerror.errno == errno.ENODEV:
          self.finish = True
          sendmsg("Device " + self.sDevice + " absent (No such device error)", \
                  priority=syslog.LOG_NOTICE)
          continue
        else:
          raise
      currentTime = time.time()
      gLastInputEventTime = currentTime
      # print currentTime-lastEventTime
      # To reduce the quantity of output, we print only a few
      # of the events, for logger.debugging purposes.  Else, it is simply
      # to much.
      if currentTime > lastEventTime + 0.01:
        self.logger.debug(
            "ApoDeviceObserverThread.run():  Activity detected on " + \
            self.sDevice + " at " + str(currentTime))
      lastEventTime = currentTime
    fd.close()

  def terminate(self):
    self.finish = True

  def sleep(self, timeout):
    self.sleep = timeout
