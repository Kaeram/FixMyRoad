from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings and configuration."""
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False
    )
    
    # Supabase Configuration
    supabase_url: str = "http://localhost:54321"
    supabase_key: str = "your_supabase_anon_key"
    
    # Application Configuration
    app_name: str = "FixMyRoad API"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # ML Model Configuration
    ml_model_confidence_threshold: float = 0.7


settings = Settings()
