#!/usr/bin/python

import simple

key = '/opt/stuff/sender/receiver_rsa.simple.pub'

command='/opt/stuff/receiver/script.sh'
sigfile='/opt/stuff/sender/script.sh.sign'

d = { 'command':command, 'signature':open(sigfile).read() }

s = simple.SimpleSender(key=key,port=3333)

s.add(d)
res = s.send('localhost')

print res
