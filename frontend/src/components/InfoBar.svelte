<script lang="ts">
    import type { InfoDetails } from "../types/InfoDetails";

    export const addInfo = (info: InfoDetails) => addNewInfo(info);
    let infos: InfoDetails[] = [];

    function addNewInfo(info: InfoDetails) {
        infos.push(info);
        infos = infos;
    }
</script>

<div class="infos">
    {#each infos as info}
        <div class="info">
            <div class="info-header">Reward</div>
            {info.points} points
        </div>
    {/each}
</div>

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
    }
</style>
