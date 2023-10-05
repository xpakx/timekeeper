<script lang="ts">
    import { goto } from "$app/navigation";
    import { page } from "$app/stores";
    import type { Skill } from "../types/Skill";
    import { getToken } from "../token-manager";
    import { createEventDispatcher } from "svelte";
    let apiUri = "http://localhost:8000";
    let message: String;
    export let id: number;

    const dispatch = createEventDispatcher();
    getHero(id);
    let skills: (Skill | undefined)[] = [
        undefined,
        undefined,
        undefined,
        undefined,
    ];

    async function getHero(heroId: number) {
        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        try {
            let response = await fetch(`${apiUri}/timers/${heroId}/history`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                let hero = await response.json();
                if (hero.skillset.skill_1) {
                    skills[0] = hero.skillset.skill_1;
                }
                if (hero.skillset.skill_2) {
                    skills[1] = hero.skillset.skill_2;
                }
                if (hero.skillset.skill_3) {
                    skills[2] = hero.skillset.skill_3;
                }
                if (hero.skillset.skill_4) {
                    skills[3] = hero.skillset.skill_4;
                }
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

    function chooseSkill(id: number) {
        dispatch("choice", { id: id });
    }
</script>

<div class="skill">
    {#each [1, 2, 3, 4] as num}
        {#if skills[num] != undefined}
            {skills[num]?.name}
        {:else}
            No skill
        {/if}
        <button on:click={() => chooseSkill(num)}>Select</button>
    {/each}
</div>

<style>
</style>
