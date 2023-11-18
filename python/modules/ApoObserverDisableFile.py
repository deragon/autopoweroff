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

import pyinotify

class ApoObserverDisableFile(ApoObserverManager, pyinotify.ProcessEvent):

    def status(self):

        if self.disabled:
            return ( True, "disabled", "✘ Currently disabled (" + self.disablefile + " exists)." )
        else:
            return ( False, "disabled", "✓ Currently enabled (" + self.disablefile + " absent)." )


    def __init__(self, disablefile):

        ApoObserverManager.__init__(self)
        self.logger = logging.getLogger("apo.observer.disablefile")

        self.disabled = os.path.exists(disablefile)
        self.disablefile = disablefile

        disabledir=os.path.dirname(disablefile)

        # From:  https://github.com/seb-m/pyinotify/wiki/Tutorial
        # The watch manager stores the watches and provides operations on watches
        wm = pyinotify.WatchManager()
        self.notifier = pyinotify.ThreadedNotifier(wm, self)

        # Start the notifier from a new thread, without doing anything as no
        # directory or file are currently monitored yet.
        self.notifier.start()

        # Watching parent directory, because if one watches for
        # self.disablefile, if it does not exist, a "No such file or
        # directory" directory will be thrown and nothing will be watched.
        #
        # When a IN_(CREATE|DELETE) occurs, we then check if it is
        # self.disablefile or not.
        #
        # See: https://stackoverflow.com/questions/47005198/inotify-add-watch-fails-with-no-such-file-or-directory
        wm.add_watch(disabledir, pyinotify.IN_DELETE | pyinotify.IN_CREATE, rec=True)


    def process_IN_CREATE(self, event):
        if(event.pathname == self.disablefile):
            self.logger.debug("process_IN_CREATE() - Disable file detected:  %s", event.pathname)
            self.disabled = True


    def process_IN_DELETE(self, event):
        if(event.pathname == self.disablefile):
            self.logger.debug("process_IN_DELETE() - Disable file removed:  %s", event.pathname)
            self.disabled = False


    def terminate(self):
        self.notifier.stop()


    def wait_termination(self):
        pass
