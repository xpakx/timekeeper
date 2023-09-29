<script lang="ts">
    import type { UserHero } from "../types/UserHero";
    import CompactHeroCard from "./CompactHeroCard.svelte";

    let active: UserHero | undefined = undefined;
    export let team: UserHero[] = [];

    async function deleteHero(heroId: number) {}
</script>

{#if team}
    <div class="team-elem">
        {#each team as hero}
            <CompactHeroCard {hero} />
        {/each}
        <div class="buttons-container">
            <button>Add</button>
            <button>Switch</button>
            <button>Delete</button>
        </div>
    </div>
    {#each [1, 2, 3, 4, 5, 6] as containers}
        {#if team.length < containers}
            <div class="team-elem">
                <div class="buttons-container">
                    <button>Add</button>
                </div>
            </div>
        {/if}
    {/each}
{/if}

<style>
    button {
        font-size: 14px;
        padding: 5px 10px;
        margin-right: 10px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        background-color: #9399b2;
        color: #313244;
    }

    .buttons-container {
        padding-top: 10px;
    }
</style>
