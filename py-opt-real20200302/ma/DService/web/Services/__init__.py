from tornado.web import RequestHandler

from CConfig import conf
from DPublic.MyLog import MyLog


class DataServiceBaseHandler(RequestHandler):
    """
    """
    @property
    def db(self):
        return self.application.db

    @property
    def cache(self):
        return self.application.cache

    def set_post_header(self):
        """
        """
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header(
            "Access-Control-Allow-Headers",
            "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With, Content-disposition"
        )
        self.set_header(
            "Access-Control-Allow-Methods",
            "POST, GET, OPTIONS, PUT, OPTIONS, DELETE"
        )


# 日志.
logFname = r'{}/ds_data.log'.format(conf.LOG_PATH)
mylog = MyLog(logFname, level=conf.LOG_LEVEL).logger

