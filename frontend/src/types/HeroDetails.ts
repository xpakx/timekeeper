import type { Hero } from "./Hero";
import type { Skillset } from "./Skillset";

export type HeroDetails  = {
    id: number;
    hero: Hero;
    incubated: boolean;
    skillset: Skillset;
}