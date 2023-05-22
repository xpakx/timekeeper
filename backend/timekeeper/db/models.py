from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
import enum


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)


class Timer(Base):
    __tablename__ = "timers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    duration_s = Column(Integer)
    instances = relationship("TimerInstance", back_populates="timer")


class TimerState(enum.Enum):
    running = 1
    finished = 2
    cancelled = 3
    failed = 4


class TimerInstance(Base):
    __tablename__ = "timer_instances"
    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    state = Column(Enum(TimerState))
    timer_id = Column(Integer, ForeignKey("timers.id"))
    timer = relationship("Timer", back_populates="instances")
