<svelte:head>
    <title>Register</title>
</svelte:head>

<script lang="ts">
    import { goto } from '$app/navigation';
    import { refreshStorage, tokenStorage, usernameStorage } from '../../storage'; 

    tokenStorage.set('');
    usernameStorage.set('');
    refreshStorage.set('');
    goto('/');

</script>