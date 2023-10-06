import type { UserHero } from "./UserHero";

export type Battle = {
    id: number;
    finished: boolean;
    hero: UserHero;
    enemy: UserHero;
}