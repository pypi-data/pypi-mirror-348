import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from typing import Literal
from trilla_lib.infra.sentry.settings import sentry_config



def init_sentry(
    plugins: set[Literal['fastapi', 'sqlalchemy', 'redis', 'celery']],
) -> None:

    if not sentry_config.enabled:
        return

    plugins_map = {
        'fastapi': FastApiIntegration(),
        'sqlalchemy': SqlalchemyIntegration(),
        'redis': RedisIntegration(),
        'celery': CeleryIntegration(),
    }

    sentry_sdk.init(
        dsn=sentry_config.dsn,
        environment=sentry_config.environment,
        release=sentry_config.release,
        traces_sample_rate=sentry_config.traces_sample_rate,
        integrations=[
            plugin
            for plugin_key, plugin in plugins_map.items()
            if plugin_key in plugins
        ],
        debug=sentry_config.debug,
    )
