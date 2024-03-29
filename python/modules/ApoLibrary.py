# -*- coding: utf-8 -*-

import errno
import syslog
import os
import logging
import pathlib
from __main__ import scriptname,gTestMode,programname

# Because of Python bug https://bugs.python.org/issue27875, we need to call
# syslog.openlog("Autopoweroff") once to setup properly the name of the
# identity to 'autopoweroffd'.  Failing to do so will default to
# '/autopoweroffd' with the leading '/'.
syslog.openlog("autopoweroffd")  # Lowercase, since this is the convention in syslog.


def createDirs(aDirs):
  for directory in aDirs:
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
    # os.chmod(directory, 0o777)  # Used to be done, but not sure why it was
                                  # required.  Commented it out 2020-05-16.
                                  # Up to know, no problems founds without it.


def sendmsg(msg, logger=None, level=logging.INFO, tosyslog=True):
  # Ill attempt to use the stacktrace to determine the name of the logger.
  # But it is not viable.  For the moment, the code remains, commented,
  # in case one would like to retry again.
  #stacktrace=traceback.extract_stack()
  #print stacktrace
  msg = str(msg)
  if logger is None:
    logger = logging.getLogger(programname)
  logger.log(level, msg)
  if tosyslog:
    syslog.syslog(msg.replace('\n', ''))


def commentString(text):
  regexp=re.compile("(?m)^")
  return regexp.sub("# ", text.rstrip().lstrip())


class APOAction:

  # No enum used here as, of this writing, this code must remain
  # compatible with 2.x Python and we do not want to add a dependency
  # to module 'enum34'.
  #
  # See:  http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python

  # Need to be capitalized.
  SHUTDOWN  = "Shutdown"
  SLEEP     = "Sleep"
  HIBERNATE = "Hibernate"
  OTHER     = "Other"

  commands={}
  commands[SHUTDOWN]  = "/sbin/shutdown -h now"
  commands[SLEEP]     = "echo -n mem >/sys/power/state"
  commands[HIBERNATE] = "echo -n disk >/sys/power/state"

  # Returns a tuple with the action and associated action command, the latter
  # being either the one hardcoded above or the one provided by the
  # configuration file.
  def parse(action, actioncommand):
    if action == None:
       return None

    action = action.strip().capitalize()
    if action == APOAction.SHUTDOWN    or \
       action == APOAction.SLEEP       or \
       action == APOAction.HIBERNATE:
      return ( action, APOAction.commands[action] )
    elif action == APOAction.OTHER:
      return ( action, actioncommand )
    else:
      return None

  # Declare parse() as a static method of the class.
  parse = staticmethod(parse)


class APOError(Exception):
  def __init__(self, header, lines, footer, errorcode):
    self.lines=lines.split("\n")
    self.header=header
    self.footer=footer
    self.errorcode=errorcode

    text=""
    for line in self.lines:
      text = text + "  - " + line + "\n"

    self.message = header + "\n\n" + text + "\n" + footer

  def __str__(self):
    return "Err #" + str(self.errorcode) + ":  " + self.message


class APOWarning(Exception):
  pass
