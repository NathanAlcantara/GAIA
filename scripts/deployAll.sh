# /bin/bash

env=$1;

if [ -z $1 ]; then
    env="dev"
fi

echo "The magic begins!"

cd src

cd layers

cd node-layer
bash deploy.sh $env