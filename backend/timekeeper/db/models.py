from sqlalchemy import Column, Integer, String, DateTime, Time, Enum, ForeignKey, Boolean
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
