from __future__ import print_function
import json
import requests
import binascii
import re
import string
from urllib.parse import unquote
from electrum.bitcoin import base_decode

def lambda_handler(event, context):
	# print("Received event: " + str(event))
	body = str(event['Body']).strip()
	data = unquote(body)
	
	if all(c in string.hexdigits for c in data):
		decoded = data
		# print("hex")
	else:
		try:
			decoded = binascii.hexlify(binascii.a2b_base64(data)).decode()
			if decoded[:2] != "01" or decoded[:2] != "02":
				decoded = base_decode(data, None, 43).hex()
			# print("not hex")
		except:
			try:
				decoded = base_decode(data, None, 43).hex()
				# print("not hex, is base43")
			except:
				decoded = None
	
	if not decoded:
		# print("PUSH DECODE ERROR")
		return
	
	decoded = decoded.strip()
	
	r = requests.post('https://api.smartbit.com.au/v1/blockchain/pushtx', json={"hex": decoded})
	
	# print(str(r.json()))
	# print(decoded)
	
	if str(r.json()['success']) == 'true' or str(r.json()['success']) == 'True':
		return '<?xml version=\"1.0\" encoding=\"UTF-8\"?>'\
			'<Response><Message>' + str(r.json()['txid']) + '</Message></Response>'
	else:
		return
