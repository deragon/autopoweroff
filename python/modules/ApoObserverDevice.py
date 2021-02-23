#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import logging
import time
import re
import os
import errno

from ApoLibrary import *
from ApoObserver import *

class ApoObserverDeviceManager(ApoObserverManager):

  def __init__(self, configuration):
    self.configuration      = configuration
    self.lastInputEventTime = time.time()
    self.devicesArray       = []
    self.apoDevObsArray     = []
    self.logger             = logging.getLogger("apo.observer.device.manager")

    try:
      devicePath = None
      # Ubuntu 06.06 does not have any /dev/input/by-path,
      # only /dev/input.
      for devicePath in ["/dev/input/by-path", "/dev/input"]:
        if os.path.exists(devicePath):
          break

      if devicePath is None:
        sendmsg("WARNING:  No input device detected.  " + \
                "Will not be able to detect user activity.")
      else:
        for path in os.listdir(devicePath):
          if "spkr" in path:
            # Ignoring speaker devices.  I do not understand how a device
            # related to a speaker can be considered an input device.  The
            # state of some volume buttons can be read from it?  Maybe
            # microphones show up as "spkr" devices?  Even if it is a
            # microphone, if a user simply leaves it on, it will always
            # receive some ambient sound even if the machine is not use.  We
            # cannot make use of this.
            #
            # This device was shown in Ubuntu 07.04 and 08.10
            # (2.6.24-17-generic).  However, it was not seen showing under
            # 18.04 and 19.10.
            self.logger.warn("path = " + path + " REJECTED because it is a speaker.")
            continue

          # TODO:  Improve catching.  Currently, only one model of an
          #        accelerometer is hardcoded here.  This code should made
          #        generic and catch all accelerometers.
          if "lis3lv02d" in path:
            # lis3lv02d:  https://www.kernel.org/doc/Documentation/misc-devices/lis3lv02d
            #
            # Accelerometers are devices that are way to sensitive for
            # Autopoweroff.  A laptop laying on a stable table with nobody
            # touching it will still have its accelerometer reporting
            # movement.  Thus, it is not reasonable nor necessary to take this
            # devices into account when attempting to figure out if the device
            # is being used or not by a person.
            self.logger.warn("path = " + path + " REJECTED because it is an accelerometer.")
            continue

          path = devicePath + "/" + path
          self.logger.debug("path = " + path)
          self.devicesArray.append(path)

    except OSError as oserror:
      if oserror.errno != errno.ENOENT:  # No such file or directory
        raise

    for device in self.devicesArray:
      self.logger.debug("Device = " + device)
      apoDevObs = ApoObserverDevice(self, device)
      apoDevObs.start()
      self.apoDevObsArray.append(apoDevObs)

  # Return True if the time elapsed since the lastInputEventTime is bigger
  # that that of the configuration IdleTime.
  def status(self):
    print("self.configuration = " + str(self.configuration.idletime))
    elapsedTimeSinceLastEvent = time.time() - self.lastInputEventTime
    condition = elapsedTimeSinceLastEvent > self.configuration.idletime * 60
    self.logger.debug(f"elapsedTimeSinceLastEvent = {elapsedTimeSinceLastEvent:0.2f} condition = {condition}")

    # Converting to minutes to make it eaiser 
    elapsedTimeSinceLastEvent = elapsedTimeSinceLastEvent / 60.0
    if condition :
      return ( True,  "idleTime", f"✓ Last event time happened over {elapsedTimeSinceLastEvent:0.1f} mins, greater than configuration IdleTime parameter set to {self.configuration.idletime:0} mins." )
    else:
      return ( False, "idleTime", f"✘ Last event time happened over {elapsedTimeSinceLastEvent:0.1f} mins, lower than configuration IdleTime parameter set to {self.configuration.idletime:0} mins." )

  def setLastInputEventTime(self, lastInputEventTime):
    self.lastInputEventTime = lastInputEventTime

  def terminate(self):
    for thread in self.apoDevObsArray:
      thread.terminate()


class ApoObserverDevice(ApoObserverThread):

  def __init__(self, apoObserverDeviceManager, sDevice):
    ApoObserverThread.__init__(self)
    self.apoObserverDeviceManager = apoObserverDeviceManager
    self.sDevice                  = sDevice
    self.sleep                    = 0

    self.logger = logging.getLogger("apo.observer.device.thread")

  def run(self):
    fd = open(self.sDevice, 'rb')
    self.logger.info("ApoObserverDevice.run():  Check on " +
                     self.sDevice + " started.")
    self.finish = False
    lastEventTime = 0.0
    while not self.finish:
      if self.sleep > 0:
        time.sleep(self.sleep)
        self.sleep = 0

      try:
        fd.read(1)
      except IOError as ioerror:
        if ioerror.errno == errno.ENODEV:
          self.finish = True
          sendmsg("Device " + self.sDevice + " absent (No such device error)", \
                  priority=syslog.LOG_NOTICE)
          continue
        else:
          raise
      currentTime = time.time()
      self.apoObserverDeviceManager.setLastInputEventTime(currentTime)

      # print currentTime-lastEventTime
      # To reduce the quantity of output, we print only a few
      # of the events, for logger.debugging purposes.  Else, it is simply
      # to much.
      if currentTime > lastEventTime + 0.01:
        self.logger.debug(
            "ApoObserverDevice.run():  Activity detected on " + \
            self.sDevice + " at " + str(currentTime))
      lastEventTime = currentTime
    fd.close()

  def terminate(self):
    self.finish = True

  def sleep(self, timeout):
    self.sleep = timeout
