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


def repl(inputt):
    inputt = inputt.replace('\n', '<br>')
    inputt = inputt.replace('\r', '<br>')
    inputt = inputt.replace("'", "`")
    inputt = inputt.replace('"', '`')
    inputt = inputt.replace('\t', ' ')
    return inputt
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

        #Check if already imported
        if not imported:
            lst = "tmpqry = DB.Imported({0})".format(query)
            exec lst
            session.add(tmpqry)
            session.flush()
            session.refresh(tmpqry)
            self.report = tmpqry.id
            session.commit()
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
                                osstring = repl(tags.string)
                                query += ", operating_system = '{0}'".format(osstring)
                            elif tags_attr['name'] == 'netbios-name':
                                query += ", Hostname = '{0}'".format(tags.string)
                            else:
                                query += ", {0} = '{1}'".format(tags_attr['name'], tags.string)
                    ips = 'tmpips = DB.Hosts({0})'.format(query)
                    exec ips
                    session.add(tmpips)
                    session.flush()
                    session.refresh(tmpips)
                    ipid = tmpips.id
                    session.commit()
                    ret = session.query(DB.exists().where(DB.Vulnerabilities.port == pref_value)).scalar()
                    for reportitem in repo.findAll("reportitem"):
                        qwry = "ipid='{0}'".format(ipid)
                        qwry += ", scanid='{0}'".format(self.report)
                        reportitem_attr = dict(reportitem.attrs)
                        qwry += ", port='{0}'".format(reportitem_attr['port'])
                        qwry += ", Service_Name='{0}'".format(reportitem_attr['svc_name'])
                        qwry += ", Protocol='{0}'".format(reportitem_attr['protocol'])
                        qwry += ", Severity='{0}'".format(reportitem_attr['severity'])
                        qwry += ", ID='{0}'".format(reportitem_attr['pluginid'])
                        nam = repl(reportitem_attr['pluginname'])
                        qwry += ", Name='{0}'".format(nam)
                        qwry += ", Family='{0}'".format(reportitem_attr['pluginfamily'])
                        desc = repl(reportitem.description.string)
                        qwry += ", Description='{0}'".format(desc)
                        qwry += ", fname='{0}'".format(reportitem.fname.string)
                        qwry += ", plugin_modification_date='{0}'".format(reportitem.plugin_modification_date.string)
                        qwry += ", plugin_name='{0}'".format(reportitem.plugin_name.string)
                        qwry += ", plugin_publication_date='{0}'".format(reportitem.plugin_publication_date.string)
                        qwry += ", plugin_type='{0}'".format(reportitem.plugin_type.string)
                        qwry += ", risk_factor='{0}'".format(reportitem.risk_factor.string)
                        qwry += ", script_version='{0}'".format(reportitem.script_version.string)
                        sol = repl(reportitem.solution.string)
                        qwry += ", solution='{0}'".format(sol)
                        qwry += ", synopsis='{0}'".format(reportitem.synopsis.string)
                        try:
                            plou = repl(reportitem.plugin_output.string)
                            qwry += ", plugin_output='{0}'".format(plou)
                        except:
                            pass
                        try:
                            seealso = repl(reportitem.see_also.string)
                            qwry += ", see_also='{0}'".format(seealso)
                        except:
                            pass
                        try:
                            qwry += ", tbid='{0}'".format(reportitem.bid.string)
                        except:
                            pass
                        try:
                            qwry += ", cve='{0}'".format(reportitem.cve.string)
                        except:
                            pass
                        try:
                            cpe = repl(reportitem.cpe.string)
                            qwry += ", cpe='{0}'".format(cpe)
                        except:
                            pass
                        try:
                            qwry += ", cvss_base_score='{0}'".format(reportitem.cvss_base_score.string)
                            qwry += ", cvss_temporal_score='{0}'".format(reportitem.cvss_temporal_score.string)
                            qwry += ", cvss_temporal_vector='{0}'".format(reportitem.cvss_temporal_vector.string)
                            qwry += ", cvss_vector='{0}'".format(reportitem.cvss_vector.string)
                        except:
                            pass
                        try:
                            qwry += ", exploit_available='{0}'".format(reportitem.exploit_available.string)
                            qwry += ", exploitability_ease='{0}'".format(reportitem.exploitability_ease.string)
                        except:
                            pass
                        vulns = 'vulnimps = DB.Vulnerabilities({0})'.format(qwry)
                        exec vulns
                        session.add(vulnimps)
                        session.flush()
                        session.refresh(vulnimps)
                        session.commit()