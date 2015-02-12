__author__ = 'Dorbian'
# Configuration parser script
# Can run on anything, make a minor mod to the module you are running it in.
import nesrep
import os
import ConfigParser


class ConfigCheck():

    def __init__(self):
        self.configfile = ''
        self.results = ''
        self.config = ConfigParser.RawConfigParser()
        self.config.read(nesrep.configfile)
        if nesrep.developmentmode:
            self.logs = True
            nesrep.log("Loading config: {0}".format(nesrep.configfile), "DEBUG")

    # Check if the config key is an integer
    def check_int(self, sect, key, def_val, cset=False):
        if not cset:
            try:
                var_out = self.config.getint(sect, key)
            except ConfigParser.NoOptionError:
                var_out = def_val
                self.config.set(sect, key, def_val)

            if self.logs:
                nesrep.log('** Loaded INT: {0} : {1} -> {2} (Default {3})'.format(sect, key, var_out, def_val), 'DEBUG')

            return int(var_out)

        if cset:
            self.config.set(sect, key, def_val)
            nesrep.log('** Set INT: {0} : {1} to {2}'.format(sect, key, def_val), 'DEBUG')

    # Check if the config key is a boolean
    def check_bool(self, sect, key, def_val, cset=False):
        if not cset:
            try:
                var_out = self.config.getboolean(sect, key)
            except ConfigParser.NoOptionError:
                var_out = def_val
                self.config.set(sect, key, def_val)

            if self.logs:
                nesrep.log('** Loaded BOOL: {0} : {1} -> {2} (Default {3})'.format(sect, key, var_out, def_val), 'DEBUG')
            return bool(var_out)

        if cset:
            self.config.set(sect, key, def_val)
            nesrep.log('** Set BOOL: {0} : {1} to {2}'.format(sect, key, def_val), 'DEBUG')

    # Check if the config key is a float
    def check_float(self, sect, key, def_val, cset=False):
        if not cset:
            try:
                var_out = self.config.getfloat(sect, key)
            except ConfigParser.NoOptionError:
                var_out = def_val
                self.config.set(sect, key, def_val)

            if self.logs:
                nesrep.log('** Loaded FLOAT: {0} : {1} -> {2} (Default {3})'.format(sect, key, var_out, def_val), 'DEBUG')
            return float(var_out)

        if cset:
            self.config.set(sect, key, def_val)
            nesrep.log('** Set FLOAT: {0} : {1} to {2}'.format(sect, key, def_val), 'DEBUG')

    # Check if the config key is a string
    def check_str(self, sect, key, def_val, cset=False):
        if not cset:
            try:
                var_out = self.config.get(sect, key)
            except ConfigParser.NoOptionError:
                var_out = def_val
                self.config.set(sect, key, def_val)

            if self.logs and not cset:
                nesrep.log('** Loaded STR: {0} : {1} -> {2} (Default {3})'.format(sect, key, var_out, def_val), 'DEBUG')
            return str(var_out)

        if cset:
            self.config.set(sect, key, def_val)
            nesrep.log('** Set STR: {0} : {1} to {2}'.format(sect, key, def_val), 'DEBUG')

    # Check if section exists
    def CheckSec(self, sec):
        if self.config.has_section(sec):
            if self.logs:
                nesrep.log('* Loaded Section: {0}'.format(sec), 'DEBUG')
                return True
        else:
            self.config.add_section(sec)

    # Write configuration to file
    def config_write(self):
        with open(nesrep.configfile, 'wb') as configfile:
            self.config.write(configfile)
        if self.logs:
            nesrep.log('* Wrote Config: {0}'.format(nesrep.configfile), 'DEBUG')
