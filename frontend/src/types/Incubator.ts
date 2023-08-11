import type { UserHero } from "./UserHero";

export type Incubator  = {
    id: number;
    usages: number;
    permanent: boolean;
    hero: UserHero;
}