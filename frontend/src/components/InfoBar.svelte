<script lang="ts">
    import Fa from "svelte-fa";
    import type { InfoDetails } from "../types/InfoDetails";
    import { faClose } from "@fortawesome/free-solid-svg-icons";
    import InfoMessage from "./InfoMessage.svelte";

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
            <InfoMessage {info} on:delete={() => closeMessage(index)} />
        {/each}
    </div>
{/if}

<style>
    .infos {
        display: flex;
        gap: 5px;
        overflow: auto;
        margin-top: 5px;
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
</style>
