from uuid import UUID

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotBattleClientSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BOT_BATTLE_")
    cgi_url: str = Field(default="http://localhost:9811")
    game_id: UUID = Field(default=...)
    player_count: int = Field(default=...)
