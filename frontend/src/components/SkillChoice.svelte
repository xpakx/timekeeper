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

<div class="skills">
    {#each skills as skill, index}
        <div class="skill">
            <div class="skill-header">
                <div class="skill-name">
                    {#if skill != undefined}
                        {skill.name}
                    {:else}
                        No skill
                    {/if}
                </div>
            </div>
            <button class="skill-btn" on:click={() => chooseSkill(index + 1)}
                >Select</button
            >
        </div>
    {/each}
</div>

<style>
    .skills {
        margin-top: 10px;
        display: flex;
        font-size: 15px;
        gap: 10px;
    }

    .skill-header {
        display: flex;
        justify-content: space-between;
        gap: 5px;
    }

    .skill-btn {
        margin-top: 5px;
        background-color: #313244;
        color: #a6adc8;
        width: 100%;
        padding-top: 5px;
        padding-bottom: 5px;
        border: none;
        border-radius: 0 0 10px 10px;
        cursor: pointer;
    }

    .skill-btn:hover {
        background-color: #6c7086;
        color: #f2cdcd;
    }
</style>
