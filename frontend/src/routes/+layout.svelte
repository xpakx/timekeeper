<script lang="ts">
    import { get } from "svelte/store";
    import { usernameStorage } from "../storage";
    import Fa from "svelte-fa";
    import {
    faBox,
    faGift,
        faHistory,
        faHourglass,
        faShield,
        faSignOut,
    } from "@fortawesome/free-solid-svg-icons";

    let username: String = get(usernameStorage);
    usernameStorage.subscribe((value) => {
        username = value;
    });
</script>

<nav>
    <div class="nav-component">
        <a href="/"><Fa icon={faHourglass} /></a>
        <a href="/history"><Fa icon={faHistory} /></a>
        <a href="/reward"><Fa icon={faGift} /></a>
        <a href="/equipment"><Fa icon={faBox} /></a>
        <a href="/heroes"><Fa icon={faShield} /></a>
    </div>
    <div class="nav-component">
        <div class="user">
            {#if username == ""}
                Not logged,
                <a href="/login">log in</a>
            {:else}
                Logged as <strong>{username}</strong>.
                <a href="/logout" class="log-out"><Fa icon={faSignOut} /></a>
            {/if}
        </div>
    </div>
</nav>

<slot />

<style>
    nav {
        display: flex;
        justify-content: space-between;
        margin: 0 10px;
        margin-bottom: 15px;
    }
    nav a {
        font-size: 14px;
        cursor: pointer;
        color: #7f849c;
        margin-right: 10px;
    }

    nav a:last-child {
        margin-right: 0;
    }

    nav a.log-out {
        color: #f2cdcd;
    }

    .nav-component {
        display: flex;
        align-items: center;
    }

    .user strong {
        color: #a6adc8;
        font-weight: bold;
    }
</style>
