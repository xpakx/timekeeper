export type StageChange = {
    stage: String,
    change: number
}

export type StatusChange = {
    status: String,
    effect: number
}

export type SkillStatus = {
    stage_changes: StageChange[],
    status_changes: StatusChange[],
}

export type SkillDamage = {
    damage: number,
    critical: boolean,
    effectiveness: number,
    secondary_status_changes: StatusChange[],
}

export type MovementTest = {
    able: boolean,
    reason: String,
}

export type SkillResult = {
    missed: boolean,
    status_skill: SkillStatus,
    skill: SkillDamage,
    able: MovementTest,
    fainted: boolean,
    second_fainted: boolean,
}

export type PostTurn = {
    reason: String,
    hp_change: number,
    status_end: boolean 
}

export type Turn = {
    first: SkillResult,
    first_changes: PostTurn[],
    second: SkillResult,
    second_changes: PostTurn[],
    other_fainted: boolean
}

export type MoveResponse = {
    turn: Turn,
    hero_first: boolean
}