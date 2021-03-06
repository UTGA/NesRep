from __future__ import with_statement

__author__ = 'Dorbian'
__product__ = 'NesRep'
__version__ = '0.0.1'

# Imports from the module itself
import Core.Regular_Functions as RF
import Core.logger as Logger
import Core.Arguments as Arguments
import copy
import sys
import os
import threading
import datetime

########################
# DEVMODE SWITCH
########################
developmentmode = True
########################

# Predefine namespaces
# ------------------------------------------------------------------
# Boolean statements
__initialized__ = update = setup_completed = False
# Empty string statements
configfile = rundir = logdir = datadir = db = dbfunc = server_port = server_user = server_root = server_host = \
    server_pass = server_style = debugging = tracing = moduledir = cachedir = appdir = ImportDir = dbuser = \
            dbpass = dbhost = dbtype = dbip = ''
# Empty lists
options = args = process = []
# Empty dicts
tmpd = modules = mods = dict()
thread_lock = threading.Lock()
threading.currentThread().name = __product__
# ------------------------------------------------------------------
try:
    if not logwriter in globals():
        pass
except NameError:
    rund = RF.get_rundir()
    logwriter = Logger.Loch(rund)
    if developmentmode is True:
        logwriter._debug = True
        logwriter._trace = True
    logwriter.initialize()


def log(msg, inf):
    logwriter.log(msg, inf)


def initialize():
    with thread_lock:
        # Set all variables needed as global variables
        global __initialized__, debugging, rundir, options, args, datadir, logdir, db, configfile, dbfunc, \
            tracing, process, __product__, __version__, logwriter, webserver, cherrypy, config, cfg, \
            server_port, server_user, server_root, server_host, server_pass, server_style, DataBase, developmentmode, \
            moduledir, logwriter, cachedir, scheduler, modules, setup_completed, appdir, mods, ImportDir, dbuser,\
            dbpass, dbhost, dbtype, dbip

        # check if arguments where passed
        # ------------------------------------------------------------------
        Arguments.optsargs()

        # If set to true a lot more logging will happen
        # ------------------------------------------------------------------
        developmentmode = developmentmode

        # Set some statics
        # ------------------------------------------------------------------
        __version__ = __version__
        __product__ = __product__

        # Add rundirs for libs to work
        # ------------------------------------------------------------------
        rundir = RF.get_rundir()
        RF.add_rundirs(rundir)

        log("Initializing {0} {1}".format(__product__, __version__), "INFO")
        appdir = os.path.join(rundir, 'nesrep')
        datadir = os.path.join(rundir, 'UserData')
        logdir = os.path.join(datadir, 'Logs')
        cachedir = os.path.join(appdir, 'Cache')
        Userdir = os.path.expanduser("~")
        if os.name == 'nt':
            Userdir = os.path.join(Userdir, 'My Documents')
            log("NT System detected", "DEBUG")

        configfile = os.path.join(datadir, '{0}.ini'.format(__product__))
        dbasefile = os.path.join(datadir, '{0}.vdb'.format(__product__))

        RF.check_dir(datadir)
        RF.check_dir(cachedir)

        # Load scheduler
        # ------------------------------------------------------------------
        from apscheduler.scheduler import Scheduler
        scheduler = Scheduler()

        # Configuration
        # ------------------------------------------------------------------
        import Core.Conf as Config
        cfg = Config.ConfigCheck()

        cfg.CheckSec('Server')
        server_host = cfg.check_str('Server', 'IP', '0.0.0.0')
        server_port = cfg.check_int('Server', 'Port', 5000)
        server_user = cfg.check_str('Server', 'Username', '')
        server_pass = cfg.check_str('Server', 'Password', '')
        server_root = cfg.check_str('Server', 'Webroot', '/')
        server_style = os.path.join(os.path.join(appdir, "WebData"), cfg.check_str('Server', 'Style', 'default'))

        cfg.CheckSec('Data')
        ImportDir = cfg.check_str('Data', 'ImportDir', os.path.join(Userdir, 'Nessus-Import'))
        dbtype = cfg.check_str('Data', 'dbtype', 'sqlite')
        db = cfg.check_str('Data', 'db', '{0}.vdb'.format(__product__))
        dbuser = cfg.check_str('Data', 'dbuser', 'root')
        dbpass = cfg.check_str('Data', 'dbpass', 'kenny')
        dbip = cfg.check_str('Data', 'dbip', '192.168.211.129')

        cfg.CheckSec('General')
        setup_completed = cfg.check_bool('General', 'Setup_Complete', "False")

        cfg.config_write()

        RF.check_dir(ImportDir)

        # Initialize the database
        # ------------------------------------------------------------------
        log("Connecting to database {0}".format(dbasefile), "INFO")
        import Core.Database as Database

        # Scheduler start
        # ------------------------------------------------------------------
        scheduler.start()

        # Initialized
        # ------------------------------------------------------------------
        __initialized__ = True
        return True


def jobs():
    i = 0
    for job in scheduler.get_jobs():
        i += 1
        log(job, "DEBUG")
    if (setup_completed) and i <= 1:
        log("No modules loaded", "ERROR")


def start():
    import Core.Nessus as Nessus
    starttime = datetime.datetime.now()
    rpt = Nessus.runrep()
    #scheduler.add_interval_job(rpt.check, minutes=1, start_date=starttime+datetime.timedelta(seconds=6))
    scheduler.add_interval_job(jobs, minutes=15, start_date=starttime+datetime.timedelta(seconds=10))
    rpt.check()


def add_names(varname, conts):
    with thread_lock:
        tmpvars = "{0} = ''".format(varname)
        tmpglob = 'global {0}'.format(varname)
        tmpcont = '{0} = {1}'.format(varname, conts)
        exec tmpvars
        exec tmpglob
        exec tmpcont