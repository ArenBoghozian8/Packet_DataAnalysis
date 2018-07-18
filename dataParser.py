#Aren Mark Boghoziann
# July 12, 2018

import numpy as np
import pandas as pd
import os
import glob
import json
import csv
import pandas as pd
import time
from datetime import datetime

class jasonParser:

	def __init__(self):
		self.packetId = ''
		self.timeStamp = ''
		self.source = ''
		self.destination = ''
		self.destinationPort = ''
		self.size = ''
		self.fileName = ''

	def generateJason(self,experiments):

		for i in range(len(experiments)):

			os.mkdir('TestResults/'+experiments[i]+'/dataAnalysis/JsonInfo')

			for f in os.listdir('TestResults/'+experiments[i]+'/dataAnalysis'):
				if f == 'JsonInfo':
					continue
					
				f2 = open('TestResults/'+experiments[i]+'/dataAnalysis/'+f,'r')
				isComplete = False
				fileName = f

				for line in f2:
					if 'Data:' in line:
						packetIdHex = line[10:14]
						packetId = int(str(packetIdHex),16)
					elif 'Arrival Time:' in line:
						timeStamp = line[18:-1]
					elif 'Source' in line and ('Source Port:' not in line and 'Source: Alcatel-_8d:ac:f1 (e8:e7:32:8d:ac:f1)' not in line):
						source = line[12:-1]
					elif 'Destination:' in line and 'Port:' not in line:
						destination = line[17:-1]
					elif 'Destination Port:' in line:
						destinationPort = line[22:-1]
					elif '[Length:' in line:
						size = line[13:17]
						isComplete = True

					if isComplete:
						r = {packetId:{'timeStamp':timeStamp,'Source IP':source,'Destination IP':destination,'Destination Port':destinationPort,'Size':size,'File Name':fileName}}
						with open('TestResults/'+experiments[i]+'/dataAnalysis/JsonInfo/'+f[:-4] +'.json', 'a') as feedsjson:
							json.dump(r, feedsjson)
							feedsjson.write(os.linesep)
						isComplete = False


class structureData:

	def __init__(self):
		self.arr = []

	def restructure(self, experiments):
		
		for i in range(len(experiments)):
			print(experiments[i])
			os.mkdir('TestResults/'+experiments[i]+'/dataAnalysis/JsonInfo/structuredData')
			for f in os.listdir('TestResults/'+experiments[i]+'/dataAnalysis/JsonInfo'):
			
				if f == 'structuredData':
					continue

				arr = []
				tempDict = {}
				finalDict = {}
				source_ip = ""

				for line in open('TestResults/'+experiments[i]+'/dataAnalysis/JsonInfo/'+f, 'r'):
					arr.append(json.loads(line))
				for x in range(len(arr)):
					for key in arr[x].keys():
						datetime_object = datetime.strptime(str(arr[x][key]['timeStamp'][:-7]), '%b %d, %Y %H:%M:%S.%f')
						#tempDict[key] = arr[x][key]['timeStamp'][:-7]
						tempDict[key] = time.mktime( (datetime_object.year, datetime_object.month, datetime_object.day, datetime_object.hour, datetime_object.minute, datetime_object.second, 0, 0, 1) )
						source_ip = arr[x][key]['Source IP']
				for x in range(1,5001):
					if str(x) not in tempDict:
						finalDict[str(x)] = -1
					else:
						finalDict[str(x)] = tempDict[str(x)]

				w = csv.writer(open('TestResults/'+experiments[i]+'/dataAnalysis/JsonInfo/structuredData/'+f[:-5]+'( '+source_ip+' )'+'.csv', 'w'))
				w.writerow(['ID','Loss vs No Loss'])
				for key, val in finalDict.items():
					w.writerow([key, val])


class graph():
	
	def __init__(self):
		self.ingore = 0

	def draw(self, ignore_Num, experiments,sourceIp):
		for i in range(len(experiments)):
			for country in sourceIp:
				for f in os.listdir('TestResults/'+experiments[i]+'/dataAnalysis/JsonInfo/structuredData'):
					if country in f:
						df = pd.read_csv('TestResults/'+experiments[i]+'/dataAnalysis/JsonInfo/structuredData/'+f)
						print(df.groupby('Loss vs No Loss').count())
						exit()



def main():
	sourceIp = {'131.179.150.70':'planetlab1.cs.ucla.edu','131.179.150.72':'planetlab2.cs.ucla.edu', '192.16.125.12':'planetlab-2.ssvl.kth.se', '165.242.90.129':'pl2.sos.info.hiroshima-cu.ac.jp', '130.195.4.68':'planetlab1.ecs.vuw.ac.nz', '129.63.159.102':'planetlab2.cs.uml.edu', '192.91.235.230':'pluto.cs.brown.edu', '142.103.2.2':'planetlab2.cs.ubc.ca'}
	
	experiments = ['Compression','SPQ','ShapingFinal']
	
	#parse = jasonParser()
	#parse.generateJason(experiments)

	struct = structureData()
	struct.restructure(experiments)

	#g = graph()
	#g.draw(0, experiments,sourceIp)


main()