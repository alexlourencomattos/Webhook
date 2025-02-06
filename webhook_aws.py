import json
import boto3
import base64

# Nome do bucket onde os arquivos serão armazenados
BUCKET_NAME = "seu-bucket-s3"

# Cliente S3 da AWS
s3 = boto3.client("s3")

def lambda_handler(event, context):
    try:
        # Verifica se a requisição tem um corpo (body)
        if "body" not in event:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Requisição inválida: Nenhum dado recebido."})
            }

        # Obtém os dados do evento
        body = json.loads(event["body"])

        # ONS envia arquivos binários? Se sim, deve ser base64
        if "file" not in body or "filename" not in body:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Formato inválido: 'file' e 'filename' são obrigatórios."})
            }

        # Decodifica o arquivo recebido (base64 -> binário)
        file_content = base64.b64decode(body["file"])
        filename = body["filename"]

        # Nome do arquivo no S3
        s3_key = f"arquivos_ons/{filename}"

        # Upload do arquivo para o S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=file_content
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Arquivo recebido e salvo no S3.",
                "file_path": f"s3://{BUCKET_NAME}/{s3_key}"
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Erro no processamento: {str(e)}"})
        }
