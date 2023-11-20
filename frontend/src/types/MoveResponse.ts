export type StageChange = {
    stage: String,
    change: number
}

export type StatusChange = {
    status: String,
    effect: String
}

export type SkillStatus = {
    stage_changes: StageChange[],
    status_changes: StatusChange[],
}

export type SkillDamage = {
    new_hp?: number,
    current_hp: number,
    critical: boolean,
    effectiveness: number,
    secondary_status_changes: StatusChange[],
}

export type MovementTest = {
    able: boolean,
    reason: String,
}

export type SkillResult = {
    name: String,
    missed: boolean,
    self_targetted: boolean,
    status_skill: SkillStatus,
    skill: SkillDamage,
    able: MovementTest,
    fainted: boolean,
    second_fainted: boolean,
}

export type PostTurnEffect = {
    reason: String,
    new_hp?: number,
    current_hp: number,
    status_end: boolean 
}

export type PostTurn = {
    changes: PostTurnEffect[],
    fainted: boolean,
    second_fainted: boolean,
}

export type Turn = {
    first: SkillResult,
    first_changes: PostTurn,
    second: SkillResult,
    second_changes: PostTurn,
}

export type MoveResponse = {
    turn: Turn,
    hero_first: boolean
}