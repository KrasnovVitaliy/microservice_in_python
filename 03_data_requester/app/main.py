import uuid
import logging
import faust
import json
import config_loader as config_loader
import data_provider
import metrics
from prometheus_client import start_http_server

SERVICE_NAME = "data-requester"
config = config_loader.Config()

logging.basicConfig(
    level=logging.getLevelName(config.get(config_loader.LOGGING_LEVEL)),
    format=config.get(config_loader.LOGGING_FORMAT))

logger = logging.getLogger(__name__)

app = faust.App(SERVICE_NAME, broker=config.get(config_loader.KAFKA_BROKER), value_serializer='raw',
                web_host=config.get(config_loader.WEB_HOST), web_port=config.get(config_loader.WEB_PORT))
src_data_topic = app.topic(config.get(config_loader.SRC_DATA_TOPIC), partitions=8)


@app.timer(interval=1.0)
async def request_data() -> None:
    provider = data_provider.DataProvider(base_url=config.get(config_loader.BASE_URL))
    pairs = await provider.get_pairs()
    metrics.REQUEST_CNT.inc()
    logger.info(f"Received new pairs: {pairs}")
    if pairs:
        await src_data_topic.send(key=uuid.uuid1().bytes, value=json.dumps(pairs).encode())


@app.task
async def on_started() -> None:
    logger.info('Starting prometheus server')
    start_http_server(port=config.get(config_loader.PROMETHEUS_PORT))
