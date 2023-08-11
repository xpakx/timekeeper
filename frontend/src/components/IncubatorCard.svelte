<script lang="ts">
    import type { Incubator } from "../types/Incubator";

    export let incubator: Incubator;
</script>

<div class="incubator-card">
    {#if incubator.hero}
        <div class="hero-container">
            <div class="hero-header">
                <span class="hero-name">{incubator.hero.hero.name}</span>,
                <span class="hero-title">{incubator.hero.hero.title}</span>
            </div>
            <div class="hero-image">
                <img src="heroes/hero_{incubator.hero.hero.num}.png" alt="" />
            </div>
        </div>
    {:else}
        <div class="empty">Empty</div>
    {/if}
</div>

<style>
    .incubator-card {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        background-color: #181825;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
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
