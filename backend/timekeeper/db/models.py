from sqlalchemy import (
        Column,
        Integer,
        String,
        DateTime,
        Enum,
        ForeignKey,
        Boolean)
from sqlalchemy.orm import relationship
from .base import Base
import enum


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    timers = relationship("Timer", back_populates="owner")


class TimerDifficulty(enum.Enum):
    trivial = "trivial"
    easy = "easy"
    medium = "medium"
    hard = "hard"


class Timer(Base):
    __tablename__ = "timers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    duration_s = Column(Integer)
    deleted = Column(Boolean)
    autofinish = Column(Boolean)
    rewarded = Column(Boolean)
    difficulty = Column(Enum(TimerDifficulty))
    instances = relationship("TimerInstance", back_populates="timer")
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="timers")


class TimerState(enum.Enum):
    running = "running"
    finished = "finished"
    cancelled = "cancelled"
    failed = "failed"


class TimerInstance(Base):
    __tablename__ = "timer_instances"
    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime(timezone=True))
    reward_time = Column(Integer)
    rewarded = Column(Boolean)
    end_time = Column(DateTime(timezone=True))
    state = Column(Enum(TimerState))
    timer_id = Column(Integer, ForeignKey("timers.id"))
    timer = relationship("Timer", back_populates="instances")
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User")


class Points(Base):
    __tablename__ = "points"
    id = Column(Integer, primary_key=True, index=True)
    points = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")


class ItemRarity(enum.Enum):
    common = "common"
    uncommon = "uncommon"
    rare = "rare"


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    num = Column(Integer, nullable=False)
    name = Column(String)
    description = Column(String)
    rarity = Column(Enum(ItemRarity))


class EquipmentEntry(Base):
    __tablename__ = "eqentries"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"))
    item = relationship("Item")
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User")


class HeroType(enum.Enum):
    fire = "fire"
    steam = "steam"
    water = "water"
    air = "air"
    earth = "earth"
    dark = "dark"
    light = "light"
    celestial = "celestial"


class Hero(Base):
    __tablename__ = "heroes"
    id = Column(Integer, primary_key=True, index=True)
    num = Column(Integer, nullable=False)
    name = Column(String)
    description = Column(String)
    base_hp = Column(Integer)
    base_attack = Column(Integer)
    base_defense = Column(Integer)
    base_speed = Column(Integer)
    base_special = Column(Integer)
    rarity = Column(Enum(ItemRarity))
    hero_type = Column(Enum(HeroType))
    secondary_hero_type = Column(Enum(HeroType))


class UserHero(Base):
    __tablename__ = "user_heroes"
    id = Column(Integer, primary_key=True, index=True)
    hp = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    speed = Column(Integer)
    special = Column(Integer)
    incubated = Column(Boolean)
    damage = Column(Integer)
    experience = Column(Integer)
    hero_id = Column(Integer, ForeignKey("heroes.id"))
    hero = relationship("Hero")
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User")


class Battle(Base):
    __tablename__ = "battles"
    id = Column(Integer, primary_key=True, index=True)
    turn = Column(Integer)
    player_turn = Column(Boolean)
    hero_hp = Column(Integer)
    enemy_hp = Column(Integer)
    hero_id = Column(Integer, ForeignKey("user_heroes.id"))
    hero = relationship("UserHero", primaryjoin="UserHero.id==Battle.hero_id")
    enemy_id = Column(Integer, ForeignKey("user_heroes.id"))
    enemy = relationship(
            "UserHero",
            primaryjoin="UserHero.id==Battle.enemy_id")
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User")


class Incubator(Base):
    __tablename__ = "incubators"
    id = Column(Integer, primary_key=True, index=True)
    permanent = Column(Boolean)
    broken = Column(Boolean)
    initial_points = Column(Integer)
    usages = Column(Integer)
    hero_id = Column(Integer, ForeignKey("user_heroes.id"))
    hero = relationship("UserHero")
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User")
