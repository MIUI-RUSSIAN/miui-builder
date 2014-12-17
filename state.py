#!/usr/bin/env python
# -*- coding: utf8 -*-
import datetime
import argparse
import os
import subprocess
from termcolor import colored
from lst import projects

def stamp_to_time(t):
	# return datetime.datetime.fromtimestamp(t).strftime('%m-%d %H:%M:%S')
	t = datetime.datetime.fromtimestamp(t)
	now = datetime.datetime.now()
	time_str = t.strftime('%m-%d %H:%M')
	delta = now - t
	if delta.days != 0: delta_str = "%2d days" % delta.days
	elif delta.seconds / 3600 != 0: delta_str = "%2d hrs " % (delta.seconds / 3600)
	elif delta.seconds / 60 != 0: delta_str = "%2d mins" % (delta.seconds / 60)
	elif delta.seconds != 0: delta_str = "%2d secs" % delta.seconds
	else : delta_str = "NEAR"
	return "%s (%s)" %(time_str, delta_str)
title_map = {
	'sync': '    sync   ',
	'system': '   system  ',
	'exist': '   exist?  ',
	'repo': '  repo  ',
	'dirty': ' dirty? ',
	'path': '  path      ',
}
title_list = [
	'sync',
	'system',
	'exist',
	'repo',
	'dirty',
	'path',
]
def html_colored(text, color):
	# TODO
	return text
def get_sync_info(path, project_path, product_name):
    manifest_path = project_path+'/manifest'
    sync_log_path = project_path+'/sync.log'
    if os.path.exists(sync_log_path):
        return stamp_to_time(os.stat(sync_log_path).st_mtime)
    elif os.path.exists(manifest_path):
        return stamp_to_time(os.stat(manifest_path).st_mtime)
    return '     miss/stable     '
status_list = (
	{	'path': lambda product: 'manifest',
		'key': 'sync',
		'description': title_map['sync'],
		'info': lambda path, project_path, product_name: colored(get_sync_info(path, project_path, product_name), 'green'),
		'html': lambda path, project_path, product_name: html_colored(get_sync_info(path, project_path, product_name), 'green'),
	},
	{	'path': lambda product: 'out/target/product/'+product+"/system.img",
		'key': 'system',
		'description': title_map['system'],
		'info': lambda path, project_path, product_name: colored(stamp_to_time(os.stat(path).st_mtime), 'cyan') if os.path.exists(path) else colored("       missing       ", 'red'),
		'html': lambda path, project_path, product_name: html_colored(stamp_to_time(os.stat(path).st_mtime), 'cyan') if os.path.exists(path) else html_colored("  missing  ", 'red')
	},
	{	'path': lambda product: '',
		'key': 'exist',
		'description': title_map['exist'],
		'info': lambda path, project_path, product_name: colored('exist', 'green') if os.path.exists(path) else colored("missing", 'red'),
		'html': lambda path, project_path, product_name: html_colored('exist', 'green') if os.path.exists(path) else html_colored("missing", 'red')
	},
)
def get_projects():
	result = []
	for project in projects:
		i = {}
		repo_name = project[0]
		project_path = project[1]
		product_name = project[2]
		memo = project[3] if len(project) >= 4 else ""
		i['ps'] = []
		manifest_time = image_time = 0
		for status in status_list:
			ps = {}
			key = status['key']
			path = os.path.join(project_path, status['path'](product_name))
			if key == 'sync':
				if os.path.exists(path):
					manifest_time = os.stat(path).st_mtime
			elif key == 'system':
				if os.path.exists(path):
					image_time = os.stat(path).st_mtime
			info = status['info'](path, project_path, product_name)
			html = status['html'](path, project_path, product_name)
			ps['d'] = status['description']
			ps['i'] = info
			i['ps'].append(ps)
			i[key] = html
		i['repo'] = repo_name
		# hack: TODO
		i['dirty'] = colored('dirty', 'red') if manifest_time > image_time else colored('ok', 'green')
		i['dirty_html'] = html_colored('dirty', 'red') if manifest_time > image_time else html_colored('ok', 'green')
		i['path'] = project_path
		i['memo'] = memo
		i['last_sync_status'] = get_last_status(os.path.join(project_path, 'sync.log'))
		i['last_build_status'] = get_last_status(os.path.join(project_path, 'build.log'))
		i['last_cleanbuildsuccess_time'] = try_get_file_time(os.path.join(project_path, 'cleanbuildsuccess.mark'))
		i['repo_branch_existance'] = file_existance(os.path.join(project_path, 'repo.branch.log'))
		i['repo_diff_existance'] = file_existance(os.path.join(project_path, 'repo.diff.log'))
                i['status'] = get_project_screen_status(project_path)
		result.append(i)
	return result
def file_existance(path):
    if os.path.exists(path):
        with open(path, 'rb') as f:
            lines = f.readlines()
            return len(lines)
    return 'n/a'
def try_get_file_time(path):
    if os.path.exists(path):
        return stamp_to_time(os.stat(path).st_mtime)
    return 'n/a'
def get_last_status(path):
    status = ''
    if os.path.exists(path):
        with open(path) as f:
            last_line = ''
            while True:
                line = f.readline()
                if not line:
                    status = last_line.strip()
                    break
                last_line = line
    code = None
    try:
        code = int(status)
    except:
        pass
    if code == None:
        if status != '': return 'running'
        else: return 'n/a'
    elif code == 0: return 'ok'
    else: return 'error(%d)'%code
def popen_get_status_code(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    return p.wait()
def get_project_screen_status(path):
    last = os.path.split(path)[-1]
    syncing = popen_get_status_code('screen -ls | grep "%s:sync" -c' %last) == 0
    building = popen_get_status_code('screen -ls | grep "%s:build" -c' %last) == 0
    cleanbuilding = popen_get_status_code('screen -ls | grep "%s:cleanbuild" -c' %last) == 0
    l = []
    if syncing: l.append("syncing")
    if building: l.append("building")
    if cleanbuilding: l.append("cleanbuilding")
    return '<br>'.join(l)
# EOF
