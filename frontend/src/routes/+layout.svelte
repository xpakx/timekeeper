<script lang="ts">
    import { get } from "svelte/store";
    import { usernameStorage } from "../storage";
    import Fa from "svelte-fa";
    import { faSignOut } from "@fortawesome/free-solid-svg-icons";

    let username: String = get(usernameStorage);
    usernameStorage.subscribe((value) => {
        username = value;
    });
</script>

<nav>
    <div>
        <a href="/">timers</a>
        <a href="/history">history</a>
    </div>
    <div class="user">
        {#if username == ""}
            <p>
                Not logged,
                <a href="/login">log in</a>
            </p>
        {:else}
            <p>
                Logged as {username}.
                <a href="/logout"><Fa icon={faSignOut} /></a>
            </p>
        {/if}
    </div>
</nav>

<slot />

<style>
    nav {
        display: flex;
        justify-content: space-between;
        margin: 0 10px;
    }
    nav a {
        font-size: 14px;
        cursor: pointer;
        color: #7f849c;
    }
</style>
