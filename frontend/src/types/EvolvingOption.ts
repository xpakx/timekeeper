import type { Hero } from "./Hero"
import type { Item } from "./Item"

export type EvolvingOption  = {
    hero: Hero;
    item?: Item
}