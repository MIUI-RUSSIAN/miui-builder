#!/usr/bin/env python
import os

PRODUCTS = ["aries", "cancro", "pisces", "virgo", "mocha", "ferrari", "gucci"]
path = os.path.normpath(os.getcwd())
parts = path.split(os.sep)
target = []
found = False
for part in parts:
	if not part: continue
	if found: break
	for product in PRODUCTS:
		if product in part:
			found = True
			break
	target.append(part)
print "/"+os.sep.join(target)

