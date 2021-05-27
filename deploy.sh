#!/bin/bash

# REMEMBER TO RUN THIS TO ACTIVATE THE BASH FILES
# chmod +x deploy.sh

# SSH root will work if the SSH of the pc as been activated in the cloud

# remove the old files
ssh root@104.236.57.23 'rm -r ~/bookstore'

# # create the bookstore folder
ssh root@104.236.57.23 'mkdir ~/bookstore'

# copy all contente from the present folder
scp -r app  root@104.236.57.23:~/bookstore

scp -r Dockerfile  root@104.236.57.23:~/bookstore
scp -r requirements.txt  root@104.236.57.23:~/bookstore
scp -r ReadMe.md  root@104.236.57.23:~/bookstore
scp -r .gitignore  root@104.236.57.23:~/bookstore

# http only
# scp -r nginx-reverse-proxy  root@104.236.57.23:~/bookstore

# https
scp -r nginx-https  root@104.236.57.23:~/bookstore

# stop the docker running on the cloud
ssh root@104.236.57.23 'docker stop bookstore-api'
ssh root@104.236.57.23 'docker rm bookstore-api'

# build the and run the new code
ssh root@104.236.57.23 'docker build -t bookstore-api-build ~/bookstore'
# you could use docker-compose here so you can keep 
# PRODUCTION environment variables out of the repository
ssh root@104.236.57.23 'docker run -idt --name=bookstore-api -e MODULE_NAME="run" -e PORT="3000" -e PRODUCTION="true" -p 3000:3000 bookstore-api-build'

# build and create the nginx
ssh root@104.236.57.23 'docker stop api-nginx'
ssh root@104.236.57.23 'docker rm api-nginx'

# now start the nginx server for both http and https requests
ssh root@104.236.57.23 'docker build -t bookstore-nginx ~/bookstore/nginx-https'
ssh root@104.236.57.23 'docker run -idt --name=api-nginx -p 80:80 -p 443:443 -e DOMAIN=bookstoreapi.solomonaboyeji.com -e EMAIL=solomonaboyeji@gmail.com bookstore-nginx'