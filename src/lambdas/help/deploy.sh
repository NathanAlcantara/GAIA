# /bin/bash
echo "Deploying lambda that  get help to the user"
echo -e "\n"

env=$1;

if [ -z $1 ]; then
    env="dev"
fi

cp ../../../docs/commands/commands.json commands.json

cp ../../../environment.json environment.json

TENANT=$(sed -n 's/.*"TENANT": "\(.*\)",/\1/p' environment.json | tr '[:upper:]' '[:lower:]')

sed -i "s/\${tenant}/$TENANT/" serverless.yml;

serverless deploy --stage $env -v -r us-east-1;

sed -i "s/$TENANT/\${tenant}/" serverless.yml;

rm environment.json

rm commands.json

echo -e "\n"
echo "Deploy Finish"
echo -e "\n"