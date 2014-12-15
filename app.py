#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import subprocess

import tornado.httpserver
import tornado.ioloop
import tornado.web

from state import get_projects

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello, world")
        result = get_projects()
        s = str(result[0])
	projects = []
	for item in result:
		projects.append(item)
        self.render("index.html", projects=projects, s=s)

class SyncHandler(tornado.web.RequestHandler):
    def get(self):
        path = self.get_argument('path')
        last = os.path.split(path)[-1]
        # cmd = 'cd "%s" && screen -S "%s:sync" -d -m ~/miui-builder/sync.sh' %(path, last)
        cmd = '/home/eggfly/miui-builder/screen.sync.sh %s %s' %(path, last)
        code = subprocess.call(cmd, shell=True)
        if code == 0:
            self.redirect('/')
            return
        self.write("action: sync, path: %s, code: %d" %(path, code))
if __name__ == "__main__":
    app = tornado.web.Application(
        handlers = [
            (r"/", MainHandler),
            (r"/sync.*", SyncHandler),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

