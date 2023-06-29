<script lang="ts">
    import { goto } from "$app/navigation";
    import { faEdit, faPlay, faTrash } from "@fortawesome/free-solid-svg-icons";
    import Fa from "svelte-fa";
    import { createEventDispatcher } from 'svelte';

    export let timer: {
        id: number;
        name: String;
        description: String;
        duration_s: number;
        autofinish: boolean;
    };

	const dispatch = createEventDispatcher();

	function deleteTimer() {
		dispatch('delete');
	}

	function startTimer() {
		dispatch('start');
	}
</script>

<div class="timer-container">
    <span class="timer-name"> {timer.name}</span>
    <div class="buttons">
        <button
            class="btn-icon"
            type="button"
            on:click={deleteTimer}
        >
            <Fa icon={faTrash} />
        </button>
        <button
            class="btn-icon"
            type="button"
            on:click={() => goto(`/edit/${timer.id}`)}
        >
            <Fa icon={faEdit} />
        </button>
        <button
            class="btn-icon"
            type="button"
            on:click={startTimer}
        >
            <Fa icon={faPlay} />
        </button>
    </div>
</div>

<style>
    .timer-container {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        background-color: #181825;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
    }

    .timer-container .timer-name {
        margin-bottom: 5px;
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

    button.btn-icon {
        border-radius: 7px;
    }

    button.btn-icon:disabled {
        background-color: #313244;
        color: #585b70;
    }
</style>