<script lang="ts">
    import type { Hero } from "../types/Hero";

    export let hero: Hero;
</script>

<div class="hero-modal {hero.rarity}">
        <div class="hero-header">
            <div class="hero-name">
                {hero.name}
            </div>
            <div class="hero-id">
                #{hero.num}
            </div>
            <div class="hero-image">
                <img src="heroes/hero_{hero.num}.png" alt="" />
            </div>
        </div>
    </div>
<style>
</style>
