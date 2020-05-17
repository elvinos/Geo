#!/bin/sh

set -ev

# these could all be environment variables:
USER="ubuntu"
SSH="ssh $USER@$SERVER_IP_ADDRESS"
APP_NAME=geo

PULL="git pull"
CHECKOUT="git checkout master"
PRUNE="docker system prune --volumes -f"
GET_IMAGE="docker pull $DOCKER_USER/geo:geo-nginx"
TAG_IMAGE="docker tag $DOCKER_USER/geo:geo-nginx 127.0.0.1:5000/geo-nginx"
BUILD="docker-compose -f docker-compose-server.yml build"
PUSH="docker-compose -f docker-compose-server.yml push"
STACK_DEPLOY="docker stack deploy -c docker-compose-server.yml $APP_NAME"

#ssh -i ./deploy_key $USER@$SERVER_IP_ADDRESS pwd

ssh -i ./deploy_key -t -t $USER@$SERVER_IP_ADDRESS << EOF
  cd Geo
  $PULL
  $CHECKOUT
  $PRUNE
  $BUILD
  $PUSH
  $STACK_DEPLOY
  exit
EOF
