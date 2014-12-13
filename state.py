#!/usr/bin/env python
# -*- coding: utf8 -*-
import datetime
import argparse
import os
from termcolor import colored as c
from lst import projects

def stamp_to_time(t):
	# return datetime.datetime.fromtimestamp(t).strftime('%m-%d %H:%M:%S')
	return datetime.datetime.fromtimestamp(t).strftime('%m-%d %H:%M')
title_list = [
	'    sync   ',
	'   system  ',
	'   exist?  ',
	'  project  ',
	' dirty? ',
	'  path      ',
]
status_list = (
	{	'path': lambda product: 'manifest',
		'description': title_list[0],
		'info': lambda path: c(stamp_to_time(os.stat(path).st_mtime), 'green') if os.path.exists(path) else c("miss/stable", 'red')
	},
	{	'path': lambda product: 'out/target/product/'+product+"/system.img",
		'description': title_list[1],
		'info': lambda path: c(stamp_to_time(os.stat(path).st_mtime), 'green') if os.path.exists(path) else c("  missing  ", 'red')
	},
	{	'path': lambda product: '',
		'description': title_list[2],
		'info': lambda path: c('exist', 'green') if os.path.exists(path) else c("missing", 'red')
	},
)
def get_projects():
	result = []
	for project in projects:
		i = {}
		project_name = project[0]
		project_path = project[1]
		product_name = project[2]
		memo = project[3] if len(project) >= 4 else ""
		i['ps'] = []
		manifest_time = image_time = 0
		for status in status_list:
			ps = {}
			path = os.path.join(project_path, status['path'](product_name))
			if status['description'] == title_list[0]:
				if os.path.exists(path):
					manifest_time = os.stat(path).st_mtime
			elif status['description'] == title_list[1]:
				if os.path.exists(path):
					image_time = os.stat(path).st_mtime
			info = status['info'](path)
			ps['d'] = status['description']
			ps['i'] = info
			i['ps'].append(ps)
		i['pn'] = project_name
		# hack: TODO
		i['dirty'] = c('dirty', 'red') if manifest_time > image_time else c('ok', 'green')
		i['pp'] = project_path
		i['pm'] = memo
		result.append(i)
	return result
# EOF
