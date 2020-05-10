#!/bin/sh

set -ev

# these could all be environment variables:
USER="ubuntu"
SSH="ssh $USER@$SERVER_IP_ADDRESS"
APP_NAME=Geo

PULL="git pull"
CHECKOUT="git checkout master"
BUILD_BACKED="docker build -t $APP_NAME-backend backend"
BUILD_NGINX="docker build -f nginx/Dockerfile  -t $APP_NAME-nginx ."
STACK_DEPLOY="docker stack deploy -c docker-compose-prod.yml $APP_NAME"

#ssh -i ./deploy_key $USER@$SERVER_IP_ADDRESS pwd

ssh -i ./deploy_key -t -t $USER@$SERVER_IP_ADDRESS << EOF
  cd $APP_NAME
  $PULL
  $CHECKOUT
  $BUILD_BACKED
  $BUILD_NGINX
  $STACK_DEPLOY
EOF

exit 0