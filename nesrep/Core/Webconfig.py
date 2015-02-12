import nesrep
import os
import cherrypy
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader(os.path.join(nesrep.server_style, 'templates')))


# def serve_template(templatename, **kwargs):
#
#     interface_dir = os.path.join(str(lazylibrarian.PROG_DIR), 'data/interfaces/')
#     template_dir = os.path.join(str(interface_dir), lazylibrarian.HTTP_LOOK)
#     _hplookup = TemplateLookup(directories=[template_dir])
#
#
#     try:
#         template = _hplookup.get_template(templatename)
#         return template.render(**kwargs)
#     except:
#         return exceptions.html_error_template().render()
# 
# {% include 'header.html' %}
#     Body
# {% include 'footer.html' %}

class WebInterface(object):

    def index(self):
        print "Test"
        if not nesrep.setup_completed:
            raise cherrypy.HTTPRedirect("setup")
        else:
            raise cherrypy.HTTPRedirect("home")
    index.exposed = True

    def setup(self, **params):
        tmpl = env.get_template('setup.html')
        try:
            ph = int(params['phase'])
        except:
            return tmpl.render(Product=nesrep.__product__, phase=0)
        if ph == 1:
            print nesrep.modules
            return tmpl.render(Modules=nesrep.modules, phase=1)
    setup.exposed = True

    def home(self):
        tmpl = env.get_template('index.html')
        return tmpl.render(salutation='Hello', target='World')
        #myDB = database.DBConnection()
        #authors = myDB.select('SELECT * from authors order by AuthorName COLLATE NOCASE')
        #return serve_template(templatename="index.html", title="Home", authors=authors)
    home.exposed = True
