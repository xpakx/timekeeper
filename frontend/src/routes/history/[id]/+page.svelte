<script lang="ts">
    import { goto } from "$app/navigation";
    import { getToken } from "../../../token-manager";
    import { page } from "$app/stores";
    import {
        faArrowLeft,
        faArrowRight,
        faCancel,
        faCheck,
        faStop,
    } from "@fortawesome/free-solid-svg-icons";
    import Fa from "svelte-fa";
    let apiUri = "http://localhost:8000";
    let message: String;
    let curr_page: number = 0;
    let id = Number($page.params.id);
    getHistory();

    let timers: {
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
    }[];

    const formatter = new Intl.DateTimeFormat("default", {
        weekday: "short",
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit",
        hour12: false,
    });

    async function getHistory(page: number = 0) {
        if (page < 0) {
            return;
        }

        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        try {
            let response = await fetch(
                `${apiUri}/timers/${id}/history${
                    page > 0 ? "?page=" + page : ""
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
                curr_page = page;
                timers = fromEndpoint.map((t: any) => {
                    return {
                        id: t.id,
                        start_time: new Date(t.start_time),
                        end_time: t.end_time ? new Date(t.end_time) : undefined,
                        state: t.state,
                        timer_id: t.timer_id,
                        timer: t.timer,
                    };
                });
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
    <title>History</title>
</svelte:head>

<h2>Timer's history</h2>

{#if timers && timers.length > 0}
    {#each timers as timer}
        <div class="timer-container">
            <span class="icon {timer.state}">
                {#if timer.state == "finished"}
                    <Fa icon={faCheck} />
                {:else if timer.state == "cancelled"}
                    <Fa icon={faCancel} />
                {:else}
                    <Fa icon={faStop} />
                {/if}
            </span>
            <span class="timer-name"> {timer.timer.name}</span>
            <span class="date">{formatter.format(timer.end_time)}</span>
        </div>
    {/each}
{/if}

<div class="page-nav">
    <button
        class="btn-icon"
        on:click={() => getHistory(curr_page - 1)}
        disabled={curr_page <= 0}
    >
        <Fa icon={faArrowLeft} />
    </button>
    <button
        class="btn-icon"
        on:click={() => getHistory(curr_page + 1)}
        disabled={!timers || timers.length < 20}
    >
        <Fa icon={faArrowRight} />
    </button>
</div>

<style>
    .timer-container {
        margin-bottom: 10px;
    }

    .date {
        font-size: 12px;
        color: #7f849c;
    }

    .icon {
        font-size: 14px;
        padding: 5px 10px;
        margin-right: 10px;
        border: none;
        border-radius: 4px;
        background-color: #9399b2;
        color: #313244;
        border-radius: 7px;
    }

    .icon.finished {
        background-color: #a6e3a1;
        color: white;
    }

    .icon.failed {
        background-color: #f38ba8;
        color: white;
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
