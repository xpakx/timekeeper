import type { Skillset } from "./Skillset";

export type HeroDetails  = {
    id: number;
    name: String;
    title: String;
    num: number;
    rarity: string;
    skillset: Skillset;
}