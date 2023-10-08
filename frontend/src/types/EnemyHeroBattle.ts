import type { Hero } from "./Hero";

export type EnemyHeroBattle = {
    id: number;
    incubated: boolean;
    hero: Hero;
    current_hp: number;
    level: number;
}