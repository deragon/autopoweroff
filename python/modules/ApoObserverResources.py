#!/usr/bin/python
# -*- coding: utf-8 -*-

import psutil
import time

import ApoConfig
from ApoLibrary import *
from ApoObserver import *

class ApoObserverResources(ApoObserverManager, ApoObserverThread):

    def status(self):
        if self.cpuUsageConfiguredLimit == "disabled":
            return ( True,  "resources",
                    ( "✓ Resources are meeting conditions "
                      f"(CPU check disabled)." ) )
        elif self.cpuUsage >= self.cpuUsageConfiguredLimit:
            return ( False, "resources",
                    ( "✘ Resources are not meeting condition "
                      f"(CPU = {self.cpuUsage}%)." ) )
        else:
            return ( True,  "resources",
                    ( "✓ Resources are meeting conditions "
                      f"(CPU = {self.cpuUsage}%)." ) )


    def __init__(self, configuration):

        ApoObserverThread.__init__(self)
        self.logger = logging.getLogger("apo.observer.resources")
        self.resources = configuration.resources
        self.cpuUsageConfiguredLimit = \
            self.resources["CPU"]["Percentage"].lower()

        if self.cpuUsageConfiguredLimit != "disabled":
            self.cpuUsageConfiguredLimit = int(self.cpuUsageConfiguredLimit)

            self.setCpuUsage()
            self.running = True
            self.start()


    def setCpuUsage(self):
        # psutil.cpu_percent() documentation found at:
        #
        # https://psutil.readthedocs.io/en/latest/#psutil.cpu_percent
        self.cpuUsage = psutil.cpu_percent(interval=1, percpu=False)
        self.logger.debug(f"Sample CPU Usage = {self.cpuUsage}%")


    def run(self):

        self.logger.info(__name__ + ".run():  started.")

        while self.running:

            # Checking if the current hour is within the "no action range".
            # Now contains the current hour.

            self.setCpuUsage()

            # This thread has a 1s resolution.  It needs to sleep or else it
            # will loop continuously and consume 100% CPU.
            time.sleep(1)

        self.logger.debug("ApoObserverResources thread ended.")


    def terminate(self):
        self.running = False
