import nesrep

if __name__ == '__main__':

    init = nesrep.initialize()
    if init == True:

        nesrep.log("Starting webserver", "INFO")
        #Boot the webserver
        import nesrep.Core.Webserver as webStart
        #webStart.initialize()

        nesrep.start()

