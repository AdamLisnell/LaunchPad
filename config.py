import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class for the application."""
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # API configuration
    API_PREFIX: str = "/v1"
    
    # Database - MySQL with async driver
    # NOTE: Default credentials are for local development only.
    # In production, always use strong passwords and environment variables.
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "mysql+aiomysql://launchpaduser:launchpadpass@localhost:3306/launchpad"
    )
    
    # Logging
    LOG_LEVEL: str = "DEBUG" if ENVIRONMENT == "development" else "INFO"
    
    @classmethod
    def as_dict(cls) -> Dict[str, Any]:
        """Returns the configuration as a dictionary."""
        return {
            key: value
            for key, value in vars(cls).items()
            if not key.startswith("__") and not callable(value)
        }


config = Config()