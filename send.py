#!/usr/bin/env python2
import urllib
import sys
def main():
    data = open('bulk.txt', 'rb').read()
    data = data[-20*1000:]
    if len(sys.argv) >= 2:
        status = sys.argv[1]
        data = status + ":\n\n" + data
    sae_request(data)
def sae_request(data):
    url = "http://1.alive.sinaapp.com/raspberrypi.php"
    req = urllib.urlopen(url, data = data)
    req.read()
main()
