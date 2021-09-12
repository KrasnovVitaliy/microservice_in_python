from prometheus_client import Counter
GET_CURRENCIES_CNT = Counter("get_currencies", "The number of get currencies request")
GET_AVERAGE_CNT = Counter("get_average", "The number of get average request")
