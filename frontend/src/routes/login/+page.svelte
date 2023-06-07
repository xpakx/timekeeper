<svelte:head>
    <title>Login</title>
</svelte:head>

<script lang="ts">
    import { goto } from '$app/navigation';
    import { tokenStorage } from '../../storage'; 

    let apiUri = "http://localhost:8000";

    let message: String;
    let user = {username: "", password: ""};

    async function login() {
        const form = <HTMLFormElement> document.getElementById('login');

        if (form && form.checkValidity()) {
            try {
                let response = await fetch(`${apiUri}/users/login`, {
                    method: 'POST',
                    body: JSON.stringify(user), 
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                if (response.ok) {
                    const fromEndpoint = await response.json();
                    tokenStorage.set(fromEndpoint.token);
                    console.log("Success");
                    goto('/')
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

<h1>Login</h1>
<form id="login" autocomplete="on" novalidate>
    <div>
        <label for="username">Username</label>
        <input 
        bind:value={user.username} 
        required placeholder="Username" 
        id="username"/>
    </div>
    <div>
        <label for="password">Password</label>
        <input type="password" 
        id="password" 
        bind:value={user.password} 
        required 
        placeholder="Password" />
    </div>
    
    {#if message}
        <p>{message}</p>
    {/if}
    
    <button type="button" on:click={login}>Login</button>
</form>