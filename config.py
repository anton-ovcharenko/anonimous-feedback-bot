import os
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str

    @staticmethod
    def from_env():
        token = grt_env('BOT_TOKEN')
        return TgBot(token=token)


@dataclass
class Config:
    tg_bot: TgBot


def load_config() -> Config:
    config = Config(tg_bot=TgBot.from_env())
    print('Config was loaded')
    return config


def grt_env(variable_name: str) -> str:
    if variable_name not in os.environ:
        raise AssertionError(f"Environment variables '{variable_name}' is absent")
    return os.environ[variable_name]
