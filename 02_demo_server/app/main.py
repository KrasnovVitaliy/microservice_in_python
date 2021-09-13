import uvicorn
import logging

from fastapi import FastAPI
from starlette_exporter import PrometheusMiddleware, handle_metrics
import config_loader as config_loader
import routes

config = config_loader.Config()

logging.basicConfig(
    level=logging.getLevelName(config.get(config_loader.LOGGING_LEVEL)),
    format=config.get(config_loader.LOGGING_FORMAT))

logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="Metrics Collector")
app.include_router(routes.router)
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

if __name__ == '__main__':
    logger.info("Starting server")
    logger.warning("This is debug server")
    logger.warning("To start server use command: uvicorn main:app --reload")
    uvicorn.run(app, port=config.get(config_loader.WEB_PORT), host=config.get(config_loader.WEB_HOST))
