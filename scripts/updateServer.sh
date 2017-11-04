#!/bin/bash

pkill node
forever start ../server.js

while :
do

code=$(node checkRepoLastUpdated.js)

if [ $code -eq "1" ]
then
git pull > /dev/null
echo Yes
pkill node
forever start ../server.js
else
echo No
fi

sleep 5s

done
