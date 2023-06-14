<svelte:head>
    <title>Register</title>
</svelte:head>

<script lang="ts">
    import { goto } from '$app/navigation';
    import { tokenStorage, usernameStorage } from '../../storage'; 

    tokenStorage.set('');
    usernameStorage.set('');
    goto('/');

</script>