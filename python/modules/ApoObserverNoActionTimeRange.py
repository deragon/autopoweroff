#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import logging
import time
import re
import os
import errno

import ApoConfig
from ApoLibrary import *
from ApoObserver import *

class ApoObserverNoActionTimeRange(ApoObserverManager, ApoObserverThread):

  def status(self):

      if self.isInTimeRange:
        return ( False, "noActionTimeRange", "✘ Currently in 'No ActionTimeRange'." )
      else:
        return ( True, "noActionTimeRange", "✓ Currently out of 'No ActionTimeRange'." )


  def __init__(self, configuration):

    ApoObserverThread.__init__(self)
    self.isInTimeRange = None
    self.logger = logging.getLogger("apo.observer.noaction.timerange")
    self.configuration = configuration
    self.running = True


  def run(self):

    self.logger.info(__name__ + ".run():  started.")

    while self.running:

      # Checking if the current hour is within the "no action range".
      # Now contains the current hour.

      now = time.time()
      # self.logger.debug("UTC:  ", time.gmtime(now))
      # self.logger.debug("LOCAL:  ", time.localtime(now))
      nowtuple = time.localtime(now)
      nowhour = nowtuple.tm_hour
      # self.logger.debug(nowhour)

      previousIsInTimeRange = self.isInTimeRange

      if self.configuration.noactiontimerange[ApoConfig.STARTHOUR] <= \
         self.configuration.noactiontimerange[ApoConfig.ENDHOUR]:
        if nowhour >= self.configuration.noactiontimerange[ApoConfig.STARTHOUR] and \
           nowhour < self.configuration.noactiontimerange[ApoConfig.ENDHOUR]:
          self.isInTimeRange = True
        else:
          self.isInTimeRange = False
      else:
        if nowhour >= self.configuration.noactiontimerange[ApoConfig.STARTHOUR] or \
           nowhour < self.configuration.noactiontimerange[ApoConfig.ENDHOUR]:
          self.isInTimeRange = True
        else:
          self.isInTimeRange = False

      if previousIsInTimeRange != self.isInTimeRange:
        # State change occurred.  Need to inform about it.
        if self.isInTimeRange:
          self.logger.debug("Switched to No Action Time Range.")
        else:
          self.logger.debug("Switched out of No Action Time Range.")

      # This thread has a 1s resolution.  It needs to sleep or else it will
      # loop continuously and consume 100% CPU.
      time.sleep(1)

    self.logger.debug("ApoObserverNoActionTimeRange thread ended.")


  def terminate(self):
      self.running = False
