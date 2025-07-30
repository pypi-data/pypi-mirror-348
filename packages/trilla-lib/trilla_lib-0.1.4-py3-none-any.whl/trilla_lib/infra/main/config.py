import os

from pydantic import BaseSettings
from yarl import URL


class MainConfig(BaseSettings):

    host: str = 'main_app'
    port: int = 8000
    api_path: str = 'main'

    @property
    def url(self) -> URL:
        return URL.build(scheme='http', host=self.host, port=self.port) / self.api_path

    @property
    def auth_url(self) -> URL:
        domain_name = os.getenv("DOMAIN_NAME")
        deploy_env = os.getenv("DEPLOY_ENV", None)
        scheme = 'https' if deploy_env else 'http'
        return URL.build(scheme=scheme, host=domain_name, port=443) / "main/oauth/token"


    class Config:
        env_prefix = "MAIN_"

