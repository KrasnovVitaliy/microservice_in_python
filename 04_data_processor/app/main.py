import logging
import faust
import json
import config_loader as config_loader
import metrics
from prometheus_client import start_http_server

SERVICE_NAME = "data-processor"
config = config_loader.Config()

logging.basicConfig(
    level=logging.getLevelName(config.get(config_loader.LOGGING_LEVEL)),
    format=config.get(config_loader.LOGGING_FORMAT))

logger = logging.getLogger(__name__)

app = faust.App(SERVICE_NAME, broker=config.get(config_loader.KAFKA_BROKER), value_serializer='raw',
                web_host=config.get(config_loader.WEB_HOST), web_port=config.get(config_loader.WEB_PORT))
src_data_topic = app.topic(config.get(config_loader.SRC_DATA_TOPIC), partitions=8)
processed_data_topic = app.topic(config.get(config_loader.PROCESSED_DATA_TOPIC), partitions=8)


@app.agent(src_data_topic)
async def on_event(stream) -> None:
    async for msg_key, msg_value in stream.items():
        metrics.SRC_DATA_RECEIVED_CNT.inc()
        logger.info(f'Received new pair message {msg_value}')
        serialized_message = json.loads(msg_value)
        for pair_name, pair_value in serialized_message.items():
            logger.info(f"Extracted pair: {pair_name}: {pair_value}")
            metrics.PROCESSED_PAIRS_CNT.inc()
            await processed_data_topic.send(key=msg_key, value=json.dumps({pair_name: pair_value}).encode())
            metrics.PROCESSED_DATA_SENT_CNT.inc()

            yield msg_value


@app.task
async def on_started() -> None:
    logger.info('Starting prometheus server')
    start_http_server(port=config.get(config_loader.PROMETHEUS_PORT))
