#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os.path

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello, world")
        # projects = [{'repo': 'cancro-v6-kk-alpha'}]
        # self.render("index.html", projects=projects)
        self.render("index.html")

application = tornado.web.Application(
    handlers = [
      (r"/", MainHandler),
    ], 
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
)

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

