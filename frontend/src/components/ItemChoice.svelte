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
                emitMessage(errorBody.detail)
            }
        } catch (err) {
            if (err instanceof Error) {
                emitMessage(err.message)
            }
        }
    }

    function chooseSkill(id: number) {
        dispatch("choice", { id: id });
    }

    function emitMessage(message: String) {
        dispatch("message", { type: "error", body: message });
    }
</script>

<div class="items">
    {#each items as item}
         {item.item.name}
    {/each}
</div>

<style>
</style>
