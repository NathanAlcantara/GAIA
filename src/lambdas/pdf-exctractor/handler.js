const AWS = require('aws-sdk');
const S3 =  new AWS.S3();


module.exports.main = async ({ Records: records }, context) => {
    try {
        await Promise.all(
            
            //É possível que o bucket emita um evento com a criação de mais de um documento
            records.map(async record => {
                let { key } = record.s3.object;

                // Quando o nome do arquivo possui espaços, o evento de criação que o 
                // bucket emite substitui esses espaços por '+'. Para fazer o download do arquivo
                // é necessário reinserir os espaços no nome.
                key = key.replace(/\+/g,' ');
                
                const pdf = await S3.getObject({
                    Bucket: process.env.bucket,
                    Key: key
                }).promise();

                console.log(pdf);
                
                // TO DO: Chamar textract
            })
        );
    } catch (err) {
        return err;
    }
    
};

