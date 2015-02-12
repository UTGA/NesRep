import nesrep


def optsargs():
    nesrep.log("Checking boot time arguments", "DEBUG")
    from optparse import OptionParser

    p = OptionParser()
    p.add_option('-d', '--daemon', action="store_true", dest='daemon', help="Run the server as a daemon")
    p.add_option('-q', '--quiet', action="store_true", dest='quiet', help="Don't log to console")
    p.add_option('-p', '--port', dest='port', default=None, help="Force webinterface to listen on this port")
    p.add_option('--nobrowser', action="store_true", dest='nobrowser', help="Don't start your browser")
    p.add_option('--datadir', dest='datadir', default=None, help="Path to the data directory")
    p.add_option('--config', dest='config', default=None, help="alternative Path to config.ini file")

    nesrep.options, nesrep.args = p.parse_args()
