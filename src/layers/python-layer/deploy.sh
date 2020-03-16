# /bin/bash
echo "Deploying Python Layer"
echo -e "\n"

env=$1;

if [ -z $1 ]; then
    env="dev"
fi

cp ../../../environment.json environment.json

cd layer

cp ../environment.json environment.json

cd python/lib/python3.7/site-packages

cp ../../../../environment.json environment.json

cd ../../../../..

TENANT=$(sed -n 's/.*"TENANT": "\(.*\)",/\1/p' environment.json | tr '[:upper:]' '[:lower:]')

sed -i "s/\${tenant}/$TENANT/" serverless.yml;

serverless deploy --stage $env -v -r us-east-1;

sed -i "s/$TENANT/\${tenant}/" serverless.yml;

rm layer/python/lib/python3.7/site-packages/environment.json 

rm layer/environment.json

rm environment.json

echo -e "\n"
echo "Deploy Finish"
echo -e "\n"

cd ../..

cd lambdas

cd help
bash deploy.sh $env

cd ..

cd count-characters
bash deploy.sh $env

cd ..

cd alphabet-number
bash deploy.sh $env

cd ..

cd number-alphabet
bash deploy.sh $env

cd ..

cd get-initials
bash deploy.sh $env

cd ..

cd new-user-conversation

bash deploy.sh $env

cd ..

cd telegram
cd telegram-downloader
bash deploy.sh $env