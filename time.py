#!/usr/bin/env python
# -*- coding: utf8 -*-
import datetime
import argparse
import os
from lst import projects
from state import title_list, title_map, get_projects

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--order', help='p: order by project name, s: order by sync time, m: order by make time, t: order by touch')
args = parser.parse_args()
order = args.order

# home = os.path.expanduser("~")
print "---- projects ----"
for key in title_list:
	print title_map[key],
print
result = get_projects()
cmp_func = None
if order == 'p':
	cmp_func = lambda a,b: cmp(a['repo'], b['repo'])
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
	print i['repo'], i['dirty']+'\t', i['path']+'\t', i['memo']+'\t',
	print
# other dirs
RAID_DIR = '/home/eggfly/raid/'
REMOTE_DIR = '/home/eggfly/remote/'
def list_others(d):
	if os.path.isdir(d):
		for path in os.listdir(d):
			full_path = os.path.join(d, path)
			if os.path.isdir(full_path):
				exist = False
				for p in projects:
					if full_path == p[1]:
						exist = True
						break
				if not exist:
					print path
list_others(RAID_DIR)
list_others(REMOTE_DIR)
# EOFi
