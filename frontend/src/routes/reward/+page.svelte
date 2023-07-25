<script lang="ts">
    import { goto } from "$app/navigation";
    import { getToken } from "../../token-manager";
    import type { Hero } from "../../types/Hero";

    let apiUri = "http://localhost:8000";
    let hero: Hero[];
    let message: String;

    async function generateHero() {
        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        try {
            let response = await fetch(
                `${apiUri}/heroes/reward`,
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
    <title>Reward</title>
</svelte:head>

<button class="hero-btn" on:click={generateHero}>Get</button>
<style></style>