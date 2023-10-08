import type { HeroBattle } from "./HeroBattle";
import type { Skill } from "./Skill";

export type UserHeroBattle = {
    id: number;
    incubated: boolean;
    hero: HeroBattle;
    current_hp: number;
    level: number;
    hp: number;
    damage: number;
    skillset: (Skill|null)[];
}