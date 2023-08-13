<script lang="ts">
    import type { Hero } from "../types/Hero";

    export let hero: Hero;
</script>

<div class="hero-modal {hero.rarity}">
    <div class="hero-header">
        <div class="spacer" />
        <div class="hero-name">
            {hero.name}
        </div>
        <div class="hero-id">
            #{hero.num}
        </div>
    </div>
    <div class="hero-title">{hero.title}</div>
    <div class="hero-image">
        <img src="heroes/hero_{hero.num}.png" alt="" />
    </div>
</div>

<style>
    .hero-modal {
        position: relative;
        width: 300px;
        height: 400px;
        background-color: #313244;
        border-radius: 8px;
        box-shadow: 0 4px 8px #11111b;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .hero-modal.common {
        border: 2px solid #585b70;
    }

    .hero-modal.uncommon {
        border: 2px solid #cdd6f4;
    }

    .hero-modal.rare {
        border: 2px solid #f2cdcd;
    }

    .hero-header {
        display: flex;
        justify-content: space-between;
        width: 100%;
        padding: 16px;
    }

    .hero-name {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 8px;
        color: #f2cdcd;
    }

    .hero-id {
        font-size: 14px;
        color: #9399b2;
    }

    .hero-image {
        width: 150px;
        height: 150px;
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
