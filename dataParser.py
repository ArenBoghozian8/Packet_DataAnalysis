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

# Converts the text file information into a json file
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
		
		# Will loop through all the experiments
		for i in range(len(experiments)):

			#Creates new directory called JsonInfo
			os.mkdir('TestResults/'+experiments[i]+'/dataAnalysis/JsonInfo')

			# Reads though each individual text file and ignores any folders	
			for f in os.listdir('TestResults/'+experiments[i]+'/dataAnalysis'):
				if f == 'JsonInfo':
					continue
					
				f2 = open('TestResults/'+experiments[i]+'/dataAnalysis/'+f,'r')
				isComplete = False
				fileName = f

				# Reads through each ine of text and if given headers are encountered there inforamtion is saved
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

					# length is the last information of the text file, we save information and we reset to parse other frames
					if isComplete:
						r = {packetId:{'timeStamp':timeStamp,'Source IP':source,'Destination IP':destination,'Destination Port':destinationPort,'Size':size,'File Name':fileName}}
						with open('TestResults/'+experiments[i]+'/dataAnalysis/JsonInfo/'+f[:-4] +'.json', 'a') as feedsjson:
							json.dump(r, feedsjson)
							feedsjson.write(os.linesep)
						isComplete = False

# Converts the Json files into csv files
class structureData:

	def __init__(self):
		self.arr = []
	
	def restructure(self, experiments):
		
		# Will loop through all the experiments	
		for i in range(len(experiments)):
			#makes a new folder called structuredData
			os.mkdir('TestResults/'+experiments[i]+'/dataAnalysis/JsonInfo/structuredData')
			
			#goes through all the json files
			for f in os.listdir('TestResults/'+experiments[i]+'/dataAnalysis/JsonInfo'):
				#ifnore the folder
				if f == 'structuredData':
					continue

				arr = []
				tempDict = {}
				finalDict = {}
				source_ip = ""

				#Append all the json information into an array
				for line in open('TestResults/'+experiments[i]+'/dataAnalysis/JsonInfo/'+f, 'r'):
					arr.append(json.loads(line))
				#iterate through all the jason information insdie the array 
				for x in range(len(arr)):
					for key in arr[x].keys():
						datetime_object = datetime.strptime(str(arr[x][key]['timeStamp'][:-7]), '%b %d, %Y %H:%M:%S.%f')
						tempDict[key] = time.mktime( (datetime_object.year, datetime_object.month, datetime_object.day, datetime_object.hour, datetime_object.minute, datetime_object.second, 0, 0, 1) )
						source_ip = arr[x][key]['Source IP']
				# If packet is recived we insert info dict with time stamp other wise we give it -1
				for x in range(1,5001):
					if str(x) not in tempDict:
						finalDict[str(x)] = -1
					else:
						finalDict[str(x)] = tempDict[str(x)]

				w = csv.writer(open('TestResults/'+experiments[i]+'/dataAnalysis/JsonInfo/structuredData/'+f[:-5]+'( '+source_ip+' )'+'.csv', 'w'))
				w.writerow(['ID','Loss vs No Loss'])
				for key, val in finalDict.items():
					w.writerow([key, val])

# Combines all the experiments into one csv file for data analysis
class CombineExperiments():
	
	def __init__(self):
		self.ingore = 0

	def combine(self, ignore_Num, experiments,sourceIp):
		for i in range(len(experiments)):
			w = csv.writer(open( experiments[i]+'.csv', 'w'))
			w.writerow(['test_date','Country','host_ip','num_packets', 'packet_size', 'base_losses_str', 'id_pcap_data', 'discrimination_losses_str', 'id_pcap_data'])

			for country in sourceIp:
				pairTracker = 0
				file_array = []
				pcap1 = ""
				pcap2 = ""
				BaseLoss = 0
				discLoss = 0

				shapingRow1 = ""
				shapingRow2 = ""
				shapingCounter = 0

				for f in os.listdir('TestResults/'+experiments[i]+'/dataAnalysis/JsonInfo/structuredData'):
					file_array.append(f)
					file_array.sort()

				for file in file_array:
					if country in file:
						df = pd.read_csv('TestResults/'+experiments[i]+'/dataAnalysis/JsonInfo/structuredData/'+file)
						count = 0
						time = ""

						if experiments[i] == 'Compression':

							pairTracker = pairTracker + 1
							for index, row in df.iterrows():
								if row["Loss vs No Loss"] == -1:
									count = count + 1
								else:
									time = datetime.fromtimestamp(row["Loss vs No Loss"])

							if pairTracker == 1:
								BaseLoss = count
								pcap1 = file[:-4]
							else:
								discLoss = count
								pcap2 = file[:-4]

						elif experiments[i] == 'SPQ':
							print('SPQ')

						else:
							pairTracker = pairTracker + 1
							
							for index, row in df.iterrows():
								shapingCounter = shapingCounter + 1
								
								if shapingCounter == 1:
									if row["Loss vs No Loss"] == -1:
										shapingRow1 = -1
									else:
										shapingRow1 = datetime.fromtimestamp(row["Loss vs No Loss"])
										time = datetime.fromtimestamp(row["Loss vs No Loss"])
								else:
									if row["Loss vs No Loss"] == -1:
										shapingRow2 = -1
									else:
										shapingRow2 = datetime.fromtimestamp(row["Loss vs No Loss"])

									if shapingRow1 == -1 or shapingRow2 == -1:
										count = count + 2

									shapingCounter = 0	

							if pairTracker == 1:
								discLoss = count
								pcap1 = file[:-4]
							else:
								BaseLoss = count
								pcap2 = file[:-4]															




						if pairTracker == 2:
							pairTracker = 0
							w.writerow([str(time),sourceIp[country],country,'5000','1024', str(BaseLoss),pcap1, str(discLoss), pcap2])
							BaseLoss = 0
							discLoss = 0



def main():
	sourceIp = {'131.179.150.70':'planetlab1.cs.ucla.edu','131.179.150.72':'planetlab2.cs.ucla.edu', '192.16.125.12':'planetlab-2.ssvl.kth.se', '165.242.90.129':'pl2.sos.info.hiroshima-cu.ac.jp', '130.195.4.68':'planetlab1.ecs.vuw.ac.nz', '129.63.159.102':'planetlab2.cs.uml.edu', '192.91.235.230':'pluto.cs.brown.edu', '142.103.2.2':'planetlab2.cs.ubc.ca'}
	
	experiments = ['Compression','SPQ','ShapingFinal']
	
	#parse = jasonParser()
	#parse.generateJason(experiments)

	#struct = structureData()
	#struct.restructure(experiments)

	g = CombineExperiments()
	g.combine(0, experiments,sourceIp)


main()