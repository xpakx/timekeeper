<script lang="ts">
    import { goto } from "$app/navigation";
    import { get } from "svelte/store";
    import { usernameStorage } from "../storage";

    let username: String = get(usernameStorage);
    usernameStorage.subscribe((value) => {
        username = value;
    });

    function logout() {
        goto("/logout");
    }

</script>
<nav>
    {#if username == ""}
        <p>Not logged, <a href="/login">log in</a></p>
    {:else}
        <p>Logged as {username}</p>
        <button type="button" on:click={logout}>log out</button>
    {/if}
</nav>

<style>

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
</style>

<slot></slot>