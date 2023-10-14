<script lang="ts">
    import { goto } from "$app/navigation";
    import { getToken } from "../token-manager";
    import { createEventDispatcher } from "svelte";
    import type { EquipmentEntry } from "../types/EquipmentEntry";
    let apiUri = "http://localhost:8000";

    const dispatch = createEventDispatcher();
    let page: number = 0;
    getItems();
    let items: EquipmentEntry[];

    async function getItems(new_page: number = 0) {
        if (new_page < 0) {
            return;
        }

        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        try {
            let response = await fetch(
                `${apiUri}/items${new_page > 0 ? "?page=" + new_page : ""}`,
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
                page = new_page;
                items = fromEndpoint;
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

    function chooseItem(id: number) {
        dispatch("choice", { id: id });
    }

    function emitMessage(message: String) {
        dispatch("message", { type: "error", body: message });
    }
</script>

<div class="items">
    {#each items as item}
        <div class="item">
            <div class="item-header">
                <div class="item-name">
                    {item.item.name}
                </div>
                <div class="item-amount">
                    {item.amount}
                </div>
            </div>
            <button class="item-btn" on:click={() => chooseItem(item.id)}
                >Select</button
            >
        </div>
    {/each}
</div>

<style>
    .items {
        margin-top: 10px;
        display: flex;
        font-size: 15px;
        gap: 10px;
    }

    .item-header {
        display: flex;
        justify-content: space-between;
        gap: 5px;
    }

    .item-btn {
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

    .item-btn:hover {
        background-color: #6c7086;
        color: #f2cdcd;
    }
</style>
