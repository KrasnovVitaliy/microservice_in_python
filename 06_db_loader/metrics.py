from prometheus_client import Counter

AVERAGE_TOPIC_RECEIVED_CNT = Counter('average_topic_received',
                                     'The number of messages received from average-changelog topic')
PROCESSED_DATA_RECEIVED_CNT = Counter('processed_data_received',
                                      'The number of messages received from processed-data topic')
AVERAGE_TOPIC_SAVED_CNT = Counter('average_topic_saved',
                                  'The number of messages saved to db')
PROCESSED_DATA_SAVED_CNT = Counter('processed_data_saved',
                                   'The number of messages saved to db')
