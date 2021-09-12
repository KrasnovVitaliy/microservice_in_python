import logging
import faust
import json
import config_loader as config_loader
import metrics
from prometheus_client import start_http_server

SERVICE_NAME = "data-aggregator"
config = config_loader.Config()

logging.basicConfig(
    level=logging.getLevelName(config.get(config_loader.LOGGING_LEVEL)),
    format=config.get(config_loader.LOGGING_FORMAT))

logger = logging.getLogger(__name__)

app = faust.App(SERVICE_NAME, broker=config.get(config_loader.KAFKA_BROKER), value_serializer='raw',
                web_host=config.get(config_loader.WEB_HOST), web_port=config.get(config_loader.WEB_PORT))
processed_data_topic = app.topic(config.get(config_loader.PROCESSED_DATA_TOPIC), partitions=8)
aggregated_data_topic = app.topic(config.get(config_loader.AGGREGATED_DATA_TOPIC), partitions=8)

average_table = app.Table('average', default=dict)


@app.agent(processed_data_topic)
async def on_event(stream) -> None:
    async for msg_key, msg_value in stream.items():
        metrics.PROCESSED_DATA_RECEIVED_CNT.inc()
        logger.info(f'Received new processed data message {msg_value}')
        serialized_message = json.loads(msg_value)
        for pair_name, pair_value in serialized_message.items():
            average_value = average_table.get(pair_name, {})
            if average_value:
                average_value['history'].append(pair_value)
                average_value['history'] = average_value['history'][-10:]
                average_value['average'] = round(sum(average_value['history']) / len(average_value['history']), 2)
            else:
                average_value['history'] = [pair_value]
                average_value['average'] = pair_value
            logger.info(f"Aggregated value: {average_value}")
            average_table[pair_name] = average_value
            metrics.PAIRS_AVERAGE_AGGREGATED_CNT.inc()


@app.task
async def on_started() -> None:
    logger.info('Starting prometheus server')
    start_http_server(port=config.get(config_loader.PROMETHEUS_PORT))
