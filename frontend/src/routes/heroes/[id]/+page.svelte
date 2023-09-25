<script lang="ts">
    import { goto } from "$app/navigation";
    import { getToken } from "../../../token-manager";
    import { page } from "$app/stores";
    import type { HeroDetails } from "../../../types/HeroDetails";
    let apiUri = "http://localhost:8000";
    let message: String;
    let id = Number($page.params.id);
    getHero(id);
    let hero: HeroDetails;

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
                let fromEndpoint = await response.json();
                hero = fromEndpoint;
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

<svelte:head>
    <title>Hero</title>
</svelte:head>

{#if hero}
    <div class="hero-container">
        {hero.name}
    </div>
    <div class="skill">
        {#if hero.skillset.skill_1}
            {hero.skillset.skill_1.name}
        {:else}
            No skill
        {/if}
    </div>
    <div class="skill">
        {#if hero.skillset.skill_2}
            {hero.skillset.skill_2.name}
        {:else}
            No skill
        {/if}
    </div>
    <div class="skill">
        {#if hero.skillset.skill_3}
            {hero.skillset.skill_3.name}
        {:else}
            No skill
        {/if}
    </div>
    <div class="skill">
        {#if hero.skillset.skill_4}
            {hero.skillset.skill_4.name}
        {:else}
            No skill
        {/if}
    </div>
{/if}

<style>
    .hero-container {
        margin-bottom: 10px;
    }
</style>
