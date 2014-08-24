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

while True:
	r = select.select([ sys.stdin ], [], [], 0)[0]
	if r:
		payload += os.read(sys.stdin.fileno(), 50)
	else:
		break


try:
	payload = pickle.loads(simple.SimpleCrypt(key=priv_key).decrypt(*pickle.loads(payload)))
except:
	print "not a proper pickle."
	sys.stdout.flush()
	exit(2)

for p in payload:
	print p
	sys.stdout.flush()

