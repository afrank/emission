#!/usr/bin/python2.7

import sys
import select
import os
import pickle
import json
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import hashlib
import binascii
import simple

payload = ""

priv_key = '/opt/stuff/receiver/receiver_rsa.simple'
verify_key = '/opt/stuff/receiver/sender_rsa.simple.pub'

while True:
	r = select.select([ sys.stdin ], [], [], 0)[0]
	if r:
		payload += os.read(sys.stdin.fileno(), 50)
	else:
		break


try:
	s = simple.SimpleCrypt(key=priv_key)
	payload = pickle.loads(s.decrypt(*pickle.loads(payload)))
except:
	print "not a proper pickle."
	sys.stdout.flush()
	exit(2)

s = simple.SimpleCrypt(key=verify_key)
for p in payload:
	print p
	print s.verify_sign(**json.loads(p))
	sys.stdout.flush()

