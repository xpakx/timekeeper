<svelte:head>
    <title>Home</title>
</svelte:head>

<script lang="ts">
    import { get } from 'svelte/store';
    import { tokenStorage, usernameStorage } from '../storage'; 
    import { goto } from '$app/navigation';
    let username: String = get(usernameStorage);
    let apiUri = "http://localhost:8000";
    let message: String;

    let timers: { id: number, name: String, description: String, duration_s: number }[];
    let running_timers: { 
        id: number,
        start_time: Date,
        end_time?: Date,
        state: String,
        timer_id: number 
    }[];

	usernameStorage.subscribe(value => {
		username = value;
        getAllTimers();
        getActiveTimers();
	});


    async function getAllTimers() {
        let token: String = get(tokenStorage);
        if(token) {
            try {
                let response = await fetch(`${apiUri}/timers/`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
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
        if(token) {
            try {
                let response = await fetch(`${apiUri}/timers/active`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    running_timers = await response.json();

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
        if(token) {
            try {
                let response = await fetch(`${apiUri}/timers/${id}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
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
        if(token) {
            try {
                let response = await fetch(`${apiUri}/timers/${id}/instances`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    let new_timer = await response.json();
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
</script>

{#if username == ""}
    <p>Not logged, <a href="/login">log in</a></p>
{:else}
    <p>Logged as {username}</p>

{/if}

{#if running_timers && running_timers.length > 0}
    <h2>Running</h2>

    {#each running_timers as timer}
        <div>
            {timer.state}

        </div>
    {/each}
{/if}

<h2>Timers</h2>
{#if timers}
    {#each timers as timer}
        <div>
            {timer.name}
            <button type="button" on:click={() => deleteTimer(timer.id)}>delete</button>
            <button type="button" on:click={() => goto(`/edit/${timer.id}`)}>edit</button>
            <button type="button" on:click={() => startTimer(timer.id)}>start</button>
        </div>
    {/each}

    <button type="button" on:click={add}>Add</button>
{/if}
{#if !timers || timers.length == 0}
    <span>No timers</span>
{/if}