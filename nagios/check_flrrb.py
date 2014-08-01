#!/usr/bin/python

import sys
import urllib2
import json

apiKey = "YOUR_API_KEY_HERE"
key = sys.argv[1]

host = "http://flrrb.com:8000"
path = "/api/get"

url = "%s%s" % (host,path)

d = { "apiKey": apiKey, "key": key }

res = urllib2.urlopen(url, json.dumps(d))
v = json.loads(res.read())

print v['comment']
exit(v['status_code'])
