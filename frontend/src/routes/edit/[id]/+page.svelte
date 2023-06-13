<svelte:head>
    <title>Edit timer</title>
</svelte:head>

<script lang="ts">
    import { get } from 'svelte/store';
    import { tokenStorage } from '../../../storage'; 
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';
    let id = Number($page.params.id);
    let apiUri = "http://localhost:8000";
    let message: String;
    let timer = {id: 0, name: "", description: "", duration_s: 0, autofinish: false};
    getTimer(id);

    async function editTimer() {
        let token: String = get(tokenStorage);
        const form = <HTMLFormElement> document.getElementById('edit_timer');

        if(token && form && form.checkValidity()) {
            try {
                let response = await fetch(`${apiUri}/timers/${id}`, {
                    method: 'PUT',
                    body: JSON.stringify(timer), 
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    goto("/");
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

    async function getTimer(id: number) {
        let token: String = get(tokenStorage);

        if(token) {
            try {
                let response = await fetch(`${apiUri}/timers/${id}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    timer = await response.json();
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

<h1>Edit timer</h1>
<form id="edit_timer" autocomplete="on" novalidate>
    <div>
        <label for="name">Name</label>
        <input 
        bind:value={timer.name} 
        required placeholder="Name" 
        id="name"/>
    </div>
    <div>
        <label for="description">Description</label>
        <input 
        bind:value={timer.description} 
        required placeholder="Description" 
        id="description"/>
    </div>
    <div>
        <label for="duration_s">Duration</label>
        <input 
        bind:value={timer.duration_s} 
        required placeholder="Duration" 
        id="duration_s"/>
    </div>
    <div>
        <label for="autofinish">Autofinish</label>
        <input type=checkbox bind:checked={timer.autofinish} id="autofinish">
    </div>
    
    {#if message}
        <p>{message}</p>
    {/if}
    
    <button type="button" on:click={editTimer}>Save</button>
</form>