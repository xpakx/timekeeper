<script lang="ts">
    import type { EnemyHeroBattle } from "../types/EnemyHeroBattle";
    import type { UserHeroBattle } from "../types/UserHeroBattle";

    export let hero: EnemyHeroBattle | UserHeroBattle;
</script>

<div class="hud">
    <div class="hexagon">
        <div class="top-container">
            <div class="hero-name">{hero.hero.name}</div>
            <div class="level">Lv {hero.level}</div>
        </div>
        <div class="progress-container">
            <div
                class="progress-bar {hero.current_hp < 50
                    ? hero.current_hp < 10
                        ? 'low'
                        : 'medium'
                    : ''}"
                style="width: {hero.current_hp}%;"
            />
        </div>
        {#if 'hp' in hero}
        <div class="health">
            {hero.hp-hero.damage}/{hero.hp}
        </div>
        {/if}
    </div>
</div>

<style>
    .hexagon {
        height: 50px;
        width: 150px;
        background: #1e1e2e;
        position: relative;
        box-sizing: border-box;
        padding: 5px 5px;
    }

    .hexagon::before,
    .hexagon::after {
        content: "";
        z-index: -1;
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: #1e1e2e;
        width: 20px;
    }

    .hexagon::before {
        left: -20px;
        clip-path: polygon(100% 0, 50% 50%, 100% 100%);
    }

    .hexagon::after {
        left: 100%;
        clip-path: polygon(0 0, 50% 50%, 0 100%);
    }

    .hero-name {
        color: #cdd6f4;
    }

    .progress-container {
        background-color: #11111b;
    }

    .progress-bar {
        height: 5px;
        background-color: #a6e3a1;
    }

    .progress-bar.medium {
        background-color: #fab387;
    }

    .progress-bar.low {
        background-color: #f38ba8;
    }

    .hud {
        filter: drop-shadow(0 0 0 #11111b) drop-shadow(0 0 1px #f2cdcd);
    }

    .top-container {
        font-size: 13px;
        display: flex;
        justify-content: space-between;
    }

    .health {
        font-size: 13px;
        color: #a6adc8;
        width: 100%;
        display: flex;
        justify-content: end;
    }
</style>
