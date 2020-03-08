import tornado
import tornado.web
import tornado.ioloop
import tornado.options
from tornado.options import define, options
from tornado.httpserver import HTTPServer

from CConfig import conf
from DPublic.MysqlDB import db_session
from DService.web.data_service_settings import url_handlers, settings


define("port", default=conf.DATA_SERVICE_PORT, help="Model-Analysis  data-service start...", type=int)


class Application(tornado.web.Application):
    """
    """
    def __init__(self, handlers, **settings):
        tornado.web.Application.__init__(
            self, handlers, **settings
        )
        self.db = db_session

application = Application(url_handlers, **settings)


if __name__ == "__main__":
    """
    """
    tornado.options.parse_command_line()

    http_server = tornado.httpserver.HTTPServer(application)

    http_server.listen(options.port)

    print('Model-Analysis data-service running on http://0.0.0.0:%d' % (options.port))

    tornado.ioloop.IOLoop.instance().start()
