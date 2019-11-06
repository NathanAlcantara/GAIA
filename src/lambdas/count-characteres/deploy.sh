# /bin/bash
echo "Deploying lambda that count characteres"
echo -e "\n"

env=$1;

if [ -z $1 ]; then
    env="dev"
fi

cp ../../../enviroments.json enviroments.json

TENANT=$(sed -n 's/.*"TENANT": "\(.*\)",/\1/p' enviroments.json | tr '[:upper:]' '[:lower:]')

sed -i "s/\${tenant}/$TENANT/" serverless.yml;

serverless deploy --stage $env -v -r us-east-1;

sed -i "s/$TENANT/\${tenant}/" serverless.yml;

rm enviroments.json

echo -e "\n"
echo "Deploy Finish"
echo -e "\n"