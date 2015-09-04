# coding=UTF-8

import commands
import threading
import time
import logging
from apolib import *

class HostsStillAliveCheckThread(threading.Thread):

  def __init__(self, hosts):
    self.logger = logging.getLogger(__name__);
    self.logger.info("Initializing Hosts...")
    threading.Thread.__init__(self, name="HostsStillAliveCheckThread")
    self.setDaemon(True)
    self.hosts = hosts

  def run(self):
    global gHostsStillAlive
    gHostsStillAlive=[]
    self.logger.info(__name__ + ".run():  Check on " + \
        str(self.hosts) + " started.")
    self.finish = False
    while not self.finish:
      time.sleep(2)

      # While testing for hosts, we do not want to initiale to false the
      # global variable until all tests are completed.  Thus this is why we 
      # use a local variable and only set the global variable once all
      # tests are completed.
      hostsStillAlive=[]
      for host in self.hosts:
        #self.logger.debug("Pinging host:  >>" + host + "<<")
        status = commands.getstatusoutput("ping -c 1 -w 10 " + host)[0]
        #self.logger.debug(status)
        #signal = status & 0xFF
        exitcode = (status >> 8) & 0xFF
        #self.logger.debug(exitcode)
        if exitcode == 0:
          hostsStillAlive = hostsStillAlive + [ host ]
          break

        # Experimental use of arping.
        interfacesList=commands.getstatusoutput( \
          "route -n | tail --lines=+3 | awk -F \" \" \"{print \$8}\" | sort -u")[1].split()

        self.logger.debug("Interfaces to probe for hosts with arp:  " + str(interfacesList))
        for interface in interfacesList:
          status = commands.getstatusoutput( \
                    "arping -w 10 -I " + interface + " " + host)[0]
          #self.logger.debug(status)
          #signal = status & 0xFF
          exitcode = (status >> 8) & 0xFF
          #self.logger.debug(exitcode)
          if exitcode == 0:
            hostsStillAlive = hostsStillAlive + [ host ]
            break

      # Now that all the testing is done, we can update the global variable.
      gHostsStillAlive=hostsStillAlive
      self.logger.debug("Hosts being checked and still alive:  " + str(hostsStillAlive))
