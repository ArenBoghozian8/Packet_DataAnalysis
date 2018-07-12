#!/bin/bash

#Aren Mark Boghozian
# Script to convert all the pcap files to txt

cd 'TestResults/Compression'
mkdir "dataAnalysis"

for file in *.pcap; do
    [ -e "$file" ] || continue
    tshark -V -r "$file" > "dataAnalysis/${file%.pcap}.txt"
done

cd "../SPQ"
mkdir "dataAnalysis"

for file in *.pcap; do
    [ -e "$file" ] || continue
    tshark -V -r "$file" > "dataAnalysis/${file%.pcap}.txt"
done

cd "../ShapingFinal"
mkdir "dataAnalysis"

for file in *.pcap; do
    [ -e "$file" ] || continue
    tshark -V -r "$file" > "dataAnalysis/${file%.pcap}.txt"
done
