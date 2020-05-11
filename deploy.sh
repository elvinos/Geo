#!/bin/sh

set -ev

# these could all be environment variables:
USER="ubuntu"
SSH="ssh $USER@$SERVER_IP_ADDRESS"
APP_NAME=geo

PULL="git pull"
CHECKOUT="git checkout master"
BUILD="sudo docker-compose -f docker-compose-prod.yml build"
PUSH="sudo docker-compose -f docker-compose-prod.yml push"
STACK_DEPLOY="sudo docker stack deploy -c docker-compose-prod.yml $APP_NAME"

#ssh -i ./deploy_key $USER@$SERVER_IP_ADDRESS pwd

ssh -i ./deploy_key -t -t $USER@$SERVER_IP_ADDRESS << EOF
  cd $APP_NAME
  $PULL
  $CHECKOUT
  $BUILD
  $PUSH
  $STACK_DEPLOY
EOF

exit 0