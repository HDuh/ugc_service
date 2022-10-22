import os
from logging import config as logging_config

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

from .logger import LOGGING

__all__ = (
    'KAFKA_CONSUMER_CONFIG',
    'CH_CONFIG',
    'APP_CONFIG'
)

load_dotenv()
# Применяем настройки логирования
logging_config.dictConfig(LOGGING)
# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AppConfig(BaseSettings):
    BATCH_SIZE: int = Field(..., env='BATCH_SIZE')


class KafkaConsumerSettings(BaseSettings):
    KAFKA_HOST: str = Field(..., env='KAFKA_BOOTSTRAP_SERVERS')
    TOPICS: list = Field(..., env='EVENT_TYPES')
    GROUP_ID: str = Field(..., env='KAFKA_GROUP_ID')


class ClickHouseSettings(BaseSettings):
    CH_HOST: str = Field(..., env='CH_HOST')
    CH_DB: str = Field(..., env='CH_DB')
    TABLES: list = Field(..., env='EVENT_TYPES')


KAFKA_CONSUMER_CONFIG = KafkaConsumerSettings()
CH_CONFIG = ClickHouseSettings()
APP_CONFIG = AppConfig()