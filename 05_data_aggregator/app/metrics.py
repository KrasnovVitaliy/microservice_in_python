from prometheus_client import Counter

PROCESSED_DATA_RECEIVED_CNT = Counter('processed_data_received',
                                      'The number of messages received from processed-data topic')
PAIRS_AVERAGE_AGGREGATED_CNT = Counter('pairs_average_aggregated',
                                       'The number of calculated average for pairs')
