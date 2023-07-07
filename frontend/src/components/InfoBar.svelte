<script lang="ts">
    import Fa from "svelte-fa";
    import type { InfoDetails } from "../types/InfoDetails";
    import { faClose } from "@fortawesome/free-solid-svg-icons";

    export const addInfo = (info: InfoDetails) => addNewInfo(info);
    let infos: InfoDetails[] = [];

    function addNewInfo(info: InfoDetails) {
        infos.push(info);
        infos = infos;
    }

    function closeMessage(index: number) {
        console.log(index);
        infos.splice(index, 1);
        infos = infos;
    }

    function closeAllMessages() {
        infos = [];
    }
</script>

{#if infos.length > 0}
    <button class="clean" on:click={closeAllMessages}>Clean</button>
    <div class="infos">
        {#each infos as info, index}
            <div class="info">
                <div class="info-header">
                    Reward
                    <button on:click={() => closeMessage(index)}>
                        <Fa icon={faClose} />
                    </button>
                </div>
                {info.points} points
            </div>
        {/each}
    </div>
{/if}

<style>
    .infos {
        display: flex;
        gap: 5px;
        overflow: auto;
    }

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
</style>
