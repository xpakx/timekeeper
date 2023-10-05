<script lang="ts">
    import { goto } from "$app/navigation";
    import { createEventDispatcher } from "svelte";
    import { getToken } from "../token-manager";
    import type { EquipmentEntry } from "../types/EquipmentEntry";
    import HeroChoice from "./HeroChoice.svelte";
    import SkillChoice from "./SkillChoice.svelte";

    export let item: EquipmentEntry;
    let apiUri = "http://localhost:8000";
    let hero_choice: boolean = false;
    let skill_choice: boolean = false;
    let hero_id: undefined | number = undefined;
    const dispatch = createEventDispatcher();

    async function installIncubator() {
        if (item.item.item_type == "incubator") {
            return;
        }

        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        let body = {
            item_id: item.id,
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
                emitMessage(errorBody.detail);
            }
        } catch (err) {
            if (err instanceof Error) {
                emitMessage(err.message);
            }
        }
    }

    async function teachSkill(num: number) {
        if (item.item.item_type == "skill") {
            return;
        }
        if (hero_id == undefined) {
            return;
        }

        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        let id = hero_id;
        hero_id = undefined;
        skill_choice = false;

        let body = {
            item_id: item.id,
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
                item.amount = item.amount - 1;
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

    function startSkillTeaching() {
        hero_choice = true;
    }

    function selectHero(id: number) {
        hero_choice = false;
        hero_id = id;
    }

    function emitMessage(message: String) {
        dispatch("message", { type: "error", body: message });
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

    <div class="actions">
        {#if item.item.item_type == "incubator"}
            <button on:click={installIncubator}>Install</button>
        {/if}
        {#if item.item.item_type == "skill"}
            <button on:click={startSkillTeaching}>Teach</button>
        {/if}
    </div>
    {#if hero_choice}
        <HeroChoice
            on:choice={(event) => {
                selectHero(event.detail.id);
            }}
            on:message={(event) => emitMessage(event.detail.body)}
        />
    {/if}
    {#if skill_choice && hero_id}
        <SkillChoice
            id={hero_id}
            on:choice={(event) => {
                teachSkill(event.detail.id);
            }}
            on:message={(event) => emitMessage(event.detail.body)}
        />
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
