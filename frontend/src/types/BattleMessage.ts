export type BattleMessage = {
    message: String;
    hp_change?: number;
    animation?: String;
    target?: 'hero' | 'enemy';
}