from typing import Dict

import boto3

from app.utils.config import load_config
from app.utils.logger import get_logger

logger = get_logger(__name__)
config_vars = load_config()


def create_boto3_client(
    service_name: str, settings: Dict = config_vars
) -> boto3.client:
    """creates a client based on the specific service name like bedrock-runtime"""
    try:
        logger.info(
            f"Criando cliente {service_name.upper()} para a região: {settings.get('AWS_BEDROCK_REGION', None)}..."
        )
        client = boto3.client(
            service_name,
            region_name=settings.get("AWS_BEDROCK_REGION", None),
            aws_access_key_id=settings.get("AWS_ACCESS_KEY_ID", None),
            aws_secret_access_key=settings.get("AWS_SECRET_ACCESS_KEY", None),
        )
        logger.info(f"Cliente {service_name.upper()} criado com sucesso.")
        return client
    except Exception as e:
        logger.critical(f"Não foi possível criar o cliente {service_name.upper()}: {e}")
        raise
