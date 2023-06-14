<svelte:head>
    <title>Register</title>
</svelte:head>

<script lang="ts">
    import { goto } from '$app/navigation';
    import { refreshStorage, tokenStorage, usernameStorage } from '../../storage'; 

    let apiUri = "http://localhost:8000";

    let message: String;
    let user = {username: "", password: "", repeated_password: ""};

    async function register() {
        const form = <HTMLFormElement> document.getElementById('register');

        if (form && form.checkValidity()) {
            try {
                let response = await fetch(`${apiUri}/users/register`, {
                    method: 'POST',
                    body: JSON.stringify(user), 
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                if (response.ok) {
                    const fromEndpoint = await response.json();
                    tokenStorage.set(fromEndpoint.token);
                    usernameStorage.set(fromEndpoint.username);
                    refreshStorage.set(fromEndpoint.refresh_token);
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

<h1>Register</h1>
<form id="register" autocomplete="on" novalidate>
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
    <div>
        <label for="password">Confirm password</label>
        <input 
        type="password" 
        id="password" 
        bind:value={user.repeated_password} 
        required 
        placeholder="Password (again)" />
    </div>
    
    {#if message}
        <p>{message}</p>
    {/if}
    
    <button type="button" on:click={register}>Register</button>
</form>