#!/bin/bash


#Install go
wget "https://go.dev/dl/go1.20.4.linux-amd64.tar.gz"
tar "-C /usr/local -xzf go1.20.4.linux-amd64.tar.gz"
export PATH=$PATH:/usr/local/go/bin

#Build and run experiment
git clone https://github.com/datahop/libp2p-das
cd libp2p-das
/bin/bash run.sh $1