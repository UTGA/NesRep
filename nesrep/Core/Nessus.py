__author__ = 'Dorbian'
import nesrep
import nessus.dotnessus_v2 as nessus
from bs4 import BeautifulSoup
import os
import nesrep.Core.Database as DB
import datetime
import sys
preflist = ['TARGET', 'stop_scan_on_disconnect', 'report_crashes', 'name', 'whoami', 'optimize_test',
            'log_whole_attack', 'ssl_cipher_list', 'unscanned_closed', 'plugins_timeout', 'auto_enable_dependencies',
            'safe_checks', 'report_task_id', 'stop_scan_on_hang', 'visibility', 'max_hosts', 'feed_type',
            'silent_dependencies', 'port_range']
tagslist = ['HOST_START', 'HOST_END', 'LastUnauthenticatedResults', 'Credentialed_Scan', 'policy-used', 'host-ip',
            'system-type', 'operating-system', 'netbios-name']

session = DB.Session()

class runrep():

    def __init__(self):
        self.rpt = nessus.Report()
        self.reportloc = nesrep.ImportDir
        self.report = ''

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
        query = "File='{0}', dateImported='{1}'".format(filenames, datetime.datetime.now())
        imported = False

        #Get Preferences

        for pref in soup.findAll('preference'):
            pref_name = pref.find('name').string
            pref_value = pref.find('value').string
            if pref_name in preflist:
                query += ", {0}='{1}'".format(pref_name, pref_value)
                if pref_name == 'report_task_id':
                    ret = session.query(DB.exists().where(DB.Imported.report_task_id == pref_value)).scalar()
                    if not ret:
                        nesrep.log("{0} has not been imported yet, importing".format(filenames), "INFO")
                    else:
                        nesrep.log("{0} has already been imported".format(filenames), "INFO")
                        imported = True
        if not imported:
            lst = "tmpqry = DB.Imported({0})".format(query)
            exec lst
            session.add(tmpqry)
            session.flush()
            session.refresh(tmpqry)
            self.report = tmpqry.id
            #session.commit()
            for repo in soup.findAll('report'):
                for rephost in repo.findAll('reporthost'):
                    rephost_attr = dict(rephost.attrs)
                    print rephost_attr[u'name']
                    query = "scanid = '{0}'".format(self.report)
                    for tags in rephost.findAll('tag'):
                        tags_attr = dict(tags.attrs)
                        if tags_attr['name'] in tagslist:
                            if tags_attr['name'] == 'policy-used':
                                query += ", policy_used = '{0}'".format(tags.string)
                            elif tags_attr['name'] == 'host-ip':
                                query += ", IP = '{0}'".format(tags.string)
                            elif tags_attr['name'] == 'system-type':
                                query += ", system_type = '{0}'".format(tags.string)
                            elif tags_attr['name'] == 'operating-system':
                                osstring = tags.string.replace('\n', ', ').replace('\r', ', ')
                                query += ", operating_system = '{0}'".format(osstring)
                            elif tags_attr['name'] == 'netbios-name':
                                query += ", Hostname = '{0}'".format(tags.string)
                            else:
                                query += ", {0} = '{1}'".format(tags_attr['name'], tags.string)
                    print query
                    ips = 'tmpips = DB.Hosts({0})'.format(query)
                    exec ips
                    session.add(tmpips)
                    session.flush()
                    session.refresh(tmpips)
                    ipid = tmpips.id
                    #session.commit()
                    qwry = "ipid='{0}'".format(ipid)
                    for reportitem in repo.findAll("reportitem"):
                        reportitem_attr = dict(reportitem.attrs)
                        qwry += "port='{0}'".format(reportitem_attr['port'])
                        qwry += "Service Name='{0}'".format(reportitem_attr['svc_name'])
                        qwry += "Protocol='{0}'".format(reportitem_attr['protocol'])
                        qwry += "Severity='{0}'".format(reportitem_attr['severity'])
                        qwry += "ID='{0}'".format(reportitem_attr['pluginid'])
                        qwry += "Name='{0}'".format(reportitem_attr['pluginname'])
                        qwry += "Family='{0}'".format(reportitem_attr['pluginfamily'])
                        qwry += "Description='{0}'".format(reportitem.description.string)
                        qwry += "fname='{0}'".format(reportitem.fname.string)
                        qwry += "plugin_modification_date='{0}'".format(reportitem.plugin_modification_date.string)
                        qwry += "plugin_name='{0}'".format(reportitem.plugin_name.string)
                        qwry += "plugin_publication_date='{0}'".format(reportitem.plugin_publication_date.string)
                        qwry += "plugin_type='{0}'".format(reportitem.plugin_type.string)
                        qwry += "risk_factor='{0}'".format(reportitem.risk_factor.string)
                        qwry += "script_version='{0}'".format(reportitem.script_version.string)
                        qwry += "solution='{0}'".format(reportitem.solution.string)
                        qwry += "synopsis='{0}'".format(reportitem.synopsis.string)
                        qwry += "plugin_output='{0}'".format(reportitem.plugin_output)
                        try:
                            tmpbid = reportitem.bid.string
                            print 'bid:', tmpbid
                        except:
                            pass
                        try:
                            tmpcve = reportitem.cve.string
                            print 'cve:', tmpcve
                        except:
                            pass
                        try:
                            tmpcvss = reportitem.cvss_base_score.string
                            print 'cvss_base_score:', tmpcvss
                            print 'cvss_temporal_score:', reportitem.cvss_temporal_score.string
                        except:
                            pass