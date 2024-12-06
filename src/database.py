import asyncio

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

from src.config import settings


engine = create_async_engine(settings.DB_URL)
