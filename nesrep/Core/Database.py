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

    def __repr__(self):
        return"<Hosts(Hostname='%s',IP='%s')>" % (
            self.Hostname, self.IP)


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
    File = Column(Integer)
    dateImported = Column(String)

    def __repr__(self):
        return"<Imported(File='%s',dateImported='%s)>" % (
            self.file, self.dateImported)

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