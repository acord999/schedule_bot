import datetime
import sys

sys.path.append("/Users/acord999/PycharmProjects/Personal_schedule/src")
from utils.mubint_schedule_parser import get_schedule
from sqlalchemy import Integer, and_, func, text, insert, select, update, and_
from sqlalchemy.orm import aliased, Session
from database.database import sync_engine, session_factory
from models import metadata, DatesOrm, EventsCategoriesOrm, UsersOrm, EventsOrm

DEFAULT_CATEGORIES = {
    1: "lessons",
    2: "work",
    3: "driving"
}

def insert_new_date(new_date):
    with session_factory() as session:
        if not session.query(DatesOrm).filter(DatesOrm.date == new_date).first():
            new_date_obj = DatesOrm(date=new_date)
            session.add(new_date_obj)
            session.commit()


def set_events_categories(categories: dict):
    with session_factory() as session:
        if not session.query(EventsCategoriesOrm).all():
            for id_ in categories:
                new_category = EventsCategoriesOrm(title=DEFAULT_CATEGORIES[id_], description=None)
                session.add(new_category)
                session.commit()
        else:
            raise ValueError("Значение категорий уже заданы")


def set_new_user(name, lastname, edu_group, telegram_id, secret_key, email=None):
    with session_factory() as session:
        new_user = UsersOrm(name=name, lastname=lastname, edu_group=edu_group, telegram_id=telegram_id,
                            secret_key=secret_key, email=email)
        session.add(new_user)
        session.commit()


def update_schedule(schedule, category_id: int, user_id: int):
    new_events = []
    for day in schedule:
        insert_new_date(day["date"])
        with session_factory() as session:
            date_id = session.query(DatesOrm.id).filter(DatesOrm.date == day["date"]).one()[0]
        for event in day["events"].values():
            with session_factory() as session:
                new_event = EventsOrm(title=event["title"], time_start=event["time_start"],
                                      time_stop=event["time_stop"],
                                      user_id=user_id, event_category_id=category_id, date_id=date_id)
                q = session.query(EventsOrm).filter(and_(EventsOrm.title == new_event.title,
                                                         EventsOrm.time_start == new_event.time_start,
                                                         EventsOrm.time_stop == new_event.time_stop,
                                                         EventsOrm.date_id == new_event.date_id,
                                                         EventsOrm.event_category_id == new_event.event_category_id)).first()
                if q is None:
                    session.add(new_event)
                    session.commit()
                    new_events.append({"date": day["date"], "new_event": event})
    return new_events


if __name__ == "__main__":
    e_sched = get_schedule("22-ИБ111", amount_days=31)
    print(update_schedule(e_sched, category_id=1, user_id=1))
    # set_new_user(*EFREM_USER_DATA)
    # set_events_categories(DEFAULT_CATEGORIES)
