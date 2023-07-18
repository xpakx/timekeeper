<script lang="ts">
    import type { EquipmentEntry } from "../types/EquipmentEntry";

    export let item: EquipmentEntry;
</script>

<div class="item-container {item.item.rarity}">
    <div class="item-header">
        <div class="item-name">
            {item.item.name}
        </div>
        <div class="item-count">
            {item.amount}
        </div>
    </div>
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
</style>
