#!/usr/bin/python
# -*- coding: utf-8 -*-

import psutil
import time

import ApoConfig
from ApoLibrary import *
from ApoObserver import *

class ApoObserverResources(ApoObserverManager, ApoObserverThread):

    def status(self):
        if self.cpuUsage >= self.cpuUsageConfiguredLimit:
            return ( False, "resources",
                    ( f"✘ Resources are not meeting condition "
                      "(CPU = {self.cpuUsage}%)." ) )
        else:
            return ( True,  "resources",
                    ( f"✓ Resources are meeting conditions "
                      "(CPU = {self.cpuUsage}%)." ) )


    def __init__(self, configuration):

        ApoObserverThread.__init__(self)
        self.isInTimeRange = None
        self.logger = logging.getLogger("apo.observer.resources")
        self.resources = configuration.resources
        self.cpuUsageConfiguredLimit = \
            self.resources["CPU"]["Percentage"].lower()
        if self.cpuUsageConfiguredLimit == "disabled":
           self.cpuUsageConfiguredLimit = 0  # Equivalent of disabled.
        else:
           self.cpuUsageConfiguredLimit = int(self.cpuUsageConfiguredLimit)

        self.setCpuUsage()
        self.start()


    def setCpuUsage(self):
        self.cpuUsage = psutil.cpu_percent(interval=1, percpu=False)
        self.logger.debug(f"Sample CPU Usage = {self.cpuUsage}%")


    def run(self):

        self.logger.info(__name__ + ".run():  started.")

        while True:

            # Checking if the current hour is within the "no action range".
            # Now contains the current hour.

            self.setCpuUsage()

            # This thread has a 1s resolution.  It needs to sleep or else it
            # will loop continuously and consume 100% CPU.
            time.sleep(1)
