<script lang="ts">
    import { goto } from "$app/navigation";
    import { getToken } from "../token-manager";
    import type { UserHero } from "../types/UserHero";
    import CompactHeroCard from "./CompactHeroCard.svelte";
    let apiUri = "http://localhost:8000";
    let message: String;

    let active: UserHero | undefined = undefined;
    export let team: UserHero[] = [];

    async function addToTeam(hero_id: number, num: number) {
        changeTeam('add', num, undefined, hero_id);
    }

    async function switchHeroes(num: number, switch_num: number) {
        changeTeam('switch', num, switch_num, undefined);
    }

    async function deleteFromTeam(num: number) {
        changeTeam('delete', num, undefined, undefined);
    }
    
    async function changeTeam(
        action: String,
        num: number,
        switch_num: number | undefined = undefined,
        hero_id: number | undefined = undefined,
        ) {
        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }
        let body = {
            action: action,
            num: num,
            switch_num: switch_num,
            hero_id: hero_id
        }

        try {
            let response = await fetch(
                `${apiUri}/teams`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                    body: JSON.stringify(body)
                }
            );

            if (response.ok) {
                let fromEndpoint = await response.json();
            } else {
                if (response.status == 401) {
                    goto("/logout");
                }
                const errorBody = await response.json();
                message = errorBody.detail;
            }
        } catch (err) {
            if (err instanceof Error) {
                message = err.message;
            }
        }
    }
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
