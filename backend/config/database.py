from supabase import create_client, Client
from backend.config import settings
from typing import Optional


class SupabaseClient:
    """Singleton Supabase client."""
    
    _instance: Optional[Client] = None
    
    @classmethod
    def get_client(cls) -> Client:
        """Get or create Supabase client instance."""
        if cls._instance is None:
            cls._instance = create_client(
                settings.supabase_url,
                settings.supabase_key
            )
        return cls._instance


def get_supabase() -> Client:
    """Dependency to get Supabase client."""
    return SupabaseClient.get_client()
