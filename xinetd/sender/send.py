#!/usr/bin/python

import simple

key = '/opt/stuff/sender/receiver_rsa.simple.pub'

d = { 'command': '/opt/stuff/receiver/script.sh', 'comment': 'here is a comment' }

s = simple.SimpleSender(key=key,port=3333)

s.add(d)
res = s.send('localhost')

print res
