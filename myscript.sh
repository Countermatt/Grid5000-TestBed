#!/bin/bash

#copy experiment directoryfrom home to tmp
cp $HOME/experiment /tmp
cd /tmp

#Install go
wget go1.20.4.linux-amd64.tar.gz
tar -C /usr/local -xzf go1.20.4.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin

#Build and run experiment
cd experiment
go build
go run -bootstrap $1

cp ./result $HOME/result_experiment