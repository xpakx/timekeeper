<script lang="ts">
    import { faCancel, faCheck, faStop } from "@fortawesome/free-solid-svg-icons";
    import { createEventDispatcher } from "svelte";

    import Fa from "svelte-fa";
    import { fade } from "svelte/transition";

    export let timer: {
        id: number;
        start_time: Date;
        end_time?: Date;
        state: String;
        timer_id: number;
        timer: {
            name: string;
            duration_s: number;
            autofinish: boolean;
        };
    };
	const dispatch = createEventDispatcher();
    
    export let date: number;
    function state(state: String) {
        dispatch("state", {'state': state});
    }
</script>

<div
    class="timer-container {date - timer.start_time.getTime() >
    1000 * timer.timer.duration_s
        ? 'finished'
        : ''}"
    transition:fade|local
>
    <span class="timer-name"> {timer.timer.name}</span>
    <div class="progress-bar">
        <progress
            value={(date - timer.start_time.getTime()) /
                (1000 * timer.timer.duration_s)}
        />
    </div>
    <div class="buttons">
        {#if date - timer.start_time.getTime() <= 1000 * timer.timer.duration_s}
            <button
                class="btn-icon"
                type="button"
                on:click={() => state("cancelled")}
            >
                <Fa icon={faStop} />
            </button>
        {:else}
            <button
                type="button"
                class="btn-finished btn-icon"
                on:click={() => state("finished")}
            >
                <Fa icon={faCheck} />
            </button>
        {/if}
        <button
            type="button"
            class="btn-fail btn-icon"
            on:click={() => state("failed")}
        >
            <Fa icon={faCancel} />
        </button>
    </div>
</div>

<style>
    .finished {
        color: #a6adc8;
    }

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

    .timer-container .progress-bar {
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

    .finished {
        opacity: 0.5;
    }

    .btn-finished {
        background-color: #a6e3a1;
        color: white;
    }

    .btn-finished:hover {
        background-color: #94e2d5;
    }

    button.btn-fail {
        background-color: #f38ba8;
        color: white;
    }

    button.btn-fail:hover {
        background-color: #eba0ac;
    }

    progress {
        height: 20px;
        border: none;
        border-radius: 10px;
        background-color: #1e1e2e;
        overflow: hidden;
        box-shadow: inset 1px 1px 3px 0 rgba(0, 0, 0, 0.8),
            1px 1px 0 0 rgba(255, 255, 255, 0.12);
    }

    progress::-webkit-progress-bar {
        background-color: #1e1e2e;
        border-radius: 10px;
    }

    progress::-webkit-progress-value {
        background-image: linear-gradient(
                to bottom,
                rgba(255, 255, 255, 0.33) 0,
                rgba(255, 255, 255, 0.08) 50%,
                rgba(0, 0, 0, 0.25) 50%,
                rgba(0, 0, 0, 0.1) 100%
            ),
            linear-gradient(to right, #e67070, #f2cdcd);
    }

    progress::-moz-progress-bar {
        background-image: linear-gradient(
                to bottom,
                rgba(255, 255, 255, 0.33) 0,
                rgba(255, 255, 255, 0.08) 50%,
                rgba(0, 0, 0, 0.25) 50%,
                rgba(0, 0, 0, 0.1) 100%
            ),
            linear-gradient(to right, #e67070, #f2cdcd);
    }

    progress::-ms-fill {
        background-image: linear-gradient(
                to bottom,
                rgba(255, 255, 255, 0.33) 0,
                rgba(255, 255, 255, 0.08) 50%,
                rgba(0, 0, 0, 0.25) 50%,
                rgba(0, 0, 0, 0.1) 100%
            ),
            linear-gradient(to right, #e67070, #f2cdcd);
    }

    progress::-ms-fill-upper {
        background-color: #1e1e2e;
        border-radius: 10px;
    }

    button.btn-icon {
        border-radius: 7px;
    }

    button.btn-icon:disabled {
        background-color: #313244;
        color: #585b70;
    }
</style>
