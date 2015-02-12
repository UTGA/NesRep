__author__ = 'dorbian'
__version__ = '1.0'

import os
import sys
import threading
import multiprocessing
import logging
#import nesrep
from logging import handlers


class Loch(object):

    def __init__(self, rund):
        self.filename = "nesrep.log"
        self.maxsize = 1000000
        self.maxfiles = 5
        self.logdir = os.path.join(rund, (os.path.join("UserData", "Logs")))
        self.loggername = __name__  # "TraceLogger"
        self.level = 9
        self.logfilelocation = ""
        self._debug = False
        self._trace = False
        self.thread = ''
        self.init = False
        self.handler = ''
        self.logger = ''
        self.streamhandler = ''

    def initialize(self):
        if not self.init:
            logging.addLevelName(9, "TRACE")
            self.logger = logging.getLogger(self.loggername)
            self.logger.setLevel(self.level)

            def trace(self, message, *args, **kws):
                self._log(9, message, args, **kws)
            logging.Logger.trace = trace

            if not os.path.exists(self.logdir):
                os.makedirs(self.logdir)

            self.logfilelocation = os.path.join(self.logdir, self.filename)
            formatter = logging.Formatter('%(asctime)s %(levelname)-5s\t%(message)s', '[%d/%b/%Y:%H:%M:%S]')
            self.handler = handlers.RotatingFileHandler(self.logfilelocation, maxBytes=self.maxsize, backupCount=self.maxfiles, )
            self.handler.setLevel(self.level)

            self.streamhandler = logging.StreamHandler()
            self.streamhandler.setLevel(logging.INFO)
            if self._debug:
                self.streamhandler.setLevel(10)
            if self._trace:
                self.streamhandler.setLevel(9)
            self.streamhandler.setFormatter(formatter)
            self.handler.setFormatter(formatter)
            self.logger.addHandler(self.handler)
            self.logger.addHandler(self.streamhandler)

            self.log("Logging Initialized!", "DEBUG")
            self.init = True


    def log(self, msg, lvl):

        self.logger = logging.getLogger(self.loggername)
        if multiprocessing.current_process().name == "Main":
            self.thread = 'LOGGER'
            mps = True
        else:
            self.thread = multiprocessing.current_process().name
            mps = True

        #print self.thread

        if threading.currentThread().name == "MainThread":
            threading.currentThread().name = "LOGGER"
            self.thread = threading.currentThread().getName()
        else:
            self.thread = threading.currentThread().getName()

        msg = '{0}\t{1}'.format(self.thread, msg)

        if lvl == 'DEBUG' and self._debug:
            self.logger.debug(msg)
        elif lvl == 'INFO':
            self.logger.info(msg)
        elif lvl == 'WARN':
            self.logger.warn(msg)
        elif lvl == 'ERROR':
            self.logger.error(msg)
        elif lvl == 'TRACE' and self._trace:
            self.logger.trace(msg)
        elif lvl == 'DEBUG':
            pass
        elif lvl == 'TRACE':
            pass
        else:
            self.logger.error("***UNKNOWN*** {0}".format(msg))

#Initialize logging on it's own
# logwriter = Loch()
# logwriter.initialize()
#
#
# #New format logging IMHO a better practice
# def log(message, level):
#     if str(level).lower() == 'debug':
#         logwriter.log(message, lvl='DEBUG')
#     elif str(level).lower() == 'info':
#         logwriter.log(message, lvl='INFO')
#     elif str(level).lower() == 'warning':
#         logwriter.log(message, lvl='WARN')
#     elif str(level).lower() == 'error':
#         logwriter.log(message, lvl='ERROR')
#     elif str(level).lower() == 'trace':
#         logwriter.log(message, lvl='TRACE')
#     else:
#         logwriter.log(message, lvl='')