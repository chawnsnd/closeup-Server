closeup-Server
==============

There isn't any guide yet. We'll make formatted documentation after launching our service 


in advance, you need python3.4>= and pip 

python install & run server

``` bash
tested on ubuntu 16.04 & 18.04 (AWS)
======================================
#add PPA
sudo add-apt-repository ppa:jonathonf/python-3.6

#update

sudo apt-get update

#install python3 
sudo apt-get install python3.6

#install  pip 
sudo apt install python3-venv python3-pip

#upgrade  pip 
python3.6 -m pip install -U pip


#check if installed properly
python3.6 -m pip -V

# install dependencies
python3.6 -m pip install websockets --user

# run server 
python3.6 close-up-server.py
```

mongodb installation

```bash

tested on ubuntu 16.04 

#Import the public key used by the package management system
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4

#on ubuntu 16.04
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list

#on ubuntu 18.04
echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list

#Reload local package database.
sudo apt-get update

#Install the MongoDB packages
sudo apt-get install -y mongodb-org

#(optional) to prevent unintended upgrades
echo "mongodb-org hold" | sudo dpkg --set-selections
echo "mongodb-org-server hold" | sudo dpkg --set-selections
echo "mongodb-org-shell hold" | sudo dpkg --set-selections
echo "mongodb-org-mongos hold" | sudo dpkg --set-selections
echo "mongodb-org-tools hold" | sudo dpkg --set-selections
```
