#!/bin/bash


#Install go
cd /tmp
wget "https://go.dev/dl/go1.20.4.linux-amd64.tar.gz"
sudo-g5k tar -C /usr/local -xzf go1.20.4.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin

#Build and run experiment
git clone https://github.com/datahop/libp2p-das
cd libp2p-das
if hostname = $2
then
    ./run.sh bootstrap $1
else
    ./run.sh $1
fi
cp *.csv /home/mapigaglio