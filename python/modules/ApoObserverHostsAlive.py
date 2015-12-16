# -*- coding: utf-8 -*-

import commands
import threading
import time
from ApoLibrary import *

class ApoObserverHostsAlive(threading.Thread):

  def __init__(self, hostsToPing):
    self.logger = logging.getLogger("apo.observer.hosts.alive")
    self.logger.info("Initializing.")
    threading.Thread.__init__(self, name="ApoObserverHostsAlive")
    self.setDaemon(True)
    self.hostsToPing = hostsToPing
    self.hostsStillAlive = hostsToPing

  def run(self):
    self.logger.info(__name__ + ".run():  Check on " +
        str(self.hostsToPing) + " started.")
    while True:

      # While testing for hosts, we do not want to initiale to false the
      # global variable until all tests are completed.  Thus this is why we
      # use a local variable and only set the global variable once all
      # tests are completed.
      newListOfHostsStillAlive=[]
      for host in self.hostsToPing:
        #self.logger.debug("Pinging host:  >>" + host + "<<")
        status = commands.getstatusoutput("ping -c 1 -w 10 " + host)[0]
        #self.logger.debug(status)
        #signal = status & 0xFF
        exitcode = (status >> 8) & 0xFF
        #self.logger.debug(exitcode)
        if exitcode == 0:
          newListOfHostsStillAlive = newListOfHostsStillAlive + [ host ]
          break

        # Experimental use of arping.
        interfacesList=commands.getstatusoutput(
          "route -n | tail --lines=+3 | awk -F \" \" \"{print \$8}\" | sort -u")[1].split()

        self.logger.debug("Interfaces to probe for hosts with arp:  " + str(interfacesList))
        for interface in interfacesList:
          status = commands.getstatusoutput(
            "arping -w 10 -I " + interface + " " + host)[0]
          #self.logger.debug(status)
          #signal = status & 0xFF
          exitcode = (status >> 8) & 0xFF
          #self.logger.debug(exitcode)
          if exitcode == 0:
            newListOfHostsStillAlive = newListOfHostsStillAlive + [ host ]
            break

      # If the list of hosts alive changed, we report it.
      if newListOfHostsStillAlive != self.hostsStillAlive:
        newListOfHostsStillAliveSet = set(newListOfHostsStillAlive)
        previousListOfHostsStillAliveSet = set(self.hostsStillAlive)

        newHostAliveSet = newListOfHostsStillAliveSet & previousListOfHostsStillAliveSet
        newHostDeadSet = set(self.hostsToPing) - newHostAliveSet
        # Converting the set to list, simply because the display then
        # is nicer.
        sendmsg("Newly alive:  " + str(list(newHostAliveSet)) + \
            "  Newly dead:  " + str(list(newHostDeadSet)), self.logger)

      # Now that all the testing is done, we can update the global variable.
      self.hostsStillAlive=newListOfHostsStillAlive
      self.logger.debug("Hosts being checked and still alive:  " + str(newListOfHostsStillAlive))

      # Poll hosts again in 10s.
      time.sleep(10)
