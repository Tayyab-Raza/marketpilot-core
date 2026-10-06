from app.core.config import settings
from app.providers.upstox import UpstoxProvider
from app.providers.marketstack import MarketstackProvider

def get_provider(name: str | None = None):
    name = name or settings.primary_provider
    if name == "upstox": return UpstoxProvider()
    if name == "marketstack": return MarketstackProvider()
    raise ValueError(f"Unknown provider: {name}")
