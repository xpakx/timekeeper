import type { EnemyHeroBattle } from "./EnemyHeroBattle";
import type { UserHeroBattle } from "./UserHeroBattle";

export type Battle = {
    id: number;
    finished: boolean;
    hero: UserHeroBattle;
    enemy: EnemyHeroBattle;
}