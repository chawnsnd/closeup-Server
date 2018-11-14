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
echo "==========python installation completed==========================="
exit 0
