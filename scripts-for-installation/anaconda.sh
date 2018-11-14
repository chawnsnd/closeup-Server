#!/bin/bash
# Apache License 2.0
# Copyright (c) 2018, CloseUp CO., LTD.

echo "===================[Anaconda3 installation ]======================="


echo "move to temp "
cd /tmp

echo "use curl to download anaconda"
curl -O https://repo.continuum.io/archive/Anaconda3-5.0.1-Linux-x86_64.sh

echo "verify the data integration of the installer "
sha256sum Anaconda3-5.0.1-Linux-x86_64.sh

echo " run the installer"
bash Anaconda3-5.0.1-Linux-x86_64.sh


echo "==========================anaconda installation completed============"
echo "type 'source ~/.bashrc' to activate conda"

exit 0
