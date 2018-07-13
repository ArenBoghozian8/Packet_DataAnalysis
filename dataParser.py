#Aren Mark Boghoziann
# July 12, 2018

import numpy as np
import pandas as pd
import os
import glob
import json


experiments = ['Compression','SPQ','ShapingFinal']

for i in range(len(experiments)):

	os.mkdir('TestResults/'+experiments[i]+'/dataAnalysis/JsonInfo')

	for f in os.listdir('TestResults/'+experiments[i]+'/dataAnalysis'):

		if f == 'JsonInfo':
			continue
			
		f2 = open('TestResults/'+experiments[i]+'/dataAnalysis/'+f,'r')

		packetId = ''
		timeStamp = ''
		source = ''
		destination = ''
		destinationPort = ''
		size = ''
		fileName = f
		isComplete = False

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