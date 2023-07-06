<script lang="ts">
    import type { InfoDetails } from "../types/InfoDetails";

    export const addInfo = (info: InfoDetails) => addNewInfo(info);
    let infos: InfoDetails[] = [];


    function addNewInfo(info: InfoDetails) {
        console.log(info.points);
        infos.push(info);
        infos = infos;

    }

</script>
{#each infos as info }
<div class="info">
    {info.points}
</div>
    
{/each}

<style></style>