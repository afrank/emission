#!/usr/bin/python

import socket
import time
import struct
import pickle
import urllib2
import json
from Crypto.PublicKey import RSA
import hashlib
import binascii
import os
from Crypto.Cipher import AES
import Crypto.Util.number
# from unittest import TestCase
from Crypto.Util import randpool
import base64

class SimpleCrypt:
	@property
	def key(self):
		return self._key
	@key.setter
	def key(self,val):
		self._key = val
	def __init__(self,**kwargs):
		self.block_size = 16
		self.key_size = 32
		self.mode = AES.MODE_CBC
		for k, v in kwargs.iteritems():
			setattr(self, k, v)
	def encrypt(self,plain_text):
		self.sig_key = self.set_rsa_key(self.key)
		key_bytes = randpool.RandomPool(512).get_bytes(self.key_size)
		pad = self.block_size - len(plain_text) % self.block_size
		data = plain_text + pad * chr(pad)
		iv_bytes = randpool.RandomPool(512).get_bytes(self.block_size)
		encrypted_bytes = iv_bytes + AES.new(key_bytes, self.mode, iv_bytes).encrypt(data)
		encrypted_string = base64.urlsafe_b64encode(str(encrypted_bytes))
		b = base64.urlsafe_b64encode(str(key_bytes))
		key_string = self.rsa_encrypt(b)
		return (key_string,encrypted_string)
	def decrypt(self,*args):
		self.ver_key = self.set_rsa_key(self.key)
		key_string = self.rsa_decrypt(args[0])
		encrypted_string = args[1]
		key_bytes = base64.urlsafe_b64decode(key_string)
		encrypted_bytes = base64.urlsafe_b64decode(encrypted_string)
		iv_bytes = encrypted_bytes[:self.block_size]
		encrypted_bytes = encrypted_bytes[self.block_size:]
		plain_text = AES.new(key_bytes, self.mode, iv_bytes).decrypt(encrypted_bytes)
		pad = ord(plain_text[-1])
		plain_text = plain_text[:-pad]
		return plain_text
	set_rsa_key = lambda self, key: RSA.importKey(open(key).read())
	rsa_encrypt = lambda self, plain_text: self.sig_key.encrypt(plain_text,16)
	rsa_decrypt = lambda self, encrypted_text: self.ver_key.decrypt(encrypted_text)

class SimpleSender(object):
	@property
	def key(self):
		return self._key
	@key.setter
	def key(self,val):
		self._key = val
	@property
	def port(self):
		return self._port
	@port.setter
	def port(self,val):
		self._port = val
	def __init__(self,**kwargs):
		self.payload = []
		for k, v in kwargs.iteritems():
			setattr(self, k, v)
	def add(self,payload):
		if payload is None:
			return False
		j = json.dumps(payload)
		self.payload.append(j)
	def get(self):
		return self.payload
	def flush(self):
		self.payload = []
	def send(self,host):
		msg = pickle.dumps(SimpleCrypt(key=self.key).encrypt(pickle.dumps(self.payload, protocol=2)), protocol=2)
		sock = socket.socket()
		sock.connect((host, self._port))
		sock.sendall(msg)
		resp = ""
		while True:
			r = sock.recv(4096)
			if r:
				resp += r
			else:
				break
		sock.close()
		self.flush()
		return resp

