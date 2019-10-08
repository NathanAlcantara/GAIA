# /bin/bash

name=nathan;
serverlessUser=nathanalcantara;
telegramToken=817872692:AAFvPb4n_7hIbeUtnb1X1vRSAaB94b_eyoI;

popd;

sed -i "s/\${telegramToken}/$telegramToken/" serverless.yml;
sed -i "s/\${org}/$serverlessUser/" serverless.yml;
sed -i "s/\${app}/$name/" serverless.yml;

serverless deploy --stage dev -v -r us-east-1;

sed -i "s/$telegramToken/\${telegramToken}/" serverless.yml;
sed -i "s/$serverlessUser/\${org}/" serverless.yml;
sed -i "s/$name/\${app}/" serverless.yml;

echo 