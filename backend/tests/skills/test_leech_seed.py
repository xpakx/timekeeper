from timekeeper.db.models import (
        ExpGroup,
        UserHero,
        Hero,
        User,
        Battle,
        HeroMods,
        HeroType,
        SkillSet,
        Skill,
        ItemRarity,
        MoveCategory,
        StatusEffect,
        Team)
from fastapi.testclient import TestClient
import pytest
from timekeeper.main import app
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from timekeeper.db.base import Base
from timekeeper.db.manager import get_db
from bcrypt import hashpw, gensalt
from timekeeper.services.user_service import create_token
from unittest.mock import patch, Mock

url = URL.create(
        "postgresql",
        "root",
        "password",
        "localhost",
        5432,
        "time_db_test")

engine = create_engine(
    url
)
TestingSessionLocal = sessionmaker(autocommit=False,
                                   autoflush=False,
                                   bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def create_user():
    db = TestingSessionLocal()
    password = hashpw("password".encode('utf-8'), gensalt()).decode()
    new_user = User(
            username="User",
            password=password
            )
    db.add(new_user)
    db.commit()
    db.close()


def create_user_with_username(username: str) -> int:
    db = TestingSessionLocal()
    password = hashpw("password".encode('utf-8'), gensalt()).decode()
    new_user = User(
            username=username,
            password=password
            )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return new_user.id


def create_user_and_return_id() -> int:
    return create_user_with_username("User")


def create_bulbasaur() -> int:
    db = TestingSessionLocal()
    item = Hero(
            num=1,
            name="Bulbasaur",
            title="Seed Pokemon",
            rarity=ItemRarity.uncommon,
            hero_type=HeroType.grass,
            secondary_hero_type=HeroType.poison,
            base_hp=45,
            base_attack=49,
            base_defense=49,
            base_speed=45,
            base_special_attack=65,
            base_special_defense=65,
            exp_group=ExpGroup.medium_slow,
            base_exp=64
            )
    db.add(item)
    db.commit()
    db.refresh(item)
    db.close()
    return item.id


def create_charmander() -> int:
    db = TestingSessionLocal()
    item = Hero(
            num=4,
            name="Charmander",
            title="Lizard Pokemon",
            rarity=ItemRarity.uncommon,
            hero_type=HeroType.fire,
            base_hp=39,
            base_attack=52,
            base_defense=43,
            base_speed=65,
            base_special_attack=60,
            base_special_defense=50,
            exp_group=ExpGroup.medium_slow,
            capture_rate=255,
            base_exp=62
            )
    db.add(item)
    db.commit()
    db.refresh(item)
    db.close()
    return item.id


def create_user_hero(hero_id: int, user_id: int, skillset: bool = True, fainted: bool = False):
    db = TestingSessionLocal()
    item = UserHero(
            hero_id=hero_id,
            owner_id=user_id,
            incubated=False,
            fainted=fainted,
            hp=0,
            attack=0,
            defense=0,
            speed=0,
            special_attack=0,
            special_defense=0,
            level=1,
            damage=0
            )
    db.add(item)
    if skillset:
        entry = SkillSet(
                hero=item,
                usages_1=0,
                usages_2=0,
                usages_3=0,
                usages_4=0
                )
        db.add(entry)
    db.commit()
    db.refresh(item)
    db.close()
    return item.id


def create_battle(
        user_id: int,
        hero_id: int,
        enemy_id: int,
        finished: bool = False):
    db = TestingSessionLocal()
    hero = HeroMods(
            accuracy=0,
            evasion=0,
            attack=0,
            defense=0,
            special_attack=0,
            special_defense=0,
            speed=0,
            flee_attempts=100)
    enemy = HeroMods(
            accuracy=0,
            evasion=0,
            attack=0,
            defense=0,
            special_attack=0,
            special_defense=0,
            speed=0,
            flee_attempts=100)
    item = Battle(
            turn=1,
            enemies=1,
            finished=finished,
            hero_id=hero_id,
            hero_mods=hero,
            enemy_id=enemy_id,
            enemy_mods=enemy,
            owner_id=user_id
            )
    db.add(item)
    db.commit()
    db.refresh(item)
    db.close()
    return item.id


def create_team(user_id: int) -> int:
    db = TestingSessionLocal()
    team = Team(
            user_id=user_id,
            )
    db.add(team)
    db.commit()
    db.refresh(team)
    db.close()
    return team.id


def add_to_team(team_id: int, hero_id: int, num: int):
    db = TestingSessionLocal()
    team = db.get(Team, team_id)
    if num == 1:
        team.hero_1_id = hero_id
    if num == 2:
        team.hero_2_id = hero_id
    if num == 3:
        team.hero_3_id = hero_id
    if num == 4:
        team.hero_4_id = hero_id
    if num == 5:
        team.hero_5_id = hero_id
    if num == 6:
        team.hero_6_id = hero_id
    db.commit()
    db.close()


def teach_skill(hero_id: int, skill_id: int, num: int = 1):
    db = TestingSessionLocal()
    skillset: SkillSet = db\
        .query(SkillSet)\
        .where(SkillSet.hero_id == hero_id)\
        .first()
    if num == 1:
        skillset.skill_1_id = skill_id
    if num == 2:
        skillset.skill_2_id = skill_id
    if num == 3:
        skillset.skill_3_id = skill_id
    if num == 4:
        skillset.skill_4_id = skill_id
    db.commit()
    db.close()


def create_leech_seed() -> int:
    db = TestingSessionLocal()
    skill = Skill(
            accuracy=90,
            power=0,
            priority=0,
            move_type=HeroType.grass,
            max_usages=10,
            name="Leech Seed",
            move_category=MoveCategory.status,
            status_effect=StatusEffect.leech_seed
            )
    db.add(skill)
    db.commit()
    db.refresh(skill)
    db.close()
    return skill.id


def get_token() -> str:
    return get_token_for(1)


def get_token_for(user_id: int) -> str:
    return create_token({"id": f"{user_id}", "sub": "User"})


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@patch('timekeeper.services.mechanics.battle_mech_service.test_accuracy', Mock(return_value=True))
def test_using_leech_seed(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    hero_id = create_user_hero(create_bulbasaur(), user_id)
    team_id = create_team(user_id)
    add_to_team(team_id, hero_id, 1)
    teach_skill(hero_id, create_leech_seed())
    enemy_id = create_user_hero(create_charmander(), None)
    battle_id = create_battle(user_id, hero_id, enemy_id)
    response = client.post(f"/battles/{battle_id}",
                           headers=headers,
                           json={
                               'move': 'skill',
                               'id': 1
                               }
                           )
    assert response.status_code == 200
    db = TestingSessionLocal()
    battle: Battle = db.query(Battle).where(Battle.id == battle_id).first()
    mods: HeroMods = battle.enemy_mods
    db.close()
    assert mods.leech_seed


@patch('timekeeper.services.mechanics.battle_mech_service.test_accuracy', Mock(return_value=False))
@patch('timekeeper.services.mechanics.battle_mech_service.calculate_if_player_moves_first', Mock(return_value=True))
def test_miss(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    hero_id = create_user_hero(create_bulbasaur(), user_id)
    team_id = create_team(user_id)
    add_to_team(team_id, hero_id, 1)
    teach_skill(hero_id, create_leech_seed())
    enemy_id = create_user_hero(create_charmander(), None)
    battle_id = create_battle(user_id, hero_id, enemy_id)
    response = client.post(f"/battles/{battle_id}",
                           headers=headers,
                           json={
                               'move': 'skill',
                               'id': 1
                               }
                           )
    assert response.status_code == 200
    result = response.json()
    assert result['turn']['first']['missed']
    db = TestingSessionLocal()
    battle: Battle = db.query(Battle).where(Battle.id == battle_id).first()
    mods: HeroMods = battle.enemy_mods
    db.close()
    assert not mods.leech_seed
