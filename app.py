#! /usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
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
class ScriptHandlerBase(tornado.web.RequestHandler):
    __metaclass__ = ABCMeta
    def get(self):
        path = self.get_argument('path')
        last = os.path.split(path)[-1]
        cmd = self.get_cmd(path, last)
        code = subprocess.call(cmd, shell=True)
        if code == 0:
            self.redirect('/')
            return
        action = self.get_action()
        self.write("action: %s, path: %s, code: %d" %(action, path, code))
    @abstractmethod
    def get_cmd(self, path, last): pass
    @abstractmethod
    def get_action(self): pass
class SyncHandler(ScriptHandlerBase):
    def get_cmd(self, path, last):
        return '/home/eggfly/miui-builder/screen.sync.sh %s %s' %(path, last)
    def get_action(self):
        return 'sync'
class BuildHandler(ScriptHandlerBase):
    def get_cmd(self, path, last):
        return '/home/eggfly/miui-builder/screen.build.sh %s %s' %(path, last)
    def get_action(self):
        return 'build'
if __name__ == "__main__":
    app = tornado.web.Application(
        handlers = [
            (r"/", MainHandler),
            (r"/sync.*", SyncHandler),
            (r"/build.*", BuildHandler),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

