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


class ItemType(enum.Enum):
    crystal = "crystal"
    incubator = "incubator"
    battle_ticket = "battle ticket"
    skill = "skill"


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    num = Column(Integer, nullable=False)
    name = Column(String)
    description = Column(String)
    rarity = Column(Enum(ItemRarity))
    item_type = Column(Enum(ItemType))
    incubator_usages = Column(Integer)


class EquipmentEntry(Base):
    __tablename__ = "eqentries"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"))
    item = relationship("Item")
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User")


class HeroType(enum.Enum):
    normal = "normal"
    fighting = "fighting"
    flying = "flying"
    poison = "poison"
    ground = "ground"
    rock = "rock"
    bug = "bug"
    ghost = "ghost"
    steel = "steel"
    fire = "fire"
    water = "water"
    grass = "grass"
    electric = "electric"
    psychic = "psychic"
    ice = "ice"
    dragon = "dragon"
    dark = "dark"


class ExpGroup(enum.Enum):
    slow = "slow"
    medium_slow = "medium slow"
    fast = "fast"
    medium_fast = "medium fast"
    erratic = "erratic"
    fluctuating = "fluctuating"


class Hero(Base):
    __tablename__ = "heroes"
    id = Column(Integer, primary_key=True, index=True)
    num = Column(Integer, nullable=False)
    name = Column(String)
    title = Column(String)
    description = Column(String)
    base_hp = Column(Integer)
    base_attack = Column(Integer)
    base_defense = Column(Integer)
    base_speed = Column(Integer)
    base_special_defense = Column(Integer)
    base_special_attack = Column(Integer)
    rarity = Column(Enum(ItemRarity))
    hero_type = Column(Enum(HeroType))
    secondary_hero_type = Column(Enum(HeroType))
    exp_group = Column(Enum(ExpGroup))


class MoveCategory(enum.Enum):
    physical = "physical"
    special = "special"
    status = "status"


class StatusEffect(enum.Enum):
    poisoned = "poisoned"
    leech_seed = "leech seed"
    confused = "confused"
    asleep = "asleep"


class StageEffect(enum.Enum):
    accuracy = "accuracy"
    evasion = "evasion"
    attack = "attack"
    defense = "defense"
    special_attack = "special attack"
    special_defense = "special defense"
    speed = "speed"


class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    priority = Column(Integer)
    accuracy = Column(Integer)
    power = Column(Integer)
    max_usages = Column(Integer)
    crit_mod = Column(Integer)
    move_type = Column(Enum(HeroType))
    move_category = Column(Enum(MoveCategory))
    self_targetted = Column(Boolean)
    stage_effect = Column(Enum(StageEffect))
    mod = Column(Integer)
    secondary_stage_effect = Column(Enum(StageEffect))
    secondary_mod = Column(Integer)
    status_effect = Column(Enum(StatusEffect))
    item_id = Column(Integer, ForeignKey("items.id"))
    item = relationship("Item")


class SkillSet(Base):
    __tablename__ = "hero_skills"
    id = Column(Integer, primary_key=True, index=True)
    hero_id = Column(Integer, ForeignKey("user_heroes.id"))
    hero = relationship("UserHero")
    skill_1_id = Column(Integer, ForeignKey("skills.id"))
    skill_1 = relationship(
            "Skill",
            primaryjoin="Skill.id==SkillSet.skill_1_id"
            )
    usages_1 = Column(Integer)
    skill_2_id = Column(Integer, ForeignKey("skills.id"))
    skill_2 = relationship(
            "Skill",
            primaryjoin="Skill.id==SkillSet.skill_2_id"
            )
    usages_2 = Column(Integer)
    skill_3_id = Column(Integer, ForeignKey("skills.id"))
    skill_3 = relationship(
            "Skill",
            primaryjoin="Skill.id==SkillSet.skill_3_id"
            )
    usages_3 = Column(Integer)
    skill_4_id = Column(Integer, ForeignKey("skills.id"))
    skill_4 = relationship(
            "Skill",
            primaryjoin="Skill.id==SkillSet.skill_4_id"
            )
    usages_4 = Column(Integer)


class UserHero(Base):
    __tablename__ = "user_heroes"
    id = Column(Integer, primary_key=True, index=True)
    hp = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    speed = Column(Integer)
    special_attack = Column(Integer)
    special_defense = Column(Integer)
    incubated = Column(Boolean)
    fainted = Column(Boolean)
    poisoned = Column(Boolean)
    in_team = Column(Boolean)
    damage = Column(Integer)
    experience = Column(Integer)
    level = Column(Integer)
    hero_id = Column(Integer, ForeignKey("heroes.id"))
    hero = relationship("Hero")
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User")
    skillset = relationship("SkillSet", back_populates="hero", uselist=False)


class HeroMods(Base):
    __tablename__ = "hero_mods"
    id = Column(Integer, primary_key=True, index=True)
    accuracy = Column(Integer)
    evasion = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    special_attack = Column(Integer)
    special_defense = Column(Integer)
    speed = Column(Integer)
    leech_seed = Column(Boolean)


class Battle(Base):
    __tablename__ = "battles"
    id = Column(Integer, primary_key=True, index=True)
    turn = Column(Integer)
    enemies = Column(Integer)
    finished = Column(Boolean)
    hero_id = Column(Integer, ForeignKey("user_heroes.id"))
    hero = relationship("UserHero", primaryjoin="UserHero.id==Battle.hero_id")
    hero_mods_id = Column(Integer, ForeignKey("hero_mods.id"))
    hero_mods = relationship("HeroMods", primaryjoin="HeroMods.id==Battle.hero_mods_id")
    enemy_id = Column(Integer, ForeignKey("user_heroes.id"))
    enemy = relationship(
            "UserHero",
            primaryjoin="UserHero.id==Battle.enemy_id")
    enemy_mods_id = Column(Integer, ForeignKey("hero_mods.id"))
    enemy_mods = relationship("HeroMods", primaryjoin="HeroMods.id==Battle.enemy_mods_id")
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


class Team(Base):
    __tablename__ = "user_teams"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
    hero_1_id = Column(Integer, ForeignKey("user_heroes.id"))
    hero_1 = relationship(
            "UserHero",
            primaryjoin="UserHero.id==Team.hero_1_id"
            )
    hero_2_id = Column(Integer, ForeignKey("user_heroes.id"))
    hero_2 = relationship(
            "UserHero",
            primaryjoin="UserHero.id==Team.hero_2_id"
            )
    hero_3_id = Column(Integer, ForeignKey("user_heroes.id"))
    hero_3 = relationship(
            "UserHero",
            primaryjoin="UserHero.id==Team.hero_3_id"
            )
    hero_4_id = Column(Integer, ForeignKey("user_heroes.id"))
    hero_4 = relationship(
            "UserHero",
            primaryjoin="UserHero.id==Team.hero_4_id"
            )
    hero_5_id = Column(Integer, ForeignKey("user_heroes.id"))
    hero_5 = relationship(
            "UserHero",
            primaryjoin="UserHero.id==Team.hero_5_id"
            )
    hero_6_id = Column(Integer, ForeignKey("user_heroes.id"))
    hero_6 = relationship(
            "UserHero",
            primaryjoin="UserHero.id==Team.hero_6_id"
            )


class SkillHero(Base):
    __tablename__ = "skill_hero_pairs"
    id = Column(Integer, primary_key=True, index=True)
    hero_id = Column(Integer, ForeignKey("heroes.id"))
    hero = relationship("Hero")
    skill_id = Column(Integer, ForeignKey("skills.id"))
    skill = relationship("Skill")
    autolearn = Column(Boolean)
    level = Column(Integer)
