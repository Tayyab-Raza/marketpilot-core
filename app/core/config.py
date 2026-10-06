from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_env: str = "dev"
    database_url: str = "sqlite:///./marketpilot.db"
    marketstack_api_key: str | None = None
    upstox_access_token: str | None = None
    upstox_base_url: str = "https://api.upstox.com"
    marketstack_base_url: str = "https://api.marketstack.com/v1"
    primary_provider: str = "upstox"
    min_strategy_confidence: float = 0.58
    max_trap_score: float = 0.60
    default_risk_per_trade: float = 0.005

settings = Settings()
