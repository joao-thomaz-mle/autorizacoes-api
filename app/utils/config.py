import os
from dataclasses import dataclass, field
from typing import Dict


def load_config():
    return {
        "ENVIRONMENT": os.getenv("ENVIRONMENT", "hml"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "hml"),
        "DEBUG": os.getenv("DEBUG", "false"),
        "APP_VERSION": os.getenv("APP_VERSION", "0.1.0"),
        "APP_TITLE": os.getenv("APP_TITLE", "Carteirinha API"),
        "APP_DESCRIPTION": os.getenv("APP_DESCRIPTION", "Carteirinha API"),
        "AWS_BEDROCK_REGION": os.getenv("AWS_BEDROCK_REGION", "us-east-1"),
        "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
        "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "ORACLE_USER": os.getenv("ORACLE_USER"),
        "ORACLE_PASSWORD": os.getenv("ORACLE_PASSWORD"),
        "ORACLE_DSN": os.getenv("ORACLE_DSN"),
        "ORACLE_INSTANT_CLIENT_PATH": os.getenv("ORACLE_INSTANT_CLIENT_PATH"),
        "MARIADB_USER": os.getenv("MARIADB_USER"),
        "MARIADB_PASSWORD": os.getenv("MARIADB_PASSWORD"),
        "MARIADB_HOST": os.getenv("MARIADB_HOST"),
        "MARIADB_PORT": os.getenv("MARIADB_PORT"),
        "MARIADB_DATABASE": os.getenv("MARIADB_DATABASE"),
    }


@dataclass
class AppConstants:
    BEDROCK_DEFAULT_MODEL_ID: str = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
    BEDROCK_DEFAULT_MODEL_VERSION: str = "bedrock-2023-05-31"
    DEFAULT_PROMPTS_DIR: str = "prompts/"
    S3_BUCKET_NAME: str = "agente-ai-carteirinha"
    S3_RESULTS_PREFIX: str = "resultados"
    S3_DEBUG_PREFIX: str = "debug"
    STREAMING: bool = False
    CACHE_PROMPT = "default"
    RETRIES: Dict[str, object] = field(
        default_factory=lambda: {"max_attempts": 3, "mode": "standard"}
    )
    CONNECTION_TIMEOUT: int = 5
    READ_TIMEOUT: int = 60
    TEMPERATURE: float = 1
    TOP_P: float = 0.95
    MAX_TOKENS: int = 4096
    BUDGET_TOKENS: int = 2048
