# /bin/bash
echo "Deploying Telegram Handler"
echo -e "\n"

env=$1;

if [ -z $1 ]; then
    env="dev"
fi

cp ../../../../enviroments.json enviroments.json

TELEGRAM_TOKEN=$(sed -n 's/.*"TELEGRAM_TOKEN": "\(.*\)",/\1/p' enviroments.json)
TENANT=$(sed -n 's/.*"TENANT": "\(.*\)",/\1/p' enviroments.json | tr '[:upper:]' '[:lower:]')

IFS=':' # hyphen (-) is set as delimiter
read -ra SPLIT_TOKEN <<< "$TELEGRAM_TOKEN" # telegramToken is read into an array as tokens separated by IFS

sed -i "s/\${telegramTokenId}/${SPLIT_TOKEN[0]}/" serverless.yml;
sed -i "s/\${tenant}/$TENANT/" serverless.yml;

serverless deploy --stage $env -v -r us-east-1;

sed -i "s/${SPLIT_TOKEN[0]}/\${telegramTokenId}/" serverless.yml;
sed -i "s/$TENANT/\${tenant}/" serverless.yml;

rm enviroments.json

echo -e "\n"
echo "Deploy Finish"
echo -e "\n"