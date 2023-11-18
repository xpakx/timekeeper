<script lang="ts">
    import Fa from "svelte-fa";
    import type { Battle } from "../types/Battle";
    import HeroHud from "./HeroHUD.svelte";
    import {
        faBolt,
        faBox,
        faCrosshairs,
        faRunning,
    } from "@fortawesome/free-solid-svg-icons";
    import { createEventDispatcher } from "svelte";
    import ItemChoice from "./ItemChoice.svelte";
    import type { BattleMessage } from "../types/BattleMessage";

    export let battle: Battle;
    export let battleMessages: BattleMessage[] = [];
    const dispatch = createEventDispatcher();
    let itemChoice: boolean = false;

    function emitSkill(num: number) {
        dispatch("skill", { num: num });
    }

    function emitItem(id: number) {
        closeItemChoice();
        dispatch("item", { num: id });
    }

    function emitFleeAction() {
        dispatch("flee");
    }

    function switchItemChoice() {
        itemChoice = !itemChoice;
    }

    function closeItemChoice() {
        itemChoice = false;
    }

    function closeMessage() {
        battleMessages.shift();
        battleMessages = battleMessages;
    }
</script>

<div class="main-container">
    <div class="view-container">
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
                <HeroHud hero={battle.hero} />
            </div>
        </div>

        {#if battleMessages.length > 0}
            <div class="message-container">
                <div class="message">
                    <div class="message-inner-container">
                        {battleMessages[0].message}
                        <div class="message-buttons-container">
                            <button
                                class="message-close-btn"
                                on:click={closeMessage}>close</button
                            >
                        </div>
                    </div>
                </div>
            </div>
        {:else}
            <div class="skills-container">
                {#each battle.hero.skillset as skill, index}
                    <div class="skill">
                        {#if skill != undefined}
                            <div class="skill-header">
                                <div class="skill-name">
                                    {skill.name}
                                </div>
                                <div class="skill-pp">
                                    {skill.max_usages}/{skill.max_usages}
                                </div>
                            </div>
                            <div class="skill-stats">
                                <div class="skill-power">
                                    <Fa icon={faBolt} />
                                    {skill.power}
                                </div>
                                <div class="skill-accuracy">
                                    <Fa icon={faCrosshairs} />
                                    {skill.accuracy}
                                </div>
                                <div
                                    class="skill-type {'type-' +
                                        skill.move_type}"
                                >
                                    {skill.move_type}
                                </div>
                            </div>
                            <button
                                class="skill-btn"
                                on:click={() => emitSkill(index + 1)}
                                >Use</button
                            >
                        {:else}
                            No skill
                        {/if}
                    </div>
                {/each}
            </div>
        {/if}
    </div>
    <div class="action-container">
        <button class="action-btn" on:click={emitFleeAction}>
            <Fa icon={faRunning} />
        </button>
        <button class="action-btn" on:click={switchItemChoice}>
            <Fa icon={faBox} />
        </button>
    </div>
</div>

{#if itemChoice}
    <div class="item-container">
        <ItemChoice on:choice={(event) => emitItem(event.detail.id)} />
    </div>
{/if}

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

    .skills-container {
        width: 600px;
        margin-top: 10px;
        display: flex;
        justify-content: space-between;
        font-size: 15px;
    }

    .skill-header {
        display: flex;
        justify-content: space-between;
        gap: 5px;
    }

    .skill-stats {
        display: flex;
        justify-content: space-between;
        gap: 5px;
        margin-top: 5px;
    }

    .skill-type {
        font-size: 10px;
        background-color: #313244;
        color: #a6adc8;
        border-radius: 4px;
        padding: 2px 5px;
    }

    .type-grass {
        color: #181825;
        background-color: #a6e3a1;
    }

    .type-fire {
        color: #181825;
        background-color: #fab387;
    }

    .type-water {
        color: #181825;
        background-color: #89b4fa;
    }

    .type-electric {
        color: #181825;
        background-color: #f9e2af;
    }

    .type-ice {
        color: #181825;
        background-color: #89dceb;
    }

    .type-fighting {
        color: #181825;
        background-color: #f38ba8;
    }

    .type-poison {
        color: #181825;
        background-color: #cba6f7;
    }

    .type-ground {
        color: #181825;
        background-color: #eba0ac;
    }

    .type-flying {
        color: #181825;
        background-color: #b4befe;
    }

    .type-psychic {
        color: #181825;
        background-color: #f2cdcd;
    }

    .type-bug {
        color: #181825;
        background-color: #94e2d5;
    }

    .type-rock {
        color: #181825;
        background-color: #94e2d5;
    }

    .type-ghost {
        color: #181825;
        background-color: #eba0ac;
    }

    .type-dragon {
        color: #181825;
        background-color: #89b4fa;
    }

    .type-dark {
        color: #181825;
        background-color: #11111b;
    }

    .type-steel {
        color: #181825;
        background-color: #9399b2;
    }

    .type-fairy {
        color: #181825;
        background-color: #f5c2e7;
    }

    .skill-btn {
        margin-top: 5px;
        background-color: #313244;
        color: #a6adc8;
        width: 100%;
        padding-top: 5px;
        padding-bottom: 5px;
        border: none;
        border-radius: 0 0 10px 10px;
        cursor: pointer;
    }

    .skill-btn:hover {
        background-color: #6c7086;
        color: #f2cdcd;
    }

    .main-container {
        display: flex;
    }

    .action-container {
        display: flex;
        flex-direction: column;
        justify-content: right;
        gap: 5px;
        margin-left: 10px;
    }

    .action-btn {
        font-size: 14px;
        cursor: pointer;
        color: #7f849c;
        margin-right: 10px;
        background-color: transparent;
        border: none;
    }

    .action-btn:hover {
        color: #6c7086;
    }

    .message-container {
        width: 600px;
        margin-top: 10px;
        display: flex;
        justify-content: center;
    }

    .message {
        width: 400px;
        display: flex;
        background-color: #45475a;
        padding: 3px;
    }

    .message-inner-container {
        width: 100%;
        background-color: #45475a;
        flex-direction: column;
        justify-content: space-between;
        border: solid 2px #313244;
        padding: 2px;
        color: #bac2de;
    }

    .message-buttons-container {
        display: flex;
        justify-content: end;
    }

    .message-close-btn {
        margin-top: 5px;
        background-color: #313244;
        color: #a6adc8;
        padding-top: 5px;
        padding-bottom: 5px;
        border: none;
        border-radius: 10px 5px 10px 5px;
        cursor: pointer;
    }

    .message-close-btn:hover {
        background-color: #6c7086;
        color: #f2cdcd;
    }
</style>
