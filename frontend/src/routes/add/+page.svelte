<svelte:head>
    <title>New timer</title>
</svelte:head>

<script lang="ts">
    import { goto } from '$app/navigation';
    import { getToken } from '../../token-manager';

    let apiUri = "http://localhost:8000";
    let message: String;
    let timer = {name: "", description: "", duration_s: 0, autofinish: false};

    async function addTimer() {
        let token: String = getToken();
        const form = <HTMLFormElement> document.getElementById('new_timer');

        if(!token || token == '' || !form || !form.checkValidity()) {
            return;
        }

        try {
            let response = await fetch(`${apiUri}/timers/`, {
                method: 'POST',
                body: JSON.stringify(timer), 
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                goto("/");
            } else {
                if (response.status == 401) {
                    goto('/logout');
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

<h1>New timer</h1>
<form id="new_timer" autocomplete="on" novalidate>
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
    
    <button type="button" on:click={addTimer}>Add</button>
</form>