<script lang="ts">
    import { tokenStorage } from "../storage";
    import { goto } from "$app/navigation";
    import { tweened } from "svelte/motion";
    import { getToken } from "../token-manager";
    import Fa from "svelte-fa";
    import {
        faTrash,
        faEdit,
        faPlay,
        faStop,
        faCancel,
        faCheck,
        faAdd,
    } from "@fortawesome/free-solid-svg-icons";
    import { fade } from "svelte/transition";
    import { onDestroy } from "svelte";

    let apiUri = "http://localhost:8000";
    let message: String;
    let date = tweened(Date.now(), { duration: 500 });
    let timer_interval = setInterval(() => {
        $date = Date.now();
        testTimers();
    }, 500);
    let audio: HTMLAudioElement;

    let timers: {
        id: number;
        name: String;
        description: String;
        duration_s: number;
        autofinish: boolean;
    }[];
    let running_timers: {
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

    tokenStorage.subscribe((_) => {
        getAllTimers();
        getActiveTimers();
    });

    onDestroy(() => {
        clearInterval(timer_interval);
    });


    async function getAllTimers() {
        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        try {
            let response = await fetch(`${apiUri}/timers/`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                timers = await response.json();
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

    async function getActiveTimers() {
        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        try {
            let response = await fetch(`${apiUri}/timers/active`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                let fromEndpoint = await response.json();
                running_timers = fromEndpoint.map((t: any) => {
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

    function add() {
        goto("/add");
    }

    async function deleteTimer(id: number) {
        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        try {
            let response = await fetch(`${apiUri}/timers/${id}`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                timers = timers.filter((a) => a.id != id);
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

    async function startTimer(id: number) {
        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        try {
            let response = await fetch(`${apiUri}/timers/${id}/instances`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                let new_timer = await response.json();
                new_timer.start_time = new Date(new_timer.start_time);
                running_timers = [...running_timers, new_timer];
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

    async function changeTimerState(id: number, state: String) {
        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        let body = {
            state: state,
        };
        try {
            let response = await fetch(
                `${apiUri}/timers/instances/${id}/state`,
                {
                    method: "POST",
                    body: JSON.stringify(body),
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

            if (response.ok) {
                running_timers = running_timers.filter((a) => a.id != id);
                let fromEndpoint = await response.json();
                let points = fromEndpoint.points;
                if (points > 0) {
                    console.log(points);
                }
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

    function testTimers() {
        if (!running_timers) {
            return;
        }

        running_timers.forEach((t) => {
            if (
                $date - t.start_time.getTime() > 1000 * t.timer.duration_s &&
                $date - t.start_time.getTime() - 500 <=
                    1000 * t.timer.duration_s
            ) {
                if (audio.paused) {
                    audio.play();
                }
                if (t.timer.autofinish) {
                    changeTimerState(t.id, "finished");
                }
            }
        });
    }
</script>

<svelte:head>
    <title>Home</title>
</svelte:head>

{#if running_timers && running_timers.length > 0}
    <h2>Running</h2>

    {#each running_timers as timer}
        <div
            class="timer-container {$date - timer.start_time.getTime() >
            1000 * timer.timer.duration_s
                ? 'finished'
                : ''}"
            transition:fade|local
        >
            <span class="timer-name"> {timer.timer.name}</span>
            <div class="progress-bar">
                <progress
                    value={($date - timer.start_time.getTime()) /
                        (1000 * timer.timer.duration_s)}
                />
            </div>
            <div class="buttons">
                {#if $date - timer.start_time.getTime() <= 1000 * timer.timer.duration_s}
                    <button
                        class="btn-icon"
                        type="button"
                        on:click={() => changeTimerState(timer.id, "cancelled")}
                    >
                        <Fa icon={faStop} />
                    </button>
                {:else}
                    <button
                        type="button"
                        class="btn-finished btn-icon"
                        on:click={() => changeTimerState(timer.id, "finished")}
                    >
                        <Fa icon={faCheck} />
                    </button>
                {/if}
                <button
                    type="button"
                    class="btn-fail btn-icon"
                    on:click={() => changeTimerState(timer.id, "failed")}
                >
                    <Fa icon={faCancel} />
                </button>
            </div>
        </div>
    {/each}
{/if}

<h2>Timers</h2>
{#if timers}
    {#each timers as timer}
        <div class="timer-container">
            <span class="timer-name"> {timer.name}</span>
            <div class="buttons">
                <button
                    class="btn-icon"
                    type="button"
                    on:click={() => deleteTimer(timer.id)}
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
                    on:click={() => startTimer(timer.id)}
                >
                    <Fa icon={faPlay} />
                </button>
            </div>
        </div>
    {/each}

    <button type="button" class="btn-icon" on:click={add}>
        <Fa icon={faAdd} />
    </button>
{/if}
{#if !timers || timers.length == 0}
    <span>No timers</span>
{/if}

<audio
    src="https://freesound.org/data/previews/536/536420_4921277-lq.mp3"
    bind:this={audio}
/>

<style>
    .finished {
        color: #a6adc8;
    }

    h2 {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
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
</style>
