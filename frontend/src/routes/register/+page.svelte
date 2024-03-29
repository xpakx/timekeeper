<script lang="ts">
  import { goto } from "$app/navigation";
  import { refreshStorage, tokenStorage, usernameStorage } from "../../storage";

  let apiUri = "http://localhost:8000";

  let message: String;
  let user = { username: "", password: "", repeated_password: "" };

  async function register() {
    const form = <HTMLFormElement>document.getElementById("register");

    if (form && form.checkValidity()) {
      try {
        let response = await fetch(`${apiUri}/users/register`, {
          method: "POST",
          body: JSON.stringify(user),
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (response.ok) {
          const fromEndpoint = await response.json();
          tokenStorage.set(fromEndpoint.token);
          usernameStorage.set(fromEndpoint.username);
          refreshStorage.set(fromEndpoint.refresh_token);
          console.log("Success");
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
</script>

<svelte:head>
  <title>Register</title>
</svelte:head>

<h2>Register</h2>
<form id="register" autocomplete="on" novalidate>
  <div>
    <label for="username">Username</label>
    <input
      bind:value={user.username}
      required
      placeholder="Username"
      id="username"
    />
  </div>
  <div>
    <label for="password">Password</label>
    <input
      type="password"
      id="password"
      bind:value={user.password}
      required
      placeholder="Password"
    />
  </div>
  <div>
    <label for="password">Confirm password</label>
    <input
      type="password"
      id="password"
      bind:value={user.repeated_password}
      required
      placeholder="Password (again)"
    />
  </div>

  {#if message}
    <p>{message}</p>
  {/if}

  <button type="button" on:click={register}>Register</button>
</form>

<div class="link">
  Already signed up? <a href="/login">Go to login</a>
</div>

<style>
  form {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    background-color: #181825;
    border-radius: 5px;
  }

  form div {
    margin-bottom: 15px;
    width: 100%;
  }

  label {
    display: block;
    font-weight: bold;
    margin-bottom: 5px;
  }

  input {
    width: 100%;
    padding: 10px;
    border: 1px solid #11111b;
    border-radius: 4px;
    box-sizing: border-box;
    font-family: inherit;
    font-size: 14px;
    transition: border-color 0.3s ease;
    background-color: #1e1e2e;
    color: #a6adc8;
  }

  input:focus {
    outline: none;
    border-color: #f2cdcd;
    box-shadow: 0 0 3px #f2cdcd;
  }

  input:hover {
    border-color: #f2cdcd;
  }

  input:disabled {
    background-color: #313244;
    cursor: not-allowed;
  }

  p {
    color: #f38ba8;
    margin-top: 10px;
  }

  button {
    padding: 10px 20px;
    background-color: #9399b2;
    color: #313244;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  button:hover {
    background-color: #7f849c;
  }

  .link {
    color: #7f849c;
    font-size: 14px;
    margin-top: 5px;
  }

  .link a {
    color: #f2cdcd;
  }
</style>
