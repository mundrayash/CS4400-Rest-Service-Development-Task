from socket import *
import radon
from radon.cli import Config
from radon.complexity import SCORE
from radon.cli.harvest import CCHarvester
import sys
import os
import os.path
import time
import requests
import json
import shutil
import threading
from threading import Thread
from git import Repo
from pprint import pprint
from re import match
BUFFER_SIZE=1024

workernum= int(sys.argv[1])
commitdir='./commit' + str(workernum) +'/'
def run():
	while True:
		clientSocket=socket(AF_INET,SOCK_STREAM)
		clientSocket.connect((gethostbyname(gethostname()),9000))
		#send request
		msg ="READY"
		clientSocket.send(msg.encode())
		reply=clientSocket.recv(BUFFER_SIZE).decode()
		if "DONE" in reply:
			print("bye!")
			clientSocket.close()
			sys.exit()
		else:	
			do_work(reply,clientSocket)
					
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
	headers = {'Accept': 'application/vnd.github.v3.raw+json'} 
	
	# the files that we want to go through
	for i, url in enumerate(blob_urls):
		repo = requests.get(url, params=payload, headers=headers)
		filename= commitdir+ '{}.py'.format(i)
		with open(filename, 'w') as f:
			files.append(filename) #list holding all the file names
			f.write(repo.text)
	avg=getavg(cc)
	shutil.rmtree(commitdir)
	if avg!=None:
		msg="Complexity: " + str(avg) 
	else:
		msg="Done"
	conn.send(msg.encode())

def getCC(files):
	# found it on the internet
	config = Config(
			exclude="",
			ignore="",
			order=SCORE,
			no_assert=True,
			show_complexity=True,
			average=True,
			total_average=True,
			show_closures=True,
			min='A',
			max='F'
			)
	commit_complexity=0
	numfiles=0
	for i ,item in enumerate(files):
		f = open(files[i], 'r')
		results = CCHarvester(files[i], config).gobble(f)
		numfiles +=1
		total_cc = 0
		for result in results:
			commit_complexity += int(result.complexity)
				
	if numfiles !=0:	
		return commit_complexity / numfiles
	else:
		# to avoid dividing by zero
	 	return None 
if __name__ == "__main__":
	run()