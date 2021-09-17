# Demo project microservice in python with Kafka and Faust

### Description
This is a demo project to represent a way to implement Python microservices with Kafka and Faust library.

## Project structure
### 01_infrastructure
[01_infrastructure](./01_infrastructure) - contains basic infrastructure described in docker-compose.yml file. Contains all infrastructure services such as:
* Kafka
* Zookeeper
* Postgres
* PgAdmin
* Prometheus
* Grafana

In [.env](./01_infrastructure/.env) file described all versions and ports required for the docker-compose.yml
The [grafana](./01_infrastructure/grafana) folder contains preconfigured dashboards and datasources required for this docker-compose.yml
The [prometheus](./01_infrastructure/prometheus) folder contains preconfigured services to collect metrics by the prometheus service, required for this docker-compose.yml 

## 02_demo_server
[02_demo_server](./02_demo_server) - contains demo server [app](02_demo_server/app) and [Dockerfile](02_demo_server/Dockerfile) required to build it as docker image. The demo server produce random test data needed for demo.
 
## 03_data_requester
[03_data_requester](./03_data_requester) - contains data request microservice [app](03_data_requester/app) and [Dockerfile](03_data_requester/Dockerfile) required to build it as docker image. The data requester service request data from demo server and send it to a Kafka.

## 04_data_processor
[04_data_processor](./04_data_processor) - contains data processor microservice [app](04_data_processor/app) and [Dockerfile](04_data_processor/Dockerfile) required to build it as docker image. The data processor service read messages received from data requester via Kafka. Split data and upload to Kafka.

## 05_data_aggregator
[05_data_aggregator](./05_data_aggregator) - contains data aggregator microservice [app](05_data_aggregator/app) and [Dockerfile](05_data_aggregator/Dockerfile) required to build it as docker image. The data aggregator service read messages received from data processor via Kafka. And calculate average value for last 10 responses.

## 06_db_loader
[06_db_loader](./06_db_loader) - contains db loader microservice [app](06_db_loader/app) and [Dockerfile](06_db_loader/Dockerfile) required to build it as docker image. The db loader service read messages from data processor and data aggregator services and store this data to Postgres DB. 

## 07_api_gateway
[07_api_gateway](./07_api_gateway) - contains API gateway microservice [app](07_api_gateway/app) and [Dockerfile](07_api_gateway/Dockerfile) required to build it as docker image. The api gateway service provide HTTP endpoints to request data from Postgres DB.

## docker-compose.yml
[docker-compose.yml](./docker-compose.yml) - contains all services and infrastructure in one. 

## Requirements 
* Python 3.8+
* Docker 20.10.8
* Docker-compose 1.29.2

## Python requirements
* asyncio==3.4.3
* aiohttp==3.7.4.post0
* uvloop==0.15.3
* fastapi==0.68.0
* uvicorn[standard]==0.14.0
* starlette==0.14.2
* starlette-exporter==0.10.0
* configloader==1.0.1
* prometheus-client===0.11.0
* PyYAML==5.4.1
* asyncpg==0.23.0
* SQLAlchemy==1.4.0
* faust[rocksdb, fast, uvloop]==1.10.4

