__author__ = 'Dorbian'
import nesrep
import nessus.dotnessus_v2 as nessus
from bs4 import BeautifulSoup
import os
import sys
preflist = ['TARGET', 'stop_scan_on_disconnect', 'report_crashes', 'name', 'whoami', 'optimize_test',
            'log_whole_attack', 'ssl_cipher_list', 'unscanned_closed', 'plugins_timeout', 'auto_enable_dependencies',
            'safe_checks', 'report_task_id', 'stop_scan_on_hang', 'visibility', 'max_hosts', 'feed_type',
            'silent_dependencies', 'port_range']

class runrep():

    def __init__(self):
        self.rpt = nessus.Report()
        self.reportloc = nesrep.ImportDir

    def check(self):
        fils = []
        for (dirpath, dirnames, filenames) in os.walk(self.reportloc):
            fils.extend(filenames)
            break
        for filer in fils:
            self.ParseReport(filer)

    def ParseReport(self, filenames):
        print os.path.join(nesrep.ImportDir, filenames)
        soup = BeautifulSoup(open(os.path.join(self.reportloc, filenames)))
        #print soup
        for pref in soup.findAll('preference'):
            pref_name = pref.find('name').string
            pref_value = pref.find('value').string
            for val in preflist:
                if val == pref_name:
                    print '{0} : {1}'.format(pref_name, pref_value)

            #print pref_attrs['name']
            #print pref_attrs['value']
        # for t in self.rpt.targets:
        #     print t.name
        # for t in self.rpt.targets:
        #     for v in t.vulns:
        #         print t
        #         print v.get('plugin-name'), v.get('solution')
