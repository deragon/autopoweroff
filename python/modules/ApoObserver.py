#!/usr/bin/python
# -*- coding: utf-8 -*-

# Abstract class of all Observer class, defining common methods they should
# implement.

from abc import ABC, abstractmethod
import threading

class ApoObserverManager(ABC):

    def status(self):
        pass

    def terminate(self):
        pass

class ApoObserverThread(ABC, threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self, name=__name__)
        self.setDaemon(True)
