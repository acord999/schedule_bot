import asyncio
import datetime

from sqlalchemy import Integer, and_, func, text, insert, select, update
from sqlalchemy.orm import aliased
from database import sync_engine,  Base, async_engine
from models.models import metadata


def create_tables():
    async_engine.echo = True
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)
    async_engine.echo = True
