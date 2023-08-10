<script lang="ts">
    import { goto } from "$app/navigation";
    import HeroCard from "../../components/HeroCard.svelte";
    import { getToken } from "../../token-manager";
    import type { Hero } from "../../types/Hero";

    let apiUri = "http://localhost:8000";
    let hero: Hero;
    let showHero: boolean = false;
    let message: String;
    let crystals: number;
    getCrystals();

    async function generateHero() {
        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        try {
            let response = await fetch(`${apiUri}/heroes/reward`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                let fromEndpoint = await response.json();
                hero = fromEndpoint;
                crystals = crystals - 1;
                showHero = true;
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

    async function getCrystals() {
        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        try {
            let response = await fetch(`${apiUri}/heroes/crystals`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                let fromEndpoint = await response.json();
                crystals = fromEndpoint.crystals;
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
    <title>Reward</title>
</svelte:head>

<button class="hero-btn" on:click={generateHero}>Get</button>
<div class="crystals">
    {#if crystals}
        {crystals} crystals
    {:else}
        No crystals
    {/if}
</div>
{#if showHero}
    <HeroCard {hero} />
{/if}

<style></style>
