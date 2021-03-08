# -*- coding: utf-8 -*-

import subprocess
import threading
import time
import socket
from ApoLibrary import *

class ApoObserverHostsAlive(threading.Thread):

  def __init__(self, hostsToPing):
    threading.Thread.__init__(self, name="ApoObserverHostsAlive")
    self.daemon = True
    self.logger = logging.getLogger("apo.observer.hosts.alive")
    self.logger.info("Initializing.")
    self.setDaemon(True)
    self.hostsToPing = hostsToPing
    self.hostsStillAlive = hostsToPing
    self.running = True

  def run(self):
    self.logger.info(__name__ + ".run():  Check on " +
        str(self.hostsToPing) + " started.")
    while self.running:
      # While testing for hosts, we do not want to initialize to false the
      # global variable until all tests are completed.  Thus this is why we
      # use a local variable and only set the global variable once all
      # tests are completed.
      newListOfHostsStillAlive=[]
      for host in self.hostsToPing:
        #self.logger.debug("Pinging host:  >>" + host + "<<")

        # Searching on the net, as of 2020-04-25, it seams the easiest
        # way to perform a ping is by calling the outside 'ping' command.
        # Go figure why.
        cmd = [ "ping", "-c", "1", "-w", "10", host ]
        cp = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if cp.returncode == 0:
          # Host return ping, thus confirming it exists.  Adding it to
          # the list of hosts alive.
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
        sendmsg( \
            "Old alive:  " + str(self.hostsStillAlive) + \
            "  Newly alive:  " + str(list(newHostAliveSet)) + \
            "  Newly dead:  " + str(list(newHostDeadSet)), self.logger)

      # Now that all the testing is done, we can update the global variable.
      self.hostsStillAlive=newListOfHostsStillAlive
      self.logger.debug("Hosts being checked and still alive:  " + str(newListOfHostsStillAlive))

      # Poll hosts again in 10s.
      time.sleep(10)
    self.logger.debug("ApoObserverHostsAlive thread ended.")


  def terminate(self):
    self.running = False
