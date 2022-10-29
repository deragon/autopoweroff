#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import logging
import time
import re
import os
import errno
import pyinotify

from ApoLibrary import *
from ApoObserver import *


class ApoObserverDeviceManager(ApoObserverManager, pyinotify.ProcessEvent):

  def __init__(self, configuration):
    self.configuration      = configuration
    self.lastInputEventTime = time.time()
    self.devicesDict        = {}
    self.logger             = logging.getLogger("apo.observer.device.manager")

    self.scanDevices()

    # From:  https://github.com/seb-m/pyinotify/wiki/Tutorial
    # The watch manager stores the watches and provides operations on watches
    wm = pyinotify.WatchManager()
    self.notifier = pyinotify.ThreadedNotifier(wm, self)
    # Start the notifier from a new thread, without doing anything as no directory or file are currently monitored yet.
    self.notifier.start()

    # Start watching the first path available in the list.
    for devicePath in ["/dev/input/by-path", "/dev/input"]:
      if os.path.exists(devicePath):
        wdd = wm.add_watch(devicePath, pyinotify.IN_DELETE | pyinotify.IN_CREATE, rec=True)
        break

  def process_IN_CREATE(self, event):
      self.logger.debug("process_IN_CREATE() - Input device added:  %s", event.pathname)
      self.manageDevice(event.pathname, "add")

  def process_IN_DELETE(self, event):
      self.logger.debug("process_IN_DELETE() - Input device removed:  %s", event.pathname)
      self.manageDevice(event.pathname, "remove")

  def manageDevice(self, devicePath, operation):
    if "spkr" in devicePath:
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
      self.logger.warn("devicePath = " + devicePath + " REJECTED because it is a speaker.")
      return

    if "smc" in devicePath:
      # On Macbook 5.5 (maybe others) the SMC is constantly sending events,
      # probably from the light sensor or something so we want to ignore this.
      #
      # The SMC is the system management controller. It's responsible for a
      # number of processes, including the cooling fans, keyboard, and LED
      # lights.

      self.logger.warn("devicePath = " + devicePath + " REJECTED because it is a SMC")
      return

    # TODO:  Improve catching.  Currently, only one model of an
    #        accelerometer is hardcoded here.  This code should made
    #        generic and catch all accelerometers.
    if "lis3lv02d" in devicePath:
      # lis3lv02d:  https://www.kernel.org/doc/Documentation/misc-devices/lis3lv02d
      #
      # Accelerometers are devices that are way to sensitive for
      # Autopoweroff.  A laptop laying on a stable table with nobody
      # touching it will still have its accelerometer reporting
      # movement.  Thus, it is not reasonable nor necessary to take this
      # devices into account when attempting to figure out if the device
      # is being used or not by a person.
      self.logger.warn("devicePath = " + devicePath + " REJECTED because it is an accelerometer.")
      return

    if operation == "add":
      if devicePath not in self.devicesDict:
          apoDevObs = ApoObserverDevice(self, devicePath)
          apoDevObs.start()
          self.devicesDict[devicePath] = apoDevObs
      else:
        sendmsg(msg=f"Asked to add {devicePath} while it is already setup.  Doing nothing, but this is a small bug from which we recovered.",
                logger=self.logger, level=syslog.LOG_WARNING)

    elif operation == "remove":
      try:
        apoDevObs = self.devicesDict.pop(devicePath)
        apoDevObs.terminate()
        sendmsg(msg=f"Remove {devicePath} since it disappeared.", logger=self.logger)
      except KeyError as keyerror:
        sendmsg(msg=f"Asked to remove {devicePath} when it was not managed at all.  Doing nothing, but this is a small bug from which we recovered.",
                logger=self.logger, level=syslog.LOG_WARNING)

    else:
        sendmsg(msg=f"BUG:  Asked to remove {devicePath} when it was not managed at all.  Doing nothing, but this is a small bug from which we recovered.",
                logger=self.logger, level=syslog.LOG_ERROR)

  def scanDevices(self):

    try:
      devicesPath = None
      # Ubuntu 06.06 does not have any /dev/input/by-path,
      # only /dev/input.
      for devicesPath in ["/dev/input/by-path", "/dev/input"]:
        if os.path.exists(devicesPath):
          break

      if devicesPath is None:
        sendmsg(msg="WARNING:  No input device detected.  " + \
                "Will not be able to detect user activity.",
                logger=self.logger, level=syslog.LOG_WARNING)
      else:
        paths=os.listdir(devicesPath)
        paths.sort()
        for path in paths:
          self.manageDevice(devicesPath + "/" + path, "add")

    except OSError as oserror:
      if oserror.errno != errno.ENOENT:  # No such file or directory
        raise

  # Return True if the time elapsed since the lastInputEventTime is bigger
  # that that of the configuration IdleTime.
  def status(self):
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
    # Sending 'terminate()' signal to all threads quickly so they can,
    # in parallel, end gracefully.  DO NOT CALL join() here or else
    # shutdown of threads will be done sequentially, taking a lot more
    # time.
    for path, apoDevObs in self.devicesDict.items():
      apoDevObs.terminate()

    # Joining with all the threads, waiting for them to end gracefully.
    for path, apoDevObs in self.devicesDict.items():
      apoDevObs.join()

    self.notifier.stop()  # Stoping the pyinotifier thread.
    self.logger.debug("ApoObserverDeviceManager thread ended.")


class ApoObserverDevice(ApoObserverThread):

  def __init__(self, apoObserverDeviceManager, sDevice):
    ApoObserverThread.__init__(self)
    self.apoObserverDeviceManager = apoObserverDeviceManager
    self.sDevice                  = sDevice

    self.logger = logging.getLogger("apo.observer.device.thread")

  def run(self):
    fd = open(self.sDevice, 'rb')
    os.set_blocking(fd.fileno(), False)  # Set no blocking
    self.logger.info("ApoObserverDevice.run():  Check on " +
                     self.sDevice + " started.")
    self.running = True
    lastEventTime = 0.0
    while self.running:
      time.sleep(5)
      try:
        # Blocks until there is something to read.  This is why we
        # do not need to setup a time.sleep(5) in this loop.
        data = fd.read()
        if data == None:
          continue  # No activity, relooping.
      except IOError as ioerror:
        if ioerror.errno == errno.ENODEV:
          # At this point, this means that the device was removed, but
          # ApoObserverDeviceManager.process_IN_DELETE() has not been called
          # yet.  This is caused by a harmless race condition.  We terminate
          # this thread anyway.  ApoObserverDeviceManager.process_IN_DELETE() will
          # eventually be called and will again call terminate() of this thread,
          # but this will be harmless.  All is good.
          self.running = False
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
    self.logger.debug("ApoObserverDevice.run():  Ended for " +
                      self.sDevice + " started.")


  def terminate(self):
    self.running = False
