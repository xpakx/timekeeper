import type { HeroDetails } from "./HeroDetails";
import type { Skill } from "./Skill";

export type UserHeroDetails = {
    id: number;
    hero: HeroDetails;
    incubated: boolean;
    skillset: (Skill|null)[];
}