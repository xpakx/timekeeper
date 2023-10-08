<script lang="ts">
    import { goto } from "$app/navigation";
    import { getToken } from "../../token-manager";
    import type { Battle } from "../../types/Battle";
    import BattleCard from "../../components/BattleCard.svelte";
    let apiUri = "http://localhost:8000";
    let message: String;
    getCurrentBattle();
    let battle: Battle = {
        id: 1,
        finished: false,
        hero: {
            id: 1,
            incubated: false,
            hp: 10,
            current_hp: 50,
            damage: 5,
            level: 1,
            hero: {
                id: 1,
                name: "Bulbasaur",
                title: "",
                num: 1,
                rarity: "rare",
                hero_type: "grass",
                secondary_hero_type: "poison",
                base_hp: 10,
            },
            skillset: [],
        },
        enemy: {
            id: 2,
            incubated: false,
            current_hp: 9,
            level: 1,
            hero: {
                id: 2,
                name: "Charmander",
                title: "",
                num: 4,
                rarity: "rare",
                hero_type: "fire",
            },
        }
    };

    async function getCurrentBattle() {
        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        try {
            let response = await fetch(`${apiUri}/battles`, {
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

    async function makeMove(num: number) {
        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        let body = {
            id: num,
            move: "skill",
        };
        try {
            let response = await fetch(`${apiUri}/battles/${battle.id}`, {
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
    <title>Battle</title>
</svelte:head>

{#if battle}
    <BattleCard {battle} />
{:else}
    <div>No active battle</div>
{/if}

<style>
</style>
