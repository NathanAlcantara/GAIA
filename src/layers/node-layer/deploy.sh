# /bin/bash
echo "Deploying Node Layer"
echo -e "\n"

env=$1;

if [ -z $1 ]; then
    env="dev"
fi

cp ../../../enviroments.json enviroments.json

cd layer

cp ../../../../enviroments.json enviroments.json

npm install

cd ..

TENANT=$(sed -n 's/.*"TENANT": "\(.*\)",/\1/p' enviroments.json | tr '[:upper:]' '[:lower:]')

sed -i "s/\${tenant}/$TENANT/" serverless.yml;

serverless deploy --stage $env -v -r us-east-1;

sed -i "s/$TENANT/\${tenant}/" serverless.yml;

rm layer/enviroments.json

rm enviroments.json

echo -e "\n"
echo "Deploy Finish"
echo -e "\n"

cd ../..

cd lambdas

cd telegram

cd set-webhook
bash deploy.sh $env

cd ..

cd telegram-handler
bash deploy.sh $env

cd ..

cd telegram-response
bash deploy.sh $env
