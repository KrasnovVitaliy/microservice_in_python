from prometheus_client import Counter

REQUEST_CNT = Counter('request', 'Sent request count')
SUCCESS_RESPONSE_CNT = Counter('success_response', 'Received response with valid data')
ERROR_RESPONSE_CNT = Counter('error_response', 'Received response with error count')
