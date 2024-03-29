<script lang="ts">
    import { goto } from "$app/navigation";
    import { createEventDispatcher } from "svelte";
    import { getToken } from "../token-manager";
    import type { UserHero } from "../types/UserHero";
    import CompactHeroCard from "./CompactHeroCard.svelte";
    let apiUri = "http://localhost:8000";

    export let active: UserHero | undefined = undefined;
    let active_num: number | undefined = undefined;
    export let team: UserHero[] = [];
    const dispatch = createEventDispatcher();

    async function addToTeam(hero_id: number, num: number) {
        changeTeam("add", num, undefined, hero_id);
    }

    function switchTo(num: number) {
        if (!active_num) {
            return;
        }
        switchHeroes(num, active_num);
        active_num = undefined;
    }

    function startSwitching(num: number) {
        active_num = num;
        dispatch("addedToTeam", { id: undefined });
    }

    function emitMessage(message: String) {
        dispatch("message", { type: "error", body: message });
    }

    function insertAt(num: number) {
        if (!active) {
            return;
        }
        addToTeam(active.id, num);
        dispatch("addedToTeam", { id: active.id });
    }

    async function switchHeroes(num: number, switch_num: number) {
        changeTeam("switch", num, switch_num, undefined);
    }

    async function deleteFromTeam(num: number) {
        changeTeam("delete", num, undefined, undefined);
    }

    async function changeTeam(
        action: String,
        num: number,
        switch_num: number | undefined = undefined,
        hero_id: number | undefined = undefined
    ) {
        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }
        let body = {
            action: action,
            num: num,
            switch_num: switch_num,
            hero_id: hero_id,
        };

        try {
            let response = await fetch(`${apiUri}/teams`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify(body),
            });

            if (response.ok) {
                let fromEndpoint = await response.json();
            } else {
                if (response.status == 401) {
                    goto("/logout");
                }
                const errorBody = await response.json();
                emitMessage(errorBody.detail)
            }
        } catch (err) {
            if (err instanceof Error) {
                emitMessage(err.message)
            }
        }
    }
</script>

{#if team}
    <div class="team-elem">
        {#each team as hero, index}
            <CompactHeroCard {hero} />
            <div class="buttons-container">
                {#if active}
                    <button on:click={() => insertAt(index + 1)}>Add</button>
                {/if}
                {#if active_num && !active}
                    <button on:click={() => switchTo(index + 1)}>Switch</button>
                {:else}
                    <button on:click={() => startSwitching(index + 1)}
                        >Switch</button
                    >
                {/if}
                <button on:click={() => deleteFromTeam(index + 1)}
                    >Delete</button
                >
            </div>
        {/each}
    </div>
    {#each [1, 2, 3, 4, 5, 6] as containers}
        {#if team.length < containers}
            <div class="team-elem">
                <div class="buttons-container">
                    {#if active}
                        <button on:click={() => insertAt(containers)}
                            >Add</button
                        >
                    {/if}
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
