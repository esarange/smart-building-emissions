import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class DatabaseHandler:
    _instance = None
    _client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseHandler, cls).__new__(cls)
            # Initialize the client when the app is first started
            cls._initialize_client()
        return cls._instance

    def __init__(self):
        # Prevent re-initialization of client in existing instance
        if not hasattr(self, '_initialized'):
            self._initialized = True
    
    @classmethod
    def _initialize_client(cls):
        """Initialize the Supabase client"""
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
        
        cls._client = create_client(url, key)
    
    def get(self) -> Client:
        """Return the Supabase client instance"""
        if self._client is None:
            self._initialize_client()
        return self._client

    def insert(self, table: str, data: dict) -> dict:
        return self.get().table(table).insert(data).execute().data[0]
    
    def select(self, table: str, filters: dict = None) -> list:
        query = self.get().table(table).select('*')
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        return query.execute().data
    
    def update(self, table: str, id: int, data: dict) -> dict:
        return self.get().table(table).update(data).eq('id', id).execute().data[0]
    
    def delete(self, table: str, id: int) -> dict:
        return self.get().table(table).delete().eq('id', id).execute().data[0]