#!/bin/sh

set -ev

# these could all be environment variables:
USER="ubuntu"
SSH="ssh $USER@$SERVER_IP_ADDRESS"
APP_NAME=geo

PULL="git pull"
CHECKOUT="git checkout master"
BUILD="docker-compose -f docker-compose-prod.yml build"
PUSH="docker-compose -f docker-compose-prod.yml push"
STACK_DEPLOY="docker stack deploy -c docker-compose-prod.yml $APP_NAME"

#ssh -i ./deploy_key $USER@$SERVER_IP_ADDRESS pwd

ssh -i ./deploy_key -t -t $USER@$SERVER_IP_ADDRESS << EOF
  cd Geo
  $PULL
  $CHECKOUT
  $BUILD
  $PUSH
  $STACK_DEPLOY
  exit
EOF
