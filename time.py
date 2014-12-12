#!/usr/bin/env python
# -*- coding: utf8 -*-
import datetime
import argparse
import os
from termcolor import colored as c
from lst import projects

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--order', help='p: order by project name, s: order by sync time, m: order by make time, t: order by touch')
args = parser.parse_args()
order = args.order

home = os.path.expanduser("~")
def stamp_to_time(t):
	# return datetime.datetime.fromtimestamp(t).strftime('%m-%d %H:%M:%S')
	return datetime.datetime.fromtimestamp(t).strftime('%m-%d %H:%M')
title_list = [
	'    sync   ',
	'   system  ',
	'   exist?  ',
#	'  userdata ',
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
#	{	'path': lambda product: 'out/target/product/'+product+"/userdata.img",
#		'description': title_list[2],
#		'info': lambda path: "exist! " if os.path.exists(path) else "missing"
#	},
#	{	'path': lambda product: 'touch',
#		'description': 'touched:',
#		'info': lambda path: "y" if os.path.exists(path) else "n"
#	},
)

result = []
print "---- projects ----"
for title in title_list:
	print title,
print
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
		path = os.path.join(home, project_path, status['path'](product_name))
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
cmp_func = None
if order == 'p':
	cmp_func = lambda a,b: cmp(a['pn'], b['pn'])
elif order == 's':
	cmp_func = lambda a,b: cmp(a['ps'][0]['i'], b['ps'][0]['i'])
elif order == 'm':
	cmp_func = lambda a,b: cmp(a['ps'][1]['i'], b['ps'][1]['i'])
elif order == 't':
	cmp_func = lambda a,b: cmp(a['ps'][2]['i'], b['ps'][2]['i'])
if cmp_func is not None:
	result.sort(cmp_func)
for i in result:
	for ps in i['ps']:
		# print ps['d'], ps['i'],
		print ps['i'],
	print i['pn'], i['dirty']+'\t', i['pp']+'\t', i['pm']+'\t',
	print
# other dirs
DIR = '/home/eggfly/raid/'
for path in os.listdir(DIR):
	if os.path.isdir(os.path.join(DIR, path)):
		exist = False
		for p in projects:
			if p[1] in path or path in p[1]:
				exist = True
				break
		if not exist:
			print path
# EOF
