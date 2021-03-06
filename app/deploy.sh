#!/bin/bash

# remove the old files
ssh root@104.236.57.23 'rm -r ~/bookstore'

# create the bookstore folder
ssh root@104.236.57.23 'mkdir ~/bookstore'

# copy all contente from the present folder
scp -r !(env)  root@104.236.57.23:~/bookstore

# stop the docker running on the cloud
ssh root@104.236.57.23 'docker stop bookstore-api'
ssh root@104.236.57.23 'docker rm bookstore-api'

# build the and run the new code
ssh root@104.236.57.23 'docker build -t bookstore-api-build ~/bookstore'
ssh root@104.236.57.23 'docker run -idt --name=bookstore-api -e MODULE_NAME="run" -e PORT="3000" -e PRODUCTION="true" -p 3000:3000 bookstore-api-build'
