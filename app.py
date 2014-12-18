#! /usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import os.path
import datetime
import subprocess
import time
import tornado.httpserver
import tornado.ioloop
import tornado.web

from state import get_projects

HISTORY_FILE = 'history.log'
JOBS_FILE = 'jobs.lst'
ACTION_LIST = ('sync', 'clean', 'build', 'cleanbuild')
def check_output(command):
    s = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    s.wait()
    return s.stdout.read()
def get_extra_info():
    # screen info
    screen_info = check_output('screen -ls')
    disk_info = check_output('df -h /home/eggfly/raid /home/eggfly/remote /home/eggfly/share')
    return (screen_info + disk_info).splitlines()
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello, world")
        result = get_projects()
        s = str(result[0])
	projects = []
	for item in result:
		projects.append(item)
        actions = get_file_lines(HISTORY_FILE, True)
        jobs = get_file_lines(JOBS_FILE, False)
        nonce = int(time.time())
        extra = get_extra_info()
        self.render("index.html", projects=projects, s=s, actions=actions, nonce=nonce, jobs=jobs, extra=extra)
class ScriptHandlerBase(tornado.web.RequestHandler):
    __metaclass__ = ABCMeta
    def get(self):
        path = self.get_argument('path', None)
        last = ""
        if path : last = os.path.split(path)[-1]
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
class StartJobsHandler(ScriptHandlerBase):
    def get_cmd(self, path, last):
        return '/home/eggfly/miui-builder/screen.jobs.sh'
    def get_action(self):
        return 'trigger_start_jobs'
class LogHandlerBase(tornado.web.RequestHandler):
    __metaclass__ = ABCMeta
    def get(self):
        path = self.get_argument('path')
        log_path = os.path.join(path, self.get_log_path())
        self.set_header("Content-Type", "text/plain; charset=UTF-8")
        if os.path.exists(log_path):
            with open(log_path, 'rb') as f:
                content = f.read()
                self.write(content)
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
class RepoBranchLogHandler(LogHandlerBase):
    def get_log_path(self):
        return 'repo.branch.log'
class RepoDiffLogHandler(LogHandlerBase):
    def get_log_path(self):
        return 'repo.diff.log'
class AddJobHandler(tornado.web.RequestHandler):
    def get(self):
        path = self.get_argument('path')
        last = ""
        if path : last = os.path.split(path)[-1]
        action = self.get_argument('action')
        if action in ACTION_LIST:
            enqueue_job(path, action)
            self.redirect('/')
        else:
            self.write('action %s not found in ACTION_LIST'%action)
def enqueue_job(path, action):
    with open(JOBS_FILE, 'a+b') as f:
        f.write("%s:%s\n" %(path, action))
def append_action_history(action):
    now = datetime.datetime.now()
    time_str = now.strftime('%Y-%m-%d %H:%M:%S')
    with open(HISTORY_FILE, 'a+b') as f:
        f.write("%s: %s\n" %(time_str, str(action)))
def get_file_lines(filename, reverse):
    if not os.path.exists(filename):
        return ()
    with open(filename, 'r') as f:
        logs = f.readlines()
        if reverse: logs.reverse()
        return logs
if __name__ == "__main__":
    app = tornado.web.Application(
        handlers = [
            (r"/", MainHandler),
            (r"/log/sync*", SyncLogHandler),
            (r"/log/build*", BuildLogHandler),
            (r"/log/clean*", CleanLogHandler),
            (r"/log/repo_branch*", RepoBranchLogHandler),
            (r"/log/repo_diff*", RepoDiffLogHandler),
            (r"/sync.*", SyncHandler),
            (r"/build.*", BuildHandler),
            (r"/cleanbuild.*", CleanBuildHandler),
            (r"/clean.*", CleanHandler),
            (r"/start_jobs.*", StartJobsHandler),
            (r"/add_job.*", AddJobHandler),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

