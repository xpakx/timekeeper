<script lang="ts">
    import { tokenStorage } from "../storage";
    import { goto } from "$app/navigation";
    import { tweened } from "svelte/motion";
    import { getToken } from "../token-manager";
    import Fa from "svelte-fa";
    import {
        faAdd,
        faArrowLeft,
        faArrowRight,
    } from "@fortawesome/free-solid-svg-icons";
    import { onDestroy } from "svelte";
    import Timer from "../components/Timer.svelte";
    import RunningTimer from "../components/RunningTimer.svelte";
    import type { TimerDetails } from "../types/TimerDetails";
    import type { RunningTimerDetails } from "../types/RunningTimerDetails";
    import InfoBar from "../components/InfoBar.svelte";
    import type { Item } from "../types/Item";

    let apiUri = "http://localhost:8000";
    let message: String;
    let page: number = 0;
    let date = tweened(Date.now(), { duration: 500 });
    let timer_interval = setInterval(() => {
        $date = Date.now();
        testTimers();
    }, 500);
    let audio: HTMLAudioElement;

    let timers: TimerDetails[];
    let running_timers: RunningTimerDetails[];

    tokenStorage.subscribe((_) => {
        getAllTimers();
        getActiveTimers();
    });

    onDestroy(() => {
        clearInterval(timer_interval);
    });

    async function getAllTimers(new_page: number = 0) {
        if (new_page < 0) {
            return;
        }

        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        try {
            let response = await fetch(
                `${apiUri}/timers/${new_page > 0 ? "?page=" + new_page : ""}`,
                {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

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
                    infoBar.addInfo({points: points});
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
            } else if(
                t.reward_time && 
                $date -t.start_time.getTime() > t.reward_time &&
                $date - t.start_time.getTime() - 500 <= t.reward_time
                ) {
                    generateReward(t.id);

            }
        });
    }

    async function generateReward(id: number) {
        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        try {
            let response = await fetch(
                `${apiUri}/timers/instances/${id}/reward`,
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
                let reward: Item = fromEndpoint;
                infoBar.addInfo({reward: reward});
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

    let infoBar: InfoBar;
</script>

<svelte:head>
    <title>Home</title>
</svelte:head>

<InfoBar bind:this={infoBar} />

{#if running_timers && running_timers.length > 0}
    <h2>Running</h2>

    {#each running_timers as timer}
        <RunningTimer
            bind:date={$date}
            {timer}
            on:state={(event) => changeTimerState(timer.id, event.detail.state)}
        />
    {/each}
{/if}

<h2>Timers</h2>
{#if timers}
    {#each timers as timer}
        <Timer
            {timer}
            on:delete={() => deleteTimer(timer.id)}
            on:start={() => startTimer(timer.id)}
        />
    {/each}
{/if}
{#if !timers || timers.length == 0}
    <span>No timers</span>
{/if}

<div class="page-nav">
    <button
        class="btn-icon"
        on:click={() => getAllTimers(page - 1)}
        disabled={page <= 0}
    >
        <Fa icon={faArrowLeft} />
    </button>
    <button type="button" class="btn-icon" on:click={add}>
        <Fa icon={faAdd} />
    </button>
    <button
        class="btn-icon"
        on:click={() => getAllTimers(page + 1)}
        disabled={!timers || timers.length < 20}
    >
        <Fa icon={faArrowRight} />
    </button>
</div>

<audio
    src="https://freesound.org/data/previews/536/536420_4921277-lq.mp3"
    bind:this={audio}
/>

<style>
    h2 {
        font-size: 24px;
        font-weight: bold;
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

    button.btn-icon {
        border-radius: 7px;
    }

    button.btn-icon:disabled {
        background-color: #313244;
        color: #585b70;
    }
</style>
