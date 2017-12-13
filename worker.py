from socket import *

import sys
import os
import os.path
import time
import requests
import json

import threading
from threading import Thread
from git import Repo
from pprint import pprint
from re import match
BUFFER_SIZE=1024



def run():
	
	while True:
		clientSocket=socket(AF_INET,SOCK_STREAM)
		clientSocket.connect((gethostbyname(gethostname()),8001))
		#send request
		msg ="READY"
		clientSocket.send(msg.encode())
		
		reply=clientSocket.recv(BUFFER_SIZE).decode()
			
		
		if "DONE" in reply:
			print("bye!")
			conn.close()
			sys.exit()
		else:	
			do_work(reply,clientSocket)
			
			
		#reply=clientSocket.recv(BUFFER_SIZE).decode()
		
def do_work(reply,conn):
	sha=reply
	blob_urls = []
	files = []
	cc=[]
	token='411243e1cd58733f3356d387bb1e9475240b8bb9'
	payload = {
		'recursive': 'true',
		'access_token': token
	}
	
	
	repo = requests.get("https://api.github.com/repos/JCass45/3D5B".format(sha), params=payload)	
	
	file_tree = repo.json()['tree']
	for item in file_tree:
		if item['type'] == 'blob':
			blob_urls.append(item['url'])
	
	payload = {'access_token': token}
	headers = {'Accept': 'application/vnd.github.v3.raw+json'} #gets the raw text?
	
	for i, url in enumerate(blob_urls):
		repo = requests.get(url, params=payload, headers=headers)
		files.append(repo.text)		
		#files[i]=repo.text
		cc.append(len(files[i]))
		#print(cc[i])
	avg=getavg(cc)
	msg=str(avg) + ' '
	
	conn.send(msg.encode())
	
def getavg(cc):
	return sum(cc)/len(cc)
	
if __name__ == "__main__":
	run()