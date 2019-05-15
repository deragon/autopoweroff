import commands
import os
import sys
import time
import ConfigParser
import re
import syslog
from types import *
from __main__ import *
import ApoDocumentation
import logging
from ApoLibrary import *

#scriptname = os.path.basename(sys.argv[0])

#print commentString(ApoDocumentation.get('IdleTime'))
#print ApoDocumentation.get('IdleTime')

# Do not use variable "scriptname" for defining the "conffile".
# "scriptname" gets the value autopoweroffd when it is the daemon
# running, thus setting "conffile" to ".../autopoweroffd.conf", which is
# non existant.
#conffile = confdir + "/autopoweroff.conf"
conffile = confdir + "/" + programname.lower() + ".conf"

STARTHOUR=0
ENDHOUR=1
            
class APOConfigurationError(APOError):

  def __init__(self, lines, errorcode):
    
    header="CONFIRGURATION ERROR\n\nThe following errors were found in configuration file:\n" + conffile
    footer="Please fix them with the GUI or by editing the file."
    super(APOConfigurationError, self).__init__(header, lines, footer, errorcode)

class Configuration:

  # Parameters can be all None.  In that circumstance, the object should
  # be used to call read() to read the content of a configuration file.
  def __init__(self, noshutdownrange=None, idletime=None, startupdelay=None, hosts=None,  action=None, actioncommand=None, disksToWatch=None, tosyslog=True):
    self.logger = logging.getLogger("apo.conf")
    self.tosyslog = tosyslog
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
    if disksToWatch == None:
      self.disksToWatch=range(0)
    else:
      self.disksToWatch=disksToWatch

    self.warnings=""
    self.errors=""
    self.configParser = ConfigParser.ConfigParser()
    self.action=action
    self.actioncommand=actioncommand

  def warn(self, msg):
    self.warnings = self.warnings + "  - " + msg + "\n"

  def deprecated(self, old, new):
    self.warn("\"" + old + "\" is deprecated.  Please use \"" + new + "\".")

  # type:           StringType or IntType
  #
  # defaultvalue:   <any value>
  #
  # section:        Name of the section found in [] in the config file.
  #
  # options:        Entry under a section found in the config file.
  #                 Options are of format "<optioname>|<status>"
  #
  #                 <status> can be one of:
  #
  #                    - v  for valid option
  #                    - d  deprecated option
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

    self.logger.debug("configuration:  " + option + " = " + str(value))
    return value

  def read(self):

    try:
      sendmsg("Reading configuration file:  " + conffile,
              tosyslog=self.tosyslog)
      fd=open(conffile)
      self.configParser.readfp(fd)
      fd.close()
      #print self.configParser.sections()

      # Shutdown range
      self.noshutdownrange[STARTHOUR]=self.optionalConfig( \
          IntType, 0, "NO_SHUTDOWN_TIME_RANGE", "StartHour|v", "start|d")

      self.noshutdownrange[ENDHOUR]=self.optionalConfig( \
          IntType, 0, "NO_SHUTDOWN_TIME_RANGE", "EndHour|v", "end|d")

      self.idletime=self.optionalConfig( \
          IntType, 0, "TIMEOUTS", "IdleTime|v", "idle_time|d")

      self.startupdelay=self.optionalConfig( \
          IntType, 0, "TIMEOUTS", "StartupDelay|v", "startup_delay|d")

      tmphosts=self.optionalConfig( \
          StringType, 0, "DEPENDANTS", "Hosts|v", "hosts|d")
      tmpdisks=self.optionalConfig( \
	  StringType, 0, "DISKS", "Disks|v", "disks|d")

      sendmsg("Disks = " + str(tmpdisks))
      self.action=self.optionalConfig( \
          StringType, None, "ACTION", "Action|v")

      self.actioncommand=self.optionalConfig( \
          StringType, None, "ACTION", "ActionCommand|v")

      if self.action == None:
        self.errors = "No action command command provided."
      else:
        # Not assigning to self.action because parse() could return None
        # if self.action is invalid.  But we still want to print out in
        # the error message the faulty section.
        action = APOCommand.parse(self.action)
        if action == None: 
          self.errors = "Invalid action command:  \"" + \
                        str(self.action) + "\""
        else:
          self.action = action

      if self.actioncommand=="":
        self.actioncommand=None

      # Removing whitespaces in list before performing the split.
      if tmphosts == None:
        self.hosts = []
      else:
        self.hosts=re.sub("\s*", "", tmphosts).split(',')

      if tmpdisks == None:
        self.disksToWatch = []
      else:
        self.disksToWatch=re.sub("\s*", "", tmpdisks).split(',')

        # If the configuration files contains a line like "hosts=" with no
        # actual hosts defined, an empty host shows up, which is wrong.
        # we eliminate this.
        if self.hosts[0] == '':
          # Got an empty host.  Getting ride of it.
          self.hosts = self.hosts[1:]
      sendmsg("disksToWatch= " + str(self.disksToWatch))
    except IOError:
      self.errors = "Could not open configuration file " + conffile + \
                    "\nUsing default values."
      raise APOConfigurationError(self.errors, 1)

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

    fd.write("""

#  [ACTION]
#
#  Action
#
#   Action to be taken when all conditions are met.
#
#   Choices are:
#
#     - Shutdown
#     - Sleep     (suspend to ram)
#     - Hibernate (suspend to disk)
#     - Other     (ActionCommand must be supplied)
#
# ActionCommand
# 
#   In some cases, users want to specifiy the action command.  It could be a
#   script, a special version of /usr/sbin/shutdown, etc...  Arguments are
#   added after the command.  Example:
#
#   ActionCommand=/usr/sbin/shutdown -r now
#
#   Strictly speaking, the command could be anything, including actions
#   that has nothing to do with powering down a computer.  In that sense,
#   'Autopoweroff' is a misnomer; it should have been called something like
#   'ScheduledAction'.
#
#   Autopoweroff already have standard Linux command hardcoded for shutting
#   down, sleep or hibernate the computer.  Therefore, this command comes
#   commented in the default configuration file.
#
#   Since this option is an advance one, it is not available from the GUI.
[ACTION]
""")

    # TODO:  
    fd.write("Action="        + str(self.action)        + "\n")
    fd.write("ActionCommand=" + str(self.actioncommand) + "\n")

    fd.write("""
# disks parameter (list of disknames , separated by commas):
#
#   Here you list the list of disknames your machine is dependant, i.e. this
#   computer should not shutdown if any of the disks declared here is
#   still active.
[DISKS]
""")
    fd.write("disks=")
    for index in range(len(self.disksToWatch)):
      fd.write(self.disksToWatch[index])
      if index != len(self.disksToWatch)-1:
        fd.write(", ")
    fd.write("\n")

    fd.close();
