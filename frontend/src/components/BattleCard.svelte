<script lang="ts">
    import type { Battle } from "../types/Battle";

    export let battle: Battle;
</script>

<div class="battle-container {battle.finished ? 'finished' : ''}">
    {battle.hero.hero.name}
    vs. 
    {battle.enemy.hero.name}
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
        align-items: center;
    }
</style>
