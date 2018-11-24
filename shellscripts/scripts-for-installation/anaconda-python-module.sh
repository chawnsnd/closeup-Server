#!/bin/bash
# Apache License 2.0
# Copyright (c) 2018, CloseUp CO., LTD.

echo "===================[Anaconda3 module installation ]======================="

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

echo "==========================conda module installation completed============"


exit 0
