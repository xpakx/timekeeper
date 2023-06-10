<script lang="ts">
    import { get } from "svelte/store";
    import { tokenStorage, usernameStorage } from "../storage";
    import { goto } from "$app/navigation";
    import { tweened } from "svelte/motion"
    let username: String = get(usernameStorage);
    let apiUri = "http://localhost:8000";
    let message: String;
    let date = tweened(Date.now(), {duration: 500});
    setInterval(() => {
        $date = Date.now();
    }, 500);

    let timers: {
        id: number;
        name: String;
        description: String;
        duration_s: number;
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
	};
    }[];

    usernameStorage.subscribe((value) => {
        username = value;
        getAllTimers();
        getActiveTimers();
    });

    async function getAllTimers() {
        let token: String = get(tokenStorage);
        if (token) {
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
                    const errorBody = await response.json();
                    message = errorBody.detail;
                }
            } catch (err) {
                if (err instanceof Error) {
                    message = err.message;
                }
            }
        }
    }

    async function getActiveTimers() {
        let token: String = get(tokenStorage);
        if (token) {
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
                            end_time: t.end_time
                                ? new Date(t.end_time)
                                : undefined,
                            state: t.state,
                            timer_id: t.timer_id,
                            timer: t.timer
                        };
                    });
                } else {
                    const errorBody = await response.json();
                    message = errorBody.detail;
                }
            } catch (err) {
                if (err instanceof Error) {
                    message = err.message;
                }
            }
        }
    }

    function add() {
        goto("/add");
    }

    async function deleteTimer(id: number) {
        let token: String = get(tokenStorage);
        if (token) {
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
                    const errorBody = await response.json();
                    message = errorBody.detail;
                }
            } catch (err) {
                if (err instanceof Error) {
                    message = err.message;
                }
            }
        }
    }

    async function startTimer(id: number) {
        let token: String = get(tokenStorage);
        if (token) {
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
                    const errorBody = await response.json();
                    message = errorBody.detail;
                }
            } catch (err) {
                if (err instanceof Error) {
                    message = err.message;
                }
            }
        }
    }

    async function changeTimerState(id: number, state: String) {
        let token: String = get(tokenStorage);
        let body = {
            "state": state
        };
        if (token) {
            try {
                let response = await fetch(`${apiUri}/timers/instances/${id}/state`, {
                    method: "POST",
                    body: JSON.stringify(body),
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                });

                if (response.ok) {
                    running_timers = running_timers.filter((a) => a.id != id);
                } else {
                    const errorBody = await response.json();
                    message = errorBody.detail;
                }
            } catch (err) {
                if (err instanceof Error) {
                    message = err.message;
                }
            }
        }
    }
</script>

<svelte:head>
    <title>Home</title>
</svelte:head>

{#if username == ""}
    <p>Not logged, <a href="/login">log in</a></p>
{:else}
    <p>Logged as {username}</p>
{/if}

{#if running_timers && running_timers.length > 0}
    <h2>Running</h2>

    {#each running_timers as timer}
        <div>
            {timer.timer.name}
            <progress value={(($date - timer.start_time.getTime())/(1000*timer.timer.duration_s))}></progress>
            <button type="button" on:click={() => changeTimerState(timer.id, "cancelled")}>
                cancel
            </button>
            <button type="button" on:click={() => changeTimerState(timer.id, "failed")}>
                fail
            </button>
        </div>
    {/each}
{/if}

<h2>Timers</h2>
{#if timers}
    {#each timers as timer}
        <div>
            {timer.name}
            <button type="button" on:click={() => deleteTimer(timer.id)}
                >delete</button
            >
            <button type="button" on:click={() => goto(`/edit/${timer.id}`)}
                >edit</button
            >
            <button type="button" on:click={() => startTimer(timer.id)}
                >start</button
            >
        </div>
    {/each}

    <button type="button" on:click={add}>Add</button>
{/if}
{#if !timers || timers.length == 0}
    <span>No timers</span>
{/if}
