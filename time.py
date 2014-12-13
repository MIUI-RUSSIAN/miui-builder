#!/usr/bin/env python
# -*- coding: utf8 -*-
import datetime
import argparse
import os
from termcolor import colored as c
from lst import projects
from state import title_list, get_projects

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--order', help='p: order by project name, s: order by sync time, m: order by make time, t: order by touch')
args = parser.parse_args()
order = args.order

# home = os.path.expanduser("~")
def stamp_to_time(t):
	# return datetime.datetime.fromtimestamp(t).strftime('%m-%d %H:%M:%S')
	return datetime.datetime.fromtimestamp(t).strftime('%m-%d %H:%M')
print "---- projects ----"
for title in title_list:
	print title,
print
result = get_projects()
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
