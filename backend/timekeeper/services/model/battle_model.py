from ...db.models import (
        StatusEffect,
        StageEffect)
from enum import Enum
from pydantic import BaseModel, root_validator
from typing import Optional
import math


class StatusChangeEffect(Enum):
    immune = 1
    success = 2
    already_present = 3


class StageChangeResult(BaseModel):
    stage: StageEffect
    change: int


class StatusChangeResult(BaseModel):
    status: StatusEffect
    effect: StatusChangeEffect


class StatusChangeEffect(Enum):
    immune = 'immune'
    success = 'success'
    already_present = 'affected'
    missed = 'missed'


class StatusSkillResults(BaseModel):
    stage_changes: list[StageChangeResult] = []
    status_changes: list[StatusChangeResult] = []


class DamageSkillResults(BaseModel):
    new_hp: int = 0
    current_hp: Optional[int] = 0
    critical: bool = False
    effectiveness: float = 0.0
    secondary_status_changes: list[StatusChangeResult] = []


class MovementTestResult(BaseModel):
    able: bool = False
    reason: Optional[StatusEffect]


class SkillResult(BaseModel):
    name: Optional[str]
    self_targetted: bool = False
    missed: bool = False
    status_skill: Optional[StatusSkillResults]
    skill: Optional[DamageSkillResults]
    able: Optional[MovementTestResult]
    fainted: bool = False
    second_fainted: bool = False


class PostTurnEffects(BaseModel):
    reason: StatusEffect
    new_hp: Optional[int]
    current_hp: Optional[int]
    status_end: bool = False


class PostTurnResult(BaseModel):
    changes: list[PostTurnEffects]
    fainted: bool = False
    second_fainted: bool = False


class MoveResult(BaseModel):
    first: SkillResult
    first_changes: PostTurnResult
    second: SkillResult
    second_changes: PostTurnResult


class BattleResult(BaseModel):
    turn: MoveResult
    hero_first: bool
    hero_hp: int
    enemy_hp: int

    @root_validator()
    def transform_data(cls, values):
        turn = values.get('turn')
        if not turn:
            return values
        first_skill = turn.first.skill
        second_skill = turn.second.skill
        hero_first = values.get('hero_first')
        hero_skill = first_skill if hero_first else second_skill
        hero_hp = values.pop('hero_hp')
        enemy_skill = second_skill if hero_first else first_skill
        enemy_hp = values.pop('enemy_hp')
        if hero_skill:
            new_hp = hero_skill.new_hp
            hero_skill.current_hp = math.floor(100*((new_hp))/hero_hp)
        if enemy_skill:
            new_hp = enemy_skill.new_hp
            enemy_skill.new_hp = None
            enemy_skill.current_hp = math.floor(100*((new_hp))/enemy_hp)
        first_changes = turn.first_changes.changes
        second_changes = turn.second_changes.changes
        hero_changes = first_changes if hero_first else second_changes
        enemy_changes = second_changes if hero_first else first_changes
        for change in hero_changes:
            new_hp = change.new_hp
            change.current_hp = math.floor(100*((new_hp))/hero_hp)
        for change in enemy_changes:
            new_hp = change.new_hp
            change.new_hp = None
            change.current_hp = math.floor(100*((new_hp))/enemy_hp)
        return values
