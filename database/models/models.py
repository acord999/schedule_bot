import datetime

from sqlalchemy import MetaData, Table, Column, Integer, Date, BigInteger, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from typing import Annotated

# Создаем метаданные для таблиц
metadata = MetaData()

intpk = Annotated[int, mapped_column(primary_key=True)]


class DatesOrm(Base):
    """Даты на которые мы создаем события"""
    __tablename__ = "dates"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date] = mapped_column(unique=True)


class EventsCategoriesOrm(Base):
    __tablename__ = "events_categories"

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    edu_group: Mapped[str] = mapped_column(nullable=False)
    telegram_id: Mapped[str]
    email: Mapped[str] = mapped_column(nullable=True)
    secret_key: Mapped[str] = mapped_column(nullable=False)


class EventsOrm(Base):
    __tablename__ = "events"

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(nullable=False)
    time_start: Mapped[int] = mapped_column(nullable=False)
    time_stop: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_id: Mapped[int] = mapped_column(ForeignKey("dates.id"))
    event_category_id: Mapped[int] = mapped_column(ForeignKey("events_categories.id"))


# Описываем модели таблиц

#
# Даты на которые мы создаем события
dates = Table(
    "dates",
    metadata,
    Column("id", Integer, autoincrement=True, primary_key=True),
    Column("date", Date, nullable=False, unique=True),

)
events_categories = Table(
    "events_categories",
    metadata,
    Column("id", Integer, autoincrement=True, primary_key=True),
    Column("title", String, nullable=False),
    Column("description", String, nullable=True),

)

users = Table(
    "users",
    metadata,
    Column("id", Integer, autoincrement=True, primary_key=True),
    Column("name", String, nullable=False),
    Column("lastname", String, nullable=False),
    Column("edu_group", String),
    Column("telegram_id", String),
    Column("email", String),
    Column("secret_key", String, nullable=False),

)
events = Table(
    "events",
    metadata,
    Column("id", Integer, autoincrement=True, primary_key=True),
    Column("title", String, nullable=False),
    Column("time-start", BigInteger, nullable=False),
    Column("time-stop", BigInteger, nullable=False),
    Column("date_id", Integer, ForeignKey("dates.id")),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("event_category_id", Integer, ForeignKey("events_categories.id")),

)
