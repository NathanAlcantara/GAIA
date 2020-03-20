# /bin/bash
echo "Deploying Node Layer"
echo -e "\n"

env=$1;

if [ -z $1 ]; then
    env="dev"
fi

cp ../../../environment.json environment.json

cd layer

cp ../../../../environment.json environment.json

npm install

cd ..

TENANT=$(sed -n 's/.*"TENANT": "\(.*\)",/\1/p' environment.json | tr '[:upper:]' '[:lower:]')

sed -i "s/\${tenant}/$TENANT/" serverless.yml;

serverless deploy --stage $env -v -r us-east-1;

sed -i "s/$TENANT/\${tenant}/" serverless.yml;

rm layer/environment.json

rm environment.json

echo -e "\n"
echo "Deploy Finish"
echo -e "\n"

cd ../..

cd lambdas

cd dynamo-write
bash deploy.sh $env

cd ..

cd telegram

cd set-webhook
bash deploy.sh $env

cd ..

cd context-read
bash deploy.sh $env

cd ..

cd handler
bash deploy.sh $env

cd ..

cd command
bash deploy.sh $env

cd ..

cd response
bash deploy.sh $env
