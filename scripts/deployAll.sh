# /bin/bash

env=$1;

if [ -z $1 ]; then
    env="dev"
fi

echo "The magic begins!"
echo -e "\n"

cd src

cd api-gatway
bash deploy.sh $env

cd ..

cd layers

cd node-layer
bash deploy.sh $env