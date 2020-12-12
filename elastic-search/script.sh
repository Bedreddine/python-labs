#!/bin/bash

# check if the script has the need privileges
if [[ $(/usr/bin/id -u) -ne 0 ]]; then
    echo "$0 is not running as root. Try using sudo."
    exit
fi

CONTAINER_NAME="elasticsearch"
NETWORK_DRIVER_NAME="elastic-net"

function checkNetworkDriver() {
    NET_DRIVER=$(docker network ls --format='{{.Name}}' | grep $NETWORK_DRIVER_NAME) 
    if [ ! "$NET_DRIVER" == "$NETWORK_DRIVER_NAME" ]; then
        docker network create elastic-net
        echo "init network driver ["$NETWORK_DRIVER_NAME"] ..."
    else
        echo "network driver with name [$NETWORK_DRIVER_NAME] already exists ... skiping !!!"
    fi
}

function createOrSkipContainerCreation() {
    CONTAINER=$(docker ps --format='{{.Names}}' | grep $CONTAINER_NAME) 
    if [ ! "$CONTAINER" == "$CONTAINER_NAME" ]; then
        docker run --name "$CONTAINER_NAME" --net "$NETWORK_DRIVER_NAME" -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -d \
            --health-cmd='curl -f http://localhost:9200 || exit 1' --health-interval=2s --health-retries=5 --health-start-period=30s \
            elasticsearch:7.9.3
    else 
        echo "container with name [$CONTAINER_NAME] already exists ... skiping !!!"    
    fi
}

function getStatus() {
    sleep 2
    CONTAINER_STATE=$(docker inspect --format='{{.State.Health.Status}}' $CONTAINER_NAME)
    echo "$(date) ["$CONTAINER_NAME"] HEALTH STATUS: ["$CONTAINER_STATE"] "
}

function installDocker() {
    echo -e "docker is not installed ... Patient !! installing docker ..."
    apt-get update -y
    apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg-agent \
        software-properties-common

    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -

    add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"

    apt-get update -y

    apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose

    groupadd docker
    usermod -aG docker $(whoami)
}

# check docker existance
if [ ! -d /etc/docker ] ; then
    installDocker
else
    echo -e "GOOD ... docker is already installed"
fi
checkNetworkDriver
createOrSkipContainerCreation
getStatus