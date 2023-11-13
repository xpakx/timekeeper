from ...db.models import (
        StatusEffect,
        StageEffect)
from enum import Enum
from pydantic import BaseModel
from typing import Optional


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
    immune = 1
    success = 2
    already_present = 3


class StatusSkillResults(BaseModel):
    stage_changes: list[StageChangeResult] = []
    status_changes: list[StatusChangeResult] = []


class DamageSkillResults(BaseModel):
    damage: int = 0
    critical: bool = False
    effectiveness: float = 0.0
    secondary_status_changes: list[StatusChangeResult] = []


class MovementTestResult(BaseModel):
    able: bool = False
    reason: Optional[StatusEffect]


class SkillResult(BaseModel):
    missed: bool = False
    status_skill: Optional[StatusSkillResults]
    skill: Optional[DamageSkillResults]
    able: Optional[MovementTestResult]
    fainted: bool = False
    other_fainted: bool = False


class PostTurnEffects(BaseModel):
    reason: StatusEffect
    hp_change: Optional[int]
    status_end: bool = False


class MoveResult(BaseModel):
    first: SkillResult
    first_changes: list[PostTurnEffects]
    second: SkillResult
    second_changes: list[PostTurnEffects]
    other_fainted: bool = False


class BattleResult(BaseModel):
    turn: MoveResult
    hero_first: bool
