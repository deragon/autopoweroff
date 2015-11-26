#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import logging
import time
import re
import os

class ApoDeviceObserverManager():

  def __init__(self):
    self.devicesArray   = []
    self.apoDevObsArray = []
    self.logger = logging.getLogger("apo.observer.device.manager")

    try:
      spkrRE = re.compile(".*spkr.*")
      devicePath = None
      # Ubuntu 06.06 does not have any /dev/input/by-paty,
      # only /dev/input.
      for devicePath in ["/dev/input/by-path", "/dev/input"]:
        if os.path.exists(devicePath):
          break

      if devicePath is None:
        sendmsg("WARNING:  No input device detected.  " + \
                "Will not be able to detect user activity.")
      else:
        for path in os.listdir(devicePath):
          if spkrRE.search(path) is not None:
            # Ignoring speaker devices.  I do not understand how a device
            # related to a speaker can be considered an input device.  A
            # microphone maybe?  Even if this is the case, if a user simply
            # leave the microphone on, it will always receive some ambient
            # sound even if the machine is not use.  We cannot make use of
            # this.  This device is available in Ubuntu 07.04 and 08.10
            # (2.6.24-17-generic).
            continue

          path = devicePath + "/" + path
          self.logger.debug("path = " + path)
          self.devicesArray.append(path)

    except OSError, oserror:
      if oserror.errno != errno.ENOENT:  # No such file or directory
        raise

    for device in self.devicesArray:
      self.logger.debug("Device = " + device)
      apoDevObs = ApoDeviceObserverThread(device)
      apoDevObs.start()
      self.apoDevObsArray.append(apoDevObs)

  def terminate():
    for thread in self.apoDevObsArray:
      thread.terminate()



class ApoDeviceObserverThread(threading.Thread):
  def __init__(self, sDevice):
    threading.Thread.__init__(self, name=sDevice)
    self.logger = logging.getLogger("apo.observer.device.thread")
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
