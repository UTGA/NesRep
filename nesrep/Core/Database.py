import nesrep
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, and_, or_, exists
from sqlalchemy.orm import sessionmaker

if nesrep.developmentmode:
    verbose = True
else:
    verbose = False

engine = sqlalchemy.create_engine('sqlite:///{0}'.format(nesrep.dbasefile), echo=verbose)
Session = sessionmaker(bind=engine)
Base = declarative_base()
Session.configure(bind=engine)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

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
    Hostname = Column(String)
    IP = Column(String)
    scanid = Column(Integer)
    HOST_START = Column(String)
    HOST_END = Column(String)
    LastUnauthenticatedResults = Column(String)
    operating_system = Column(String)
    system_type = Column(String)
    Credentialed_Scan = Column(String)
    policy_used = Column(String)

    def __repr__(self):
        return"<Hosts(Hostname='%s',IP='%s', scanid='%s', HOST_START='%s', HOST_END='%s', " \
              "LastUnauthenticatedResults='%s'. operating_system='%s', system_type='%s', " \
              "Credentialed_Scan='%s', policy_used='%s')>" % (
            self.Hostname, self.IP, self.scanid, self.HOST_START, self.HOST_END, self.LastUnauthenticatedResults,
            self.operating_system, self.system_type, self.Credentialed_Scan, self.policy_used)


class Vulnerability(Base):
    __tablename__ = 'Vulnerabilities'

    id = Column(Integer, primary_key=True)
    vulnerability = Column(String)
    details = Column(String)

    def __repr__(self):
        return"<Vulnerabilities(vulnerability='%s',details='%s')>" % (
            self.vulnerability, self.details)


class VulnFound(Base):
    __tablename__ = 'VulnFound'

    id = Column(Integer, primary_key=True)
    HostID = Column(Integer)
    VulnID = Column(Integer)
    datefound = Column(String)

    def __repr__(self):
        return"<VulnFound(HostID='%s',VulnID='%s',datefound='%s)>" % (
            self.HostID, self.VulnID, self.datefound)


class Imported(Base):
    __tablename__ = 'Imported'

    id = Column(Integer, primary_key=True)
    File = Column(String)
    dateImported = Column(String)
    TARGET = Column(String)
    stop_scan_on_disconnect = Column(String)
    report_crashes = Column(String)
    name = Column(String)
    whoami = Column(String)
    optimize_test = Column(String)
    log_whole_attack = Column(String)
    ssl_cipher_list = Column(String)
    unscanned_closed = Column(String)
    plugins_timeout = Column(String)
    auto_enable_dependencies = Column(String)
    safe_checks = Column(String)
    report_task_id = Column(String)
    stop_scan_on_hang = Column(String)
    visibility = Column(String)
    max_hosts = Column(String)
    feed_type = Column(String)
    silent_dependencies = Column(String)
    port_range = Column(String)

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