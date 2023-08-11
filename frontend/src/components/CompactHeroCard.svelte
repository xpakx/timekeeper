<script lang="ts">
    import type { UserHero } from "../types/UserHero";

    export let hero: UserHero;
</script>

<div class="hero-card {hero.hero.rarity}">
    <div class="hero-container">
        <div class="hero-header">
            <span class="hero-name">{hero.hero.name}</span>, 
            <span class="hero-title">{hero.hero.title}</span>
            <span class="hero-id">
                [#{hero.hero.num}]
            </span>
        </div>
    </div>
    <div class="hero-image">
        <img src="heroes/hero_{hero.hero.num}.png" alt="" />
    </div>
</div>

<style>
    .hero-card {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        background-color: #181825;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
    }

    .hero-card.common {
        border: 2px solid #585b70;
    }

    .hero-card.uncommon {
        border: 2px solid #cdd6f4;
    }

    .hero-card.rare {
        border: 2px solid #f2cdcd;
    }

    .hero-header {
        width: 100%;
        padding: 16px;
    }

    .hero-name {
        font-weight: bold;
        margin-bottom: 8px;
        color: #f2cdcd;
    }

    .hero-id {
        font-size: 14px;
        color: #9399b2;
    }

    .hero-image {
        width: 70px;
        height: 70px;
        margin-top: 16px;
    }

    .hero-image img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 50%;
        box-shadow: 0 2px 4px #11111b;
    }
</style>
