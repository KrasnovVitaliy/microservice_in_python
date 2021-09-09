from prometheus_client import Counter

SRC_DATA_RECEIVED_CNT = Counter('src_data_received', 'The number of messages received from src-data topic')
PROCESSED_PAIRS_CNT = Counter('processed_pairs', 'The number of processed currency pairs')
PROCESSED_DATA_SENT_CNT = Counter('processed_data_sent', 'The number of messages sent to processed-data topic')
