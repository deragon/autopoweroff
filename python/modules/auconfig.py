#!/usr/bin/python

import commands
import os
import sys
import time
import ConfigParser
import re
import syslog
from types import *
from __main__ import *
import apodoc

scriptname = os.path.basename(sys.argv[0])

def sendmsg(msg, priority=syslog.LOG_INFO):
  print msg
  syslog.syslog(scriptname + ":  " + str(msg))

def debug(msg):
  if testmode:
    print msg

def commentString(text):
  regexp=re.compile("(?m)^")
  return regexp.sub("# ", text.rstrip().lstrip())

#print commentString(apodoc.get('IdleTime'))
#print apodoc.get('IdleTime')

conffile = etcdir + "/autopoweroff.conf"

class APOError(Exception):
  def __init__(self, msg, errorcode):
    self.msg=msg
    self.errorcode=errorcode

class APOWarning(Exception):
  pass

class Configuration:

  def __init__(self, noshutdownrange, idletime, startupdelay, hosts):
    if noshutdownrange == None:
      self.noshutdownrange=[4, 23] # hours
    else:
      self.noshutdownrange=noshutdownrange

    if startupdelay == None:
      self.startupdelay=15 # minutes
    else:
      self.startupdelay=startupdelay

    if idletime == None:
      self.idletime=5 # minutes.
    else:
      self.idletime=idletime

    if hosts == None:
      self.hosts=range(0)
    else:
      self.hosts=hosts

    self.warnings=""
    self.errors=""
    self.configParser = ConfigParser.ConfigParser()

  def warn(self, msg):
    self.warnings = self.warnings + "  - " + msg + "\n"

  def deprecated(self, old, new):
    self.warn("\"" + old + "\" is deprecated.  Please use \"" + new + "\".")

  def optionalConfig(self, type, defaultValue, section, *options):
    regex=re.compile("(\w+)\|(\w)")
    validOption = None
    validWarn = None
    value = None
    for entry in options:
      mo=regex.search(entry)
      option=mo.group(1)
      validity=mo.group(2)

      if validity == "v":
        validOption = option

      try:
        if type == IntType:
          value = self.configParser.getint(section, option)
        elif type == StringType:
          value = self.configParser.get(section, option)

        if validity != "v":
          self.deprecated(option, validOption)
          validWarn = None  # Reseting warning, as deprecated option is
                            # available and is being used.
        if value != None:
          break

      except ConfigParser.NoOptionError:
        value = defaultValue
        if validity == "v":
          # Setting a warning, but do not print it out yet.  If a deprecated
          # token is found later, then we ignore this warning by reseting
          # validWarn to None.
          validWarn = "No \"" + option + "\" option defined in section \"" + \
                       section + "\"."

      except ConfigParser.NoSectionError:
        self.warn("No \"" + section + "\" section defined.")

    if validWarn:
        self.warn(validWarn)

    debug("configuration:  " + option + " = " + str(value))
    return value

  def read(self):

    try:
      fd=open(conffile)
      self.configParser.readfp(fd)
      fd.close()
      #print self.configParser.sections()
      #print "conffile=" + conffile

      # Shutdown range

      self.noshutdownrange[0]=self.optionalConfig( \
          IntType, 0, "NO_SHUTDOWN_TIME_RANGE", "StartHour|v", "start|d")

      self.noshutdownrange[1]=self.optionalConfig( \
          IntType, 0, "NO_SHUTDOWN_TIME_RANGE", "EndHour|v", "end|d")

      self.idletime=self.optionalConfig( \
          IntType, 0, "TIMEOUTS", "IdleTime|v", "idle_time|d")

      self.startupdelay=self.optionalConfig( \
          IntType, 0, "TIMEOUTS", "StartupDelay|v", "startup_delay|d")

      tmphosts=self.optionalConfig( \
          StringType, 0, "DEPENDANTS", "Hosts|v", "hosts|d")

      # Removing whitespaces in list before performing the split.
      self.hosts=re.sub("\s*", "", tmphosts).split(',')
        # If the configuration files contains a line like "hosts=" with no
        # actual hosts defined, an empty host shows up, which is wrong.
        # we eliminate this.
      if self.hosts[0] == '':
        # Got an empty host.  Getting ride of it.
        self.hosts = self.hosts[1:]

    except IOError:
      self.errors = "Could not open configuration file " + conffile + \
                    "\nUsing default values."
      raise APOError(self.errors, 1)

  def save(self):

    fd=open(conffile, 'w')
    fd.write("""# Autopoweroff """ + version + """ configuration file.

# WARNING:  If you decide to edit this file, edit only the values of the
#           parameters.  If you add comments, they will be lost at the
#           next software upgrade or when the GUI configurator is being
#           used to update the file.  Only values persists.


# StartHour and EndHour parameters (expressed in hours):
#
#   Following is the time range where the computer should not shutdown
#   even if all conditions are met.  In this example where StartHour=5
#   and EndHour=22, the computer will not shut down between 05:00 and
#   22:00, local time.

[NO_SHUTDOWN_TIME_RANGE]
""")
    fd.write("StartHour=" + str(int(self.noshutdownrange[0])) + "\n")
    fd.write("EndHour="   + str(int(self.noshutdownrange[1])) + "\n")

    fd.write("""

# StartupDelay parameter (expressed in minutes):
#
#   When the computer is booting up, if all the conditions are met and
#   the computer is in the shutdown time range, as soon as Autopoweroff
#   is started, the computer will shutdown.  Thus, the user will never
#   have the chance to boot into the computer.  This is where the
#   "delay" parameter comes in.  If "delay" is set to 15 for example,
#   Autopoweroff will not poweroff the computer even if all the
#   conditions are met, for a period of 15 minutes after the computer
#   has booted.  This allows the user to login and change Autopoweroff's
#   configuration.
#
#
# IdleTime parameter (expressed in minutes):
#
#   Like a screensaver, Autopoweroff detects keyboard and mouse
#   activity, and if there is any activity on the server, it would not
#   be powered off regardless if all the other conditions are met.  If
#   set to 0, user activity on the server will be ignored.

[TIMEOUTS]
""")
    fd.write("StartupDelay=" + str(int(self.startupdelay)) + "\n")
    fd.write("IdleTime=" + str(int(self.idletime))  + "\n")

    fd.write("""

# Hosts parameter (list of hostnames or IPs, separated by commas):
#
#   Here you list the list of hosts your machine is dependant, i.e. this
#   computer should not shutdown if any of the hosts declared here is
#   still up (responding to ping).

[DEPENDANTS]
""")
    fd.write("Hosts=")

    for index in range(len(self.hosts)):
      fd.write(self.hosts[index])
      if index != len(self.hosts)-1:
        fd.write(", ")
    fd.write("\n")
    fd.close();
