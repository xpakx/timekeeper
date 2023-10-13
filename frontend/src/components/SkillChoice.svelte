<script lang="ts">
    import { goto } from "$app/navigation";
    import type { Skill } from "../types/Skill";
    import { getToken } from "../token-manager";
    import { createEventDispatcher } from "svelte";
    let apiUri = "http://localhost:8000";
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
                skills = hero.skillset;
            } else {
                if (response.status == 401) {
                    goto("/logout");
                }
                const errorBody = await response.json();
                emitMessage(errorBody.detail);
            }
        } catch (err) {
            if (err instanceof Error) {
                emitMessage(err.message);
            }
        }
    }

    function chooseSkill(id: number) {
        dispatch("choice", { id: id });
    }

    function emitMessage(message: String) {
        dispatch("message", { type: "error", body: message });
    }
</script>

<div class="skill">
    {#each skills as skill, index}
        {#if skill != undefined}
            {skill.name}
        {:else}
            No skill
        {/if}
        <button on:click={() => chooseSkill(index+1)}>Select</button>
    {/each}
</div>

<style>
</style>
