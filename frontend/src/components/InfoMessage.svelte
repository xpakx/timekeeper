<script lang="ts">
    import Fa from "svelte-fa";
    import type { InfoDetails } from "../types/InfoDetails";
    import { faClose } from "@fortawesome/free-solid-svg-icons";
    import { createEventDispatcher } from "svelte";

    export let info: InfoDetails;

    const dispatch = createEventDispatcher();

    function closeMessage() {
        dispatch("delete");
    }
</script>

<div class="info {info.reward ? info.reward.rarity : ''}">
    <div class="info-header">
        Reward
        <button on:click={() => closeMessage()} class="btn-icon">
            <Fa icon={faClose} />
        </button>
    </div>
    {#if info.points}
        {info.points} points
    {:else if info.reward}
        {info.reward.name}
    {/if}
</div>

<style>
    .info {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        background-color: #181825;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
    }

    .info-header {
        font-weight: bold;
        color: #a6adc8;
        display: flex;
        justify-content: space-between;
    }

    button {
        font-size: 12;
        padding: 2px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        background-color: #9399b2;
        color: #313244;
    }

    button.btn-icon {
        background-color: transparent;
        color: #9399b2;
    }

    .common {
        border: solid 1px #585b70;
    }

    .uncommon {
        border: solid 1px #cdd6f4;
    }

    .rare {
        border: solid 1px #f2cdcd;
    }

    .info.uncommon .info-header {
        color: #cdd6f4;
    }

    .info.rare .info-header {
        color: #f2cdcd;
    }
</style>
