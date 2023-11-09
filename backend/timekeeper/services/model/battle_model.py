from ...db.models import (
        StatusEffect,
        StageEffect)
from enum import Enum


class StatusChangeEffect(Enum):
    immune = 1
    success = 2
    already_present = 3


class StageChangeResult():
    stage: StageEffect
    change: int

    def __init__(self, stage, change):
        self.stage = stage
        self.change = change


class StatusChangeResult():
    status: StatusEffect
    effect: StatusChangeEffect

    def __init__(self, status, effect):
        self.status = status
        self.effect = effect


class StatusChangeEffect(Enum):
    immune = 1
    success = 2
    already_present = 3


class StatusSkillResults():
    stage_changes: list[StageChangeResult] = []
    status_changes: list[StatusChangeResult] = []


class DamageSkillResults():
    damage: int = 0
    secondary_status_changes: list[StatusChangeResult] = []


class SkillResult():
    missed: bool = False
    status_skill: StatusSkillResults
    skill: DamageSkillResults
