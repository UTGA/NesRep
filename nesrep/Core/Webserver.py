__author__ = 'Dorbian'
import os
import sys
import nesrep
import cherrypy

from Webconfig import WebInterface


def initialize():

    cherrypy.config.update({
        'log.screen': True,
        'server.thread_pool': 10,
        'server.socket_port': nesrep.server_port,
        'server.socket_host': nesrep.server_host,
        'engine.autoreload.on': False,
    })

    conf = {
        '/': {
            'tools.staticdir.root': nesrep.server_style
        },
        '/interfaces': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': "interfaces"
        },
        '/img': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': "img"
        },
        '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': "css"
        },
        '/js': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': "js"
        },
        '/templates': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': "templates"
        },
        '/fonts': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': "fonts"
        },
        # '/favicon.ico': {
        #     'tools.staticfile.on': True,
        #     'tools.staticfile.filename': "images/favicon.ico"
        # }
    }

    if nesrep.server_pass != "":
        conf['/'].update({
            'tools.auth_basic.on': True,
            'tools.auth_basic.realm': 'Kaidame',
            'tools.auth_basic.checkpassword': cherrypy.lib.auth_basic.checkpassword_dict(
                {nesrep.server_user: nesrep.server_pass})
        })

    # Prevent time-outs
    cherrypy.engine.timeout_monitor.unsubscribe()
    cherrypy.tree.mount(WebInterface(), nesrep.server_root, config=conf)

    cherrypy.engine.autoreload.on = True

    try:
        cherrypy.process.servers.check_port(nesrep.server_host, nesrep.server_port)
        cherrypy.server.start()
    except IOError:
        print 'Failed to start on port: {0}. Is something else running?'.format(nesrep.server_port)
        sys.exit(0)
    #cherrypy.server.wait()
