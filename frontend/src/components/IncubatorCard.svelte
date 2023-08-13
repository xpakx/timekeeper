<script lang="ts">
    import { goto } from "$app/navigation";
    import { createEventDispatcher } from "svelte";
    import { getToken } from "../token-manager";
    import type { Incubator } from "../types/Incubator";
    import type { UserHero } from "../types/UserHero";

    export let incubator: Incubator;
    export let hero: UserHero | undefined;
    let apiUri = "http://localhost:8000";
    const dispatch = createEventDispatcher();

    async function deleteIncubator() {
        if (!incubator) {
            return;
        }

        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        try {
            let response = await fetch(`${apiUri}/incubators/${incubator.id}`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                // TODO: send delete event to parent
            } else {
                if (response.status == 401) {
                    goto("/logout");
                }
                const errorBody = await response.json();
                // TODO: send error msg to parent
            }
        } catch (err) {
            if (err instanceof Error) {
                // TODO: send error msg to parent
            }
        }
    }

    async function incubate() {
        if (!incubator || !hero) {
            return;
        }

        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        let body = {
            hero_id: hero.id,
        };
        console.log(body);

        dispatch("endChoice");
        console.log(body);
        try {
            let response = await fetch(`${apiUri}/incubators/${incubator.id}`, {
                method: "POST",
                body: JSON.stringify(body),
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                // TODO: send event to parent
                incubator.hero = hero;
            } else {
                if (response.status == 401) {
                    goto("/logout");
                }
                const errorBody = await response.json();
                // TODO: send error msg to parent
            }
        } catch (err) {
            if (err instanceof Error) {
                // TODO: send error msg to parent
            }
        }
    }
</script>

<div class="incubator-card">
    {#if incubator.hero}
        <div class="hero-container">
            <div class="hero-header">
                <span class="hero-name">{incubator.hero.hero.name}</span>,
                <span class="hero-title">{incubator.hero.hero.title}</span>
            </div>
            <div class="hero-image">
                <img src="heroes/hero_{incubator.hero.hero.num}.png" alt="" />
            </div>
        </div>
    {:else}
        <div class="empty">Empty</div>
        <button on:click={deleteIncubator}>Delete</button>
        {#if hero}
            <button on:click={incubate}>Incubate</button>
        {/if}
    {/if}
</div>

<style>
    .incubator-card {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        background-color: #181825;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
    }

    .hero-header {
        width: 100%;
        padding: 16px;
    }

    .hero-name {
        font-weight: bold;
        margin-bottom: 8px;
        color: #f2cdcd;
    }

    .hero-image {
        width: 70px;
        height: 70px;
        margin-top: 16px;
    }

    .hero-image img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 50%;
        box-shadow: 0 2px 4px #11111b;
    }
</style>
