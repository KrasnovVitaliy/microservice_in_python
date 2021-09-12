import logging
import faust
import json
import config_loader as config_loader
import metrics
from prometheus_client import start_http_server
from db import DB

SERVICE_NAME = "db-loader"
config = config_loader.Config()

logging.basicConfig(
    level=logging.getLevelName(config.get(config_loader.LOGGING_LEVEL)),
    format=config.get(config_loader.LOGGING_FORMAT))

logger = logging.getLogger(__name__)

app = faust.App(SERVICE_NAME, broker=config.get(config_loader.KAFKA_BROKER), value_serializer='raw',
                web_host=config.get(config_loader.WEB_HOST), web_port=config.get(config_loader.WEB_PORT))
average_changelog_topic = app.topic(config.get(config_loader.AVERAGE_CHANGELOG_TOPIC), partitions=8)
processed_data_topic = app.topic(config.get(config_loader.PROCESSED_DATA_TOPIC), partitions=8)

db = DB()


@app.agent(average_changelog_topic)
async def on_average_event(stream) -> None:
    metrics.AVERAGE_TOPIC_RECEIVED_CNT.inc()
    async for msg_key, msg_value in stream.items():
        logger.info(f'Received new average message {msg_key}, {msg_value}')
        serialized_message = json.loads(msg_value)
        await db.save_average(pair_name=msg_key.decode(), value=serialized_message['average'])


@app.agent(processed_data_topic)
async def on_processed_data_event(stream) -> None:
    metrics.PROCESSED_DATA_RECEIVED_CNT.inc()
    async for msg_key, msg_value in stream.items():
        logger.info(f'Received new pair message {msg_key}, {msg_value}')
        serialized_message = json.loads(msg_value)
        for pair_name, pair_value in serialized_message.items():
            await db.save_currency(pair_name=pair_name, value=pair_value)


@app.task
async def on_started() -> None:
    logger.info('Starting prometheus server')
    start_http_server(port=config.get(config_loader.PROMETHEUS_PORT))
