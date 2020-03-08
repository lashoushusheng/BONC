import tornado.ioloop
import tornado.web
import time


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!")

    def post(self, *args, **kwargs):
        self.write("Hello, world")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


if __name__ == "__main__":
    print("server start!")
    app = make_app()
    app.listen(7777)
    tornado.ioloop.IOLoop.instance().start()


