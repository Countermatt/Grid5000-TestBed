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
    ./run.sh bootstrap $1 $2 &
    for (( i=0; i<$5-2; i++ ))
    do
    ./run.sh $1 &
    done
    ./run.sh $1
else
    if hostname = $3
    then
        for (( i=0; i<$4-1; i++ ))
        do
        ./run.sh $1 &
        done
        ./run.sh $1
    else
        for (( i=0; i<$5-1; i++ ))
        do
        ./run.sh $1 &
        done
        ./run.sh $1
    fi
fi
if [!-d /home/mapigaglio/result]; then
    mkdir -p /home/mapigaglio/result;
fi;
mkdir /home/mapigaglio/result/$(date +%d-%m-%y-%H-%M)
cp *.csv /home/mapigaglio/result/$(date +%d-%m-%y-%H-%M)