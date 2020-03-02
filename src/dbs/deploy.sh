# /bin/bash
echo "Deploying Databases"
echo -e "\n"

env=$1;

if [ -z $1 ]; then
    env="dev"
fi

serverless deploy --stage $env -v -r us-east-1;

echo -e "\n"
echo "Deploy Finish"
echo -e "\n"