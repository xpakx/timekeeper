export type BattleMessage = {
    message: String;
    new_hp?: number;
    animation?: String;
    target?: 'hero' | 'enemy';
}