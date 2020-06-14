#!/bin/sh

set -ev

# these could all be environment variables:
USER="ubuntu"
SSH="ssh $USER@$SERVER_IP_ADDRESS"
APP_NAME=geo

PULL="git pull"
CHECKOUT="git checkout master"
PRUNE="docker system prune --volumes -f"
BUILD="docker-compose -f docker-compose-server.yml build"
STACK_DEPLOY="docker stack deploy -c docker-compose-server.yml $APP_NAME"

ssh -i ./deploy_key -t -t $USER@$SERVER_IP_ADDRESS << EOF
  cd Geo
  $PULL
  $CHECKOUT
  $PRUNE
  $BUILD
  $STACK_DEPLOY
  exit
EOF