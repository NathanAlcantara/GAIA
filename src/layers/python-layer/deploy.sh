# /bin/bash
echo "Deploying Python Layer"
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

cd count-characteres
bash deploy.sh $env
