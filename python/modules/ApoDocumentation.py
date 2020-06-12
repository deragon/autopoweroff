# coding=UTF-8
#
# This file contains the text that constitute the documentation of
# Autopoweroff.

aDocument = \
  { 
    "config-IdleTime" :
      { "default" :
        """
IdleTime parameter (expressed in minutes):

  Like a screensaver, Autopoweroff detects keyboard and mouse
  activity, and if there is any activity on the server, it would not
  be powered off regardless if all the other conditions are met.  If
  set to 0, user activity on the server will be ignored.
"""
      },

    "config-StartupDelay" :
      { "default" :
        """
StartupDelay parameter (expressed in minutes):

  When the computer is booting up, if all the conditions are met and
  the computer is in the action time range, as soon as Autopoweroff
  is started, the computer will take action.  Thus, the user will never
  have the chance to boot into the computer.  This is where the
  "delay" parameter comes in.  If "delay" is set to 15 for example,
  Autopoweroff will not poweroff the computer even if all the
  conditions are met, for a period of 15 minutes after the computer
  has booted.  This allows the user to login and change Autopoweroff's
  configuration.
"""
      },

    "config-StartHour&EndHour" :
      { "default" :
        """
StartHour and EndHour parameters (expressed in hours):

  Following is the time range where the computer should not take any action
  even if all conditions are met.  In this example where StartHour=5 and
  EndHour=22, the computer will not take action between 05:00 and
  22:00, local time.
"""
      },

    "config-Hosts" :
      { "default" :
        """
Hosts parameter (list of hostnames or IPs, separated by commas):

  Here you list the list of hosts your machine is dependant, i.e. this
  computer should not take any action if any of the hosts declared here is
  still up (responding to ping).
"""
      },

    "config-Warning":
      { "default" :
        """
WARNING:  If you decide to edit this file, edit only the values of the
          parameters.  If you add comments, they will be lost at the
          next software upgrade or when the GUI configurator is being
          used to update the file.  Only values persists.
"""
      },

  }

def get(tag, language="default"):
  return aDocument[tag][language].rstrip().lstrip()
