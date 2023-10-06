<script lang="ts">
    import { goto } from "$app/navigation";
    import { getToken } from "../../../token-manager";
    import { page } from "$app/stores";
    import type { Battle } from "../../../types/Battle";
    let apiUri = "http://localhost:8000";
    let message: String;
    let id = Number($page.params.id);
    getBattle(id);
    let battle: Battle;

    async function getBattle(battleId: number) {
        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        try {
            let response = await fetch(`${apiUri}/battles/${battleId}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                let fromEndpoint = await response.json();
                battle = fromEndpoint;
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

{#if battle}
    <div class="battle-container">
    </div>
{/if}

<style>
    .battle-container {
        margin-bottom: 10px;
    }
</style>
