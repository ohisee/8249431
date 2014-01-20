#!/bin/bash

echo "Starting runing mapper and reducer"

MAPPERCODE=./mapperAccessAddress.py
REDUCERCODE=./reducerAccessPopular.py
OUTPUTDIR=logoutput

hadoop jar /usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.0.0-mr1-cdh4.1.1.jar -mapper $MAPPERCODE -reducer $REDUCERCODE -file $MAPPERCODE -file $REDUCERCODE -input loginput -output $OUTPUTDIR 

