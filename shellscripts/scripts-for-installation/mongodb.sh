#!/bin/bash
# Apache License 2.0
# Copyright (c) 2018, CloseUp CO., LTD.

echo "Import the public key used by the package management system"
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4

echo "Create a list file for MongoDB (depends on your system)"

echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
  

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
echo "=========================mongodb installation completed==========="
exit 0
