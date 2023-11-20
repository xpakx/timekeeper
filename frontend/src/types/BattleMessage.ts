export type BattleMessage = {
    message: String;
    new_hp?: number;
    new_current_hp?: number,
    animation?: String;
    target?: 'hero' | 'enemy';
}