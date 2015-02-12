import nesrep
#from nesrep import *
#from nesrep.Core import *

if __name__ == '__main__':
    #processing = Proc()

    #Threader.Thread(1, 'init', initialize())
    #processing.start(initialize(), 'lock', 'init')
    #initialize()

    #cmd = nesrep.Core.Processing.CommandServer()
    #cmd.start()

    init = nesrep.initialize()
    if init == True:
        nesrep.log("Starting webserver", "INFO")
        #Boot the webserver
        import nesrep.Core.Webserver as webStart
        webStart.initialize()
        nesrep.start()
        #import nesrep.Modules.Anime.nyaa as nyaa
        #parsert = nyaa.SiteLoader()
        #parsert.searchsite("Durarara", "Anime")

        #anidb.getdata()
        #anidb.extract()
        #anidb.list_import()

