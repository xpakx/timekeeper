<script lang="ts">
    import { goto } from "$app/navigation";
    import { getToken } from "../../../token-manager";
    import { page } from "$app/stores";
    import type { UserHeroDetails } from "../../../types/UserHeroDetails";
    import type { Skill } from "../../../types/Skill";
    import SkillChoice from "../../../components/SkillChoice.svelte";
    let apiUri = "http://localhost:8000";
    let message: String;
    let id = Number($page.params.id);
    getHero(id);
    let hero: UserHeroDetails;
    let skills: Skill[] = [];
    let showSkillsToLearn: boolean = false;
    let numChoiceFor: number | undefined = undefined;

    async function getHero(heroId: number) {
        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        try {
            let response = await fetch(`${apiUri}/heroes/${heroId}`, {
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

    async function getLearnableSkills() {
        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }
        showSkillsToLearn = true;
        let heroId = hero.id;

        try {
            let response = await fetch(
                `${apiUri}/heroes/${heroId}/skills/learnable`,
                {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

            if (response.ok) {
                let fromEndpoint = await response.json();
                skills = fromEndpoint;
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

    function showMessage(text: String) {
        message = text;
    }


    function chooseNum(skill_id: number) {
        numChoiceFor = skill_id;
    }


    async function teachSkill(num: number, skill_id: number) {
        numChoiceFor = undefined;
        if (hero == undefined) {
            return;
        }

        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        let id = hero.id;

        let body = {
            skill_id: skill_id,
            num: num,
        };
        try {
            let response = await fetch(`${apiUri}/heroes/${id}/skills`, {
                method: "POST",
                body: JSON.stringify(body),
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                let fromEndpoint = await response.json();
            } else {
                if (response.status == 401) {
                    goto("/logout");
                }
                const errorBody = await response.json();
                showMessage(errorBody.detail);
            }
        } catch (err) {
            if (err instanceof Error) {
                showMessage(err.message);
            }
        }
    }


    async function evolve(hero_id: number) {
        if (hero == undefined) {
            return;
        }

        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        let body = {
            hero_id: hero_id,
        };
        try {
            let response = await fetch(`${apiUri}/heroes/${id}/evolve`, {
                method: "POST",
                body: JSON.stringify(body),
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
                showMessage(errorBody.detail);
            }
        } catch (err) {
            if (err instanceof Error) {
                showMessage(err.message);
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
        {#each hero.skillset as skill}
            {#if skill != undefined}
                {skill.name}
            {:else}
                No skill
            {/if}
        {/each}
    </div>
{/if}

{#if !showSkillsToLearn}
    <button on:click={getLearnableSkills}>Check skills to learn</button>
{:else}
    <div class="skill">
        {#each skills as skill}
            {#if skill != undefined}
                {skill.name}
                <button on:click={() => chooseNum(skill.id)}>Learn</button>
            {:else}
                No skill
            {/if}
            {#if numChoiceFor == skill.id}
                <SkillChoice
                    id={hero.id}
                    on:choice={(event) => {
                        teachSkill(event.detail.id, skill.id);
                    }}
                    on:message={(event) => showMessage(event.detail.body)}
                />
            {/if}
        {/each}
    </div>
{/if}

<style>
    .hero-container {
        margin-bottom: 10px;
    }
</style>
