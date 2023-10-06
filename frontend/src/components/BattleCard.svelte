<script lang="ts">
    import type { Battle } from "../types/Battle";
    import HeroHud from "./HeroHUD.svelte";

    export let battle: Battle;
</script>

<div class="battle-container {battle.finished ? 'finished' : ''}">
    <div class="enemy">
        <HeroHud hero={battle.enemy} />
        <div class="hero-image">
            <img src="heroes/00{battle.enemy.hero.num}.png" alt="" />
        </div>
    </div>
    <div class="hero">
        <div class="hero-image">
            <img src="heroes/00{battle.hero.hero.num}.png" alt="" />
        </div>
        <HeroHud hero={battle.hero} showHealth={true} />
    </div>
</div>

<style>
    .battle-container {
        position: relative;
        width: 600px;
        height: 400px;
        background-color: #313244;
        border-radius: 8px;
        box-shadow: 0 4px 8px #11111b;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        background-image: url("background.png");
        background-repeat: no-repeat;
        background-size: cover;
    }

    .hero {
        display: flex;
        justify-content: space-between;
        align-items: end;
        margin-right: 20px;
        margin-bottom: 10px;
    }

    .enemy {
        display: flex;
        justify-content: space-between;
        margin-left: 20px;
        margin-top: 10px;
    }

    .hero-image {
        width: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .hero-image img {
        width: 150px;
        height: 150px;
    }

    .enemy .hero-image {
        margin-top: 20px;
    }
</style>
