<script lang="ts">
    import { goto } from "$app/navigation";
    import { getToken } from "../token-manager";
    import type { EquipmentEntry } from "../types/EquipmentEntry";

    export let item: EquipmentEntry;
    const INCUBATOR = 7;
    const SUPER_INCUBATOR = 16;
    let apiUri = "http://localhost:8000";

    async function installIncubator(id: number) {
        if (id != INCUBATOR && id != SUPER_INCUBATOR) {
            return;
        }

        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        let body = {
            item_id: id,
        };
        try {
            let response = await fetch(`${apiUri}/incubators`, {
                method: "POST",
                body: JSON.stringify(body),
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                let fromEndpoint = await response.json();
                item.amount = item.amount - 1;
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

    async function teachSkill(hero_id: number, num: number) {
        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        let body = {
            item_id: item.id,
            num: num
        };
        try {
            let response = await fetch(`${apiUri}/heroes/${hero_id}/skills`, {
                method: "POST",
                body: JSON.stringify(body),
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                let fromEndpoint = await response.json();
                item.amount = item.amount - 1;
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

<div class="item-container {item.item.rarity}">
    <div class="item-header">
        <div class="item-name-container">
            <div class="item-name">
                {item.item.name}
            </div>
            <div class="item-count">
                [{item.amount}]
            </div>
        </div>
        <div class="item-id">
            #{item.item.num}
        </div>
    </div>

    {#if item.item.num == INCUBATOR || item.item.num == SUPER_INCUBATOR}
        <div class="actions">
            <button on:click={() => installIncubator(item.item.num)}
                >Install</button
            >
        </div>
    {/if}
</div>

<style>
    .item-container {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        background-color: #181825;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
    }

    .item-header {
        display: flex;
        justify-content: space-between;
    }

    .item-name-container {
        display: flex;
        gap: 5px;
    }

    .item-count,
    .item-id {
        color: #585b70;
    }

    .item-name {
        margin-bottom: 5px;
    }

    .common {
        border: solid 1px #585b70;
    }

    .uncommon {
        border: solid 1px #cdd6f4;
    }

    .rare {
        border: solid 1px #f2cdcd;
    }

    .item-container.uncommon .item-name {
        color: #cdd6f4;
    }

    .item-container.rare .item-name {
        color: #f2cdcd;
    }

    button {
        font-size: 14px;
        padding: 5px 10px;
        margin-right: 10px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        background-color: #9399b2;
        color: #313244;
    }
</style>
