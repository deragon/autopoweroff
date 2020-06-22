#!/usr/bin/python
# -*- coding: utf-8 -*-

# Abstract class of all Observer class, defining common methods they should
# implement.

from abc import ABC, abstractmethod
import threading

class ApoObserver(ABC, threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self, name=__name__)
        self.daemon = True


    def status(self):
        pass
