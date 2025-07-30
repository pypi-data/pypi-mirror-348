from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor


def instrument_fastapi(app):
    FastAPIInstrumentor().instrument_app(app)
    app.add_middleware(OpenTelemetryMiddleware)

def instrument_sqlalchemy(engine):
    SQLAlchemyInstrumentor().instrument(engine=engine)

def instrument_redis():
    RedisInstrumentor().instrument()

def instrument_httpx():
    HTTPXClientInstrumentor().instrument()
