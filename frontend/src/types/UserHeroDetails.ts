import type { HeroDetails } from "./HeroDetails";
import type { Skillset } from "./Skillset";

export type UserHeroDetails = {
    id: number;
    hero: HeroDetails;
    incubated: boolean;
    skillset: Skillset;
}