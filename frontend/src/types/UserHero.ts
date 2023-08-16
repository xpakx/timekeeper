import type { Hero } from "./Hero";

export type UserHero  = {
    id: number;
    hero: Hero;
    incubated: boolean;
}