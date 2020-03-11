from CConfig import conf
import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(
    'mysql://{}:{}@{}:{}/{}'.format(
        conf.MYSQL_USER, conf.MYSQL_PASSWD, conf.MYSQL_HOST, conf.MYSQL_PORT, conf.MYSQL_DB
    ),
    connect_args={"charset": "utf8"},
    echo=False,
    pool_recycle=60,
    pool_size=5,
    max_overflow=10,
    # pool_pre_ping=True
)

Base = declarative_base()
db_session = scoped_session(
    sessionmaker(bind=engine)
)


# def create_all():
#     Base.metadata.create_all(
#         bind=engine
#     )
#
# def drop_all():
#     Base.metadata.drop_all(
#         bind=engine
#     )

# def re_connect(self):
#     try:
#         self.connection.ping()
#     except:
#         self.connection()

# session = DBSession()
# session.close()
