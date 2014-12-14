#!/usr/bin/env python
# -*- coding: utf8 -*-
import datetime
import argparse
import os
from termcolor import colored
from lst import projects

def stamp_to_time(t):
	# return datetime.datetime.fromtimestamp(t).strftime('%m-%d %H:%M:%S')
	t = datetime.datetime.fromtimestamp(t)
	now = datetime.datetime.now()
	time_str = t.strftime('%m-%d %H:%M')
	delta = now - t
	if delta.days != 0: delta_str = "%2d days" % delta.days
	elif delta.seconds / 3600 != 0: delta_str = "%2d hrs " % delta.seconds / 3600
	elif delta.seconds / 60 != 0: delta_str = "%2d mins" % delta.seconds / 60
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
status_list = (
	{	'path': lambda product: 'manifest',
		'key': 'sync',
		'description': title_map['sync'],
		'info': lambda path: colored(stamp_to_time(os.stat(path).st_mtime), 'green') if os.path.exists(path) else colored("     miss/stable     ", 'green'),
		'html': lambda path: html_colored(stamp_to_time(os.stat(path).st_mtime), 'green') if os.path.exists(path) else html_colored("miss/stable", 'green')
	},
	{	'path': lambda product: 'out/target/product/'+product+"/system.img",
		'key': 'system',
		'description': title_map['system'],
		'info': lambda path: colored(stamp_to_time(os.stat(path).st_mtime), 'cyan') if os.path.exists(path) else colored("       missing       ", 'red'),
		'html': lambda path: html_colored(stamp_to_time(os.stat(path).st_mtime), 'cyan') if os.path.exists(path) else html_colored("  missing  ", 'red')
	},
	{	'path': lambda product: '',
		'key': 'exist',
		'description': title_map['exist'],
		'info': lambda path: colored('exist', 'green') if os.path.exists(path) else colored("missing", 'red'),
		'html': lambda path: html_colored('exist', 'green') if os.path.exists(path) else html_colored("missing", 'red')
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
			info = status['info'](path)
			html = status['html'](path)
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
		result.append(i)
	return result
# EOF
