<svelte:head>
    <title>Home</title>
</svelte:head>

<script lang="ts">
    import { usernameStorage } from '../storage'; 
    let username: String = "";

	usernameStorage.subscribe(value => {
		username = value;
	});
</script>

{#if username == ""}
    <p>Not logged</p>
{:else}
    <p>Logged as {username}</p>
{/if}