closeup-Server
==============

There isn't any guide yet. We'll make formatted documentation after launching our service 


in advance, you need python3.4>= and pip 


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
