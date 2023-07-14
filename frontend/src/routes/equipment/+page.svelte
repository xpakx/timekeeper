<script lang="ts">
    import { goto } from "$app/navigation";
    import Fa from "svelte-fa";
    import { getToken } from "../../token-manager";
    import {
        faArrowLeft,
        faArrowRight,
    } from "@fortawesome/free-solid-svg-icons";
    import type { EquipmentEntry } from "../../types/EquipmentEntry";
    let apiUri = "http://localhost:8000";
    let message: String;
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
                `${apiUri}/items${
                    new_page > 0 ? "?page=" + new_page : ""
                }`,
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
    <title>Equipment</title>
</svelte:head>

<h2>Equipment</h2>

{#if items && items.length > 0}
    {#each items as item}
        {item.item.name}
    {/each}
{/if}

<div class="page-nav">
    <button
        class="btn-icon"
        on:click={() => getItems(page - 1)}
        disabled={page <= 0}
    >
        <Fa icon={faArrowLeft} />
    </button>
    <button
        class="btn-icon"
        on:click={() => getItems(page + 1)}
        disabled={!items || items.length < 20}
    >
        <Fa icon={faArrowRight} />
    </button>
</div>

<style>
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

    button.btn-icon {
        border-radius: 7px;
    }

    button.btn-icon:disabled {
        background-color: #313244;
        color: #585b70;
    }
</style>
