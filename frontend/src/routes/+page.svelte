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

	usernameStorage.subscribe(value => {
		username = value;
        getAllTimers();
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
</script>

{#if username == ""}
    <p>Not logged, <a href="/login">log in</a></p>
{:else}
    <p>Logged as {username}</p>

{/if}


{#if timers}
    <h2>Timers</h2>
    {#each timers as timer}
        <div>
            {timer.name}
            <button type="button" on:click={() => deleteTimer(timer.id)}>delete</button>
        </div>
    {/each}
    {#if !timers || timers.length == 0}
        <span>No timers</span>
    {/if}

    <button type="button" on:click={add}>Add</button>
{/if}