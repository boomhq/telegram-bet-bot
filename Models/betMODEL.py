import os

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class Match(Base):
    __tablename__ = "matches"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_unicode_ci",
    }
    id = Column(Integer, primary_key=True)
    title = Column(String(500))
    start_date = Column(DateTime)
    team1 = Column(String(50))
    team2 = Column(String(50))
    score1 = Column(Integer)
    score2 = Column(Integer)


class Ranking(Base):
    __tablename__ = "ranking"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_unicode_ci",
    }
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer)
    wins = Column(Integer, default=0)
    total = Column(Integer, default=0)


class Bet(Base):
    __tablename__ = "bets"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_unicode_ci",
    }
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer)
    match = Column(Integer)
    bet = Column(String(50))


class User(Base):
    __tablename__ = "users"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_unicode_ci",
    }
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer)
    telegram = Column(String(191))
    notify = Column(Integer)


schema = os.environ.get("BET_BOT_SCHEMA")
engine = create_engine(schema)
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()


def get_session():
    return session


def get_matches():
    return session.query(Match)


def get_bets():
    return session.query(Bet)


def get_ranking():
    return session.query(Ranking)


def get_users():
    return session.query(User)


def add(to_add):
    try:
        session.add(to_add)
        session.commit()
        return 1
    except Exception:
        return 0


def update():
    session.commit()


def delete(model, _filter):
    session.query(model).filter(_filter).delete()
    session.commit()
