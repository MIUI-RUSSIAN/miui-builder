#! /usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import os.path
import subprocess

import tornado.httpserver
import tornado.ioloop
import tornado.web

from state import get_projects

HISTORY_FILE = 'history.log'
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello, world")
        result = get_projects()
        s = str(result[0])
	projects = []
	for item in result:
		projects.append(item)
        actions = get_action_history()
        self.render("index.html", projects=projects, s=s, actions=actions)
class ScriptHandlerBase(tornado.web.RequestHandler):
    __metaclass__ = ABCMeta
    def get(self):
        path = self.get_argument('path')
        last = os.path.split(path)[-1]
        cmd = self.get_cmd(path, last)
        code = subprocess.call(cmd, shell=True)
        action = self.get_action()
        log = "action: %s, path: %s, code: %d" %(action, path, code)
        append_action_history(log)
        if code == 0:
            self.redirect('/')
            return
        self.write(log)
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
class CleanHandler(ScriptHandlerBase):
    def get_cmd(self, path, last):
        return '/home/eggfly/miui-builder/screen.clean.sh %s %s' %(path, last)
    def get_action(self):
        return 'clean'
class CleanBuildHandler(ScriptHandlerBase):
    def get_cmd(self, path, last):
        return '/home/eggfly/miui-builder/screen.cleanbuild.sh %s %s' %(path, last)
    def get_action(self):
        return 'cleanbuild'
class LogHandlerBase(tornado.web.RequestHandler):
    __metaclass__ = ABCMeta
    def get(self):
        path = self.get_argument('path')
        log_path = os.path.join(path, self.get_log_path())
        self.set_header("Content-Type", "text/plain")
        if os.path.exists(log_path):
            with open(log_path, 'rb') as f:
                self.write(f.read())
        else:
            self.write(log_path + ' is not found')
    @abstractmethod
    def get_log_path(self): pass
class SyncLogHandler(LogHandlerBase):
    def get_log_path(self):
        return 'sync.log'
class BuildLogHandler(LogHandlerBase):
    def get_log_path(self):
        return 'build.log'
class CleanLogHandler(LogHandlerBase):
    def get_log_path(self):
        return 'clean.log'
def append_action_history(action):
    with open(HISTORY_FILE, 'a+b') as f:
        f.write(str(action) + '\n')
def get_action_history():
    if not os.path.exists(HISTORY_FILE):
        return ()
    with open(HISTORY_FILE, 'r') as f:
        logs = f.readlines()
        logs.reverse()
        return logs
if __name__ == "__main__":
    app = tornado.web.Application(
        handlers = [
            (r"/", MainHandler),
            (r"/log/sync*", SyncLogHandler),
            (r"/log/build*", BuildLogHandler),
            (r"/log/clean*", CleanLogHandler),
            (r"/sync.*", SyncHandler),
            (r"/build.*", BuildHandler),
            (r"/clean.*", CleanHandler),
            (r"/cleanbuild.*", CleanBuildHandler),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

