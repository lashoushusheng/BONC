import tornado.web
import tornado.ioloop

import tornado.websocket


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class ChatHandler(tornado.websocket.WebSocketHandler):
    # 用户存储当前聊天室用户
    def open(self, *args, **kwargs):
        """
        1. connect
        2. handshake
        :param args:
        :param kwargs:
        :return:
        """
        print("来人了。。。。。。")

    def on_message(self, message):
        print(message)
        message = message + "haha  haha"
        self.write_message(message)

def run():
    settings = {
        'template_path': 'templates',
        'static_path': 'static',
    }
    application = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/chat", ChatHandler),
    ], **settings)
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    run()