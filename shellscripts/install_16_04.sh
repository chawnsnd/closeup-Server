#!/bin/bash
# Apache License 2.0
# Copyright (c) 2018, CloseUp CO., LTD.


echo "======================[python install] ============================"

echo "add PPA"
sudo add-apt-repository ppa:jonathonf/python-3.6

echo "update"

sudo apt-get update

echo "install python3 "
sudo apt-get install python3.6

echo "install  pip "
sudo apt install python3-venv python3-pip

echo "upgrade  pip "
python3.6 -m pip install -U pip


echo "check if installed properly"
python3.6 -m pip -V

echo " install dependencies"
python3.6 -m pip install websockets --user



echo "=======================[mongodb installation]============================="


echo "Import the public key used by the package management system"
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4

echo "Create a list file for MongoDB (depends on your system)"

echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
  

echo "Reload local package database."
sudo apt-get update

echo "Install the MongoDB packages"
sudo apt-get install -y mongodb-org

echo "(optional) to prevent unintended upgrades"
echo "mongodb-org hold" | sudo dpkg --set-selections
echo "mongodb-org-server hold" | sudo dpkg --set-selections
echo "mongodb-org-shell hold" | sudo dpkg --set-selections
echo "mongodb-org-mongos hold" | sudo dpkg --set-selections
echo "mongodb-org-tools hold" | sudo dpkg --set-selections



echo "===================[Anaconda3 installation ]======================="


echo "move to temp "
cd /tmp

echo "use curl to download anaconda"
curl -O https://repo.continuum.io/archive/Anaconda3-5.0.1-Linux-x86_64.sh

echo "verify the data integration of the installer "
sha256sum Anaconda3-5.0.1-Linux-x86_64.sh

echo " run the installer"
bash Anaconda3-5.0.1-Linux-x86_64.sh

echo "source to activate conda"
source ~/.bashrc

echo " verify installation"
conda list

echo "check what python versions are available "
conda search "^python$"

echo "make your python env  (for example here, python3.6_ana is the name of the env)"
conda create --name python3.6_ana python=3.6

echo "activate your env"
source activate python3.6_ana

echo "install websockets"
conda install -c conda-forge websockets

echo "install numpy"
conda install numpy

echo "install scikit-learn"
conda install -c anaconda scikit-learn 

echo "install matplotlib"
conda install matplotlib

echo "========================================installation completed==========================="


exit 0