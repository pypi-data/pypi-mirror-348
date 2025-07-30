import boto3
import json

## ONLY RETURNS THE VALUE - DEPRECATED
# def get_secrets(secret_name):
#     """
#     Get secrets from AWS Secrets Manager.

#     :param secret_name: str - The name of the secret to get.
#     :return: dict - The secrets.
#     """
#     region_name = "eu-west-1"

#     session = boto3.session.Session()
#     client = session.client(
#         service_name='secretsmanager',
#         region_name=region_name
#     )

#     get_secret_value_response = client.get_secret_value(
#         SecretId=secret_name
#     )['SecretString']

#     secrets = json.loads(get_secret_value_response)[secret_name]

#     return secrets


def get_secrets(secret_name):
    region_name = "eu-west-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )

    secrets = json.loads(get_secret_value_response['SecretString'])

    return secrets