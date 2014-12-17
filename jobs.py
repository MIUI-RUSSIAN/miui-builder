#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import datetime
import subprocess
import time
from app import append_action_history
from state import popen_get_status_code

def main():
    while True:
        job = get_job()
        if not job:
            finish_log = 'all task finished'
            print finish_log
            append_action_history(finish_log)
            break
        path = job[0]
        action = job[1]
        last = os.path.split(path)[-1]
        cmd = get_command(action, path, last)
        code = subprocess.call(cmd, shell=True)
        log = "background task: %s, path: %s, code: %d" %(action, path, code)
        print log
        append_action_history(log)
        while True:
            working = popen_get_status_code('screen -ls | grep "%s:%s" -c' %(last, action)) == 0
            if working:
                time.sleep(5)
            else:
                break
        done_log = "done " + log
        print done_log
        append_action_history(done_log)
        dequeue_job()
def get_job():
    with open('jobs.lst', 'rb') as f:
        line = f.readline().strip()
        if not line: return None
        parts = line.split(':')
        if len(parts) != 2:
            print "error parsing job line:", line
            return None
        else:
            return (parts[0], parts[1])
def dequeue_job():
    lines = []
    with open('jobs.lst', 'rb') as f:
        lines = f.readlines()
    # don't append new task at the head of this file
    lines.pop(0)
    with open('jobs.lst', 'wb') as f:
        f.writelines(lines)
def get_command(action, path, last):
    if action == "sync":
        return '/home/eggfly/miui-builder/screen.sync.sh %s %s' %(path, last)
    if action == "build":
        return '/home/eggfly/miui-builder/screen.build.sh %s %s' %(path, last)
    if action == "clean":
        return '/home/eggfly/miui-builder/screen.clean.sh %s %s' %(path, last)
    if action == "cleanbuild":
        return '/home/eggfly/miui-builder/screen.cleanbuild.sh %s %s' %(path, last)
if __name__ == '__main__':
    main()
