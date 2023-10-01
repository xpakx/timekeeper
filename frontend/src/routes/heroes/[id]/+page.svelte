<script lang="ts">
    import { goto } from "$app/navigation";
    import { getToken } from "../../../token-manager";
    import { page } from "$app/stores";
    import type { UserHeroDetails } from "../../../types/UserHeroDetails";
    import type { Skill } from "../../../types/Skill";
    let apiUri = "http://localhost:8000";
    let message: String;
    let id = Number($page.params.id);
    getHero(id);
    let hero: UserHeroDetails;
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
                let fromEndpoint = await response.json();
                hero = fromEndpoint;
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
</script>

<svelte:head>
    <title>Hero</title>
</svelte:head>

{#if hero}
    <div class="hero-container">
        {hero.hero.name}
    </div>
    <div class="skill">
        {#each [1, 2, 3, 4] as container}
            {#if skills[container] != undefined}
                {skills[container]?.name}
            {:else}
                No skill
            {/if}
        {/each}
    </div>
{/if}

<style>
    .hero-container {
        margin-bottom: 10px;
    }
</style>
