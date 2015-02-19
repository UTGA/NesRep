import nesrep
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, and_, or_, exists, Text
from sqlalchemy.orm import sessionmaker

if nesrep.developmentmode:
    verbose = True
else:
    verbose = False
if nesrep.dbtype == 'sqlite':

    engine = sqlalchemy.create_engine('sqlite:///{0}'.format(nesrep.db), echo=verbose)
if nesrep.dbtype == 'mysql':
    engine = sqlalchemy.create_engine("mysql+pymysql://{0}:{1}@{2}:3306/{3}".format(
        nesrep.dbuser, nesrep.dbpass, nesrep.dbip, nesrep.db))
Session = sessionmaker(bind=engine)
Base = declarative_base()
Session.configure(bind=engine)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    fullname = Column(String(250))
    password = Column(String(250))

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
                         self.name, self.fullname, self.password)


class Options(Base):
    __tablename__ = 'options'

    id = Column(Integer, primary_key=True)
    sync = Column(DateTime)

    def __repr__(self):
        return "<Options(sync='%s')>" % (
                         self.sync)


class Hosts(Base):
    __tablename__ = 'Hosts'

    id = Column(Integer, primary_key=True)
    Hostname = Column(String(250))
    IP = Column(String(250))
    scanid = Column(Integer)
    HOST_START = Column(String(250))
    HOST_END = Column(String(250))
    LastUnauthenticatedResults = Column(String(250))
    operating_system = Column(String(250))
    system_type = Column(String(250))
    Credentialed_Scan = Column(String(250))
    policy_used = Column(String(250))

    def __repr__(self):
        return"<Hosts(Hostname='%s',IP='%s', scanid='%s', HOST_START='%s', HOST_END='%s', " \
              "LastUnauthenticatedResults='%s'. operating_system='%s', system_type='%s', " \
              "Credentialed_Scan='%s', policy_used='%s')>" % (
            self.Hostname, self.IP, self.scanid, self.HOST_START, self.HOST_END, self.LastUnauthenticatedResults,
            self.operating_system, self.system_type, self.Credentialed_Scan, self.policy_used)


class Vulnerabilities(Base):
    __tablename__ = 'Vulnerabilities'

    uid = Column(Integer, primary_key=True)
    scanid = Column(Integer)
    ipid = Column(Integer)
    port = Column(String(250))
    Service_Name = Column(String(250))
    Protocol = Column(String(250))
    Severity = Column(String(250))
    ID = Column(String(250))
    Name = Column(String(250))
    Family = Column(String(250))
    Description = Column(Text)
    fname = Column(String(250))
    plugin_modification_date = Column(String(250))
    plugin_name = Column(String(250))
    plugin_publication_date = Column(String(250))
    plugin_type = Column(String(250))
    risk_factor = Column(String(250))
    script_version = Column(String(250))
    solution = Column(Text)
    synopsis = Column(String(250))
    plugin_output = Column(Text)
    see_also = Column(Text)
    tbid = Column(String(250))
    cve = Column(String(250))
    cpe = Column(Text(250))
    cvss_base_score = Column(String(250))
    cvss_temporal_score = Column(String(250))
    cvss_temporal_vector = Column(String(250))
    cvss_vector = Column(String(250))
    exploit_available = Column(String(250))
    exploitability_ease = Column(String(250))

    def __repr__(self):
        return "<Vulnerabilities(scanid='%s',ipid='%s',port='%s',Service_Name='%s',Protocol='%s',Severity='%s'," \
               "ID='%s',Name='%s',Family='%s',Description='%s',fname='%s',plugin_modification_date='%s'," \
               "plugin_name='%s',plugin_publication_date='%s',plugin_type='%s',risk_factor='%s',script_version='%s'," \
               "solution='%s',synopsis='%s',plugin_output='%s',see_also='%s',tbid='%s',cve='%s',cpe='%s'," \
               "cvss_base_score='%s',cvss_temporal_score='%s',cvss_temporal_vector='%s',cvss_vector='%s'," \
               "exploit_available='%s',exploitability_ease='%s')>" % (
            self.scanid, self.ipid, self.port, self.Service_Name, self.Protocol, self.Severity, self.ID, self.Name,
            self.Family, self.Description, self.fname, self.plugin_modification_date, self.plugin_name,
            self.plugin_publication_date, self.plugin_type, self.risk_factor, self.script_version, self.solution,
            self.synopsis, self.plugin_output, self.see_also, self.tbid, self.cve, self.cpe, self.cvss_base_score,
            self.cvss_temporal_score, self.cvss_temporal_vector, self.cvss_vector,
            self.exploit_available, self.exploitability_ease)


class VulnFound(Base):
    __tablename__ = 'VulnFound'

    id = Column(Integer, primary_key=True)
    HostID = Column(Integer)
    VulnID = Column(Integer)
    datefound = Column(String(250))

    def __repr__(self):
        return"<VulnFound(HostID='%s',VulnID='%s',datefound='%s)>" % (
            self.HostID, self.VulnID, self.datefound)


class Imported(Base):
    __tablename__ = 'Imported'

    id = Column(Integer, primary_key=True)
    File = Column(String(250))
    dateImported = Column(String(250))
    TARGET = Column(String(250))
    stop_scan_on_disconnect = Column(String(250))
    report_crashes = Column(String(250))
    name = Column(String(250))
    whoami = Column(String(250))
    optimize_test = Column(String(250))
    log_whole_attack = Column(String(250))
    ssl_cipher_list = Column(String(250))
    unscanned_closed = Column(String(250))
    plugins_timeout = Column(String(250))
    auto_enable_dependencies = Column(String(250))
    safe_checks = Column(String(250))
    report_task_id = Column(String(250))
    stop_scan_on_hang = Column(String(250))
    visibility = Column(String(250))
    max_hosts = Column(String(250))
    feed_type = Column(String(250))
    silent_dependencies = Column(String(250))
    port_range = Column(String(250))

    def __repr__(self):
        return "<Imported(File='%s',dateImported='%s',TARGET='%s',stop_scan_on_disconnect='%s',report_crashes='%s'," \
              "name='%s',whoami='%s',optimize_test='%s',log_whole_attack='%s',ssl_cipher_list='%s'," \
              "unscanned_closed='%s',plugins_timeout='%s',auto_enable_dependencies='%s',safe_checks='%s'" \
              ",report_task_id='%s',stop_scan_on_hang='%s',visibility='%s',max_hosts='%s',feed_type='%s'," \
              "silent_dependencies='%s',port_range='%s')>" % (
            self.File, self.dateImported, self.TARGET, self.stop_scan_on_disconnect, self.report_crashes, self.name,
            self.whoami, self.optimize_test, self.log_whole_attack, self.ssl_cipher_list, self.unscanned_closed,
            self.plugins_timeout, self.auto_enable_dependencies, self.safe_checks, self.report_task_id,
            self.stop_scan_on_hang, self.visibility, self.max_hosts, self.feed_type,
            self.silent_dependencies, self.port_range)

Base.metadata.create_all(engine)


#ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
#session.add(ed_user)
#session.commit

# for name, fullname in session.query(User.name, User.fullname):
#   print name, fullname
# ed Ed Jones
# wendy Wendy Williams
# mary Mary Contrary
# fred Fred Flinstone