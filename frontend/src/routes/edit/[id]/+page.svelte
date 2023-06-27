<script lang="ts">
    import { goto } from "$app/navigation";
    import { page } from "$app/stores";
    import { getToken } from "../../../token-manager";
    let id = Number($page.params.id);
    let apiUri = "http://localhost:8000";
    let message: String;
    let timer = {
        id: 0,
        name: "",
        description: "",
        duration_s: 0,
        autofinish: false,
        rewarded: false,
    };
    getTimer(id);

    async function editTimer() {
        let token: String = await getToken();
        const form = <HTMLFormElement>document.getElementById("edit_timer");
        if (!token || token == "" || !form || !form.checkValidity()) {
            return;
        }

        try {
            let response = await fetch(`${apiUri}/timers/${id}`, {
                method: "PUT",
                body: JSON.stringify(timer),
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                goto("/");
            } else {
                if (response.status == 401) {
                    goto("/logout");
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

    async function getTimer(id: number) {
        let token: String = await getToken();

        if (!token || token == "") {
            return;
        }

        try {
            let response = await fetch(`${apiUri}/timers/${id}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                timer = await response.json();
            } else {
                if (response.status == 401) {
                    goto("/logout");
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

<svelte:head>
    <title>Edit timer</title>
</svelte:head>

<h1>Edit timer</h1>
<form id="edit_timer" autocomplete="on" novalidate>
    <div>
        <label for="name">Name</label>
        <input bind:value={timer.name} required placeholder="Name" id="name" />
    </div>
    <div>
        <label for="description">Description</label>
        <input
            bind:value={timer.description}
            required
            placeholder="Description"
            id="description"
        />
    </div>
    <div>
        <label for="duration_s">Duration</label>
        <input
            bind:value={timer.duration_s}
            required
            placeholder="Duration"
            id="duration_s"
        />
    </div>
    <div class="checkbox-container">
        <input
            type="checkbox"
            bind:checked={timer.autofinish}
            id="autofinish"
        />
        <label for="autofinish" class="checkbox-label">
            <div class="checkbox" />
            Autofinish
        </label>
    </div>
    
    <div class="checkbox-container">
        <input
            type="checkbox"
            bind:checked={timer.rewarded}
            id="reward"
        />
        <label for="reward" class="checkbox-label">
            <div class="checkbox" />
            Reward for timer
        </label>
    </div>

    {#if message}
        <p>{message}</p>
    {/if}

    <button type="button" on:click={editTimer}>Save</button>
</form>

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

    .checkbox-container label {
        display: flex;
        align-items: start;
    }

    .checkbox-label {
        color: #a6adc8;
        font-size: 14px;
    }

    .checkbox {
        position: relative;
        width: 16px;
        height: 16px;
        border: 1px solid #11111b;
        border-radius: 3px;
        transition: border-color 0.3s ease;
        background-color: #1e1e2e;
        margin-right: 10px;
        cursor: pointer;
    }

    .checkbox:before {
        content: "";
        position: absolute;
        top: 3px;
        left: 3px;
        width: 10px;
        height: 10px;
        border-radius: 2px;
        background-color: #f2cdcd;
        opacity: 0;
        transition: all 0.3s ease;
    }

    input[type="checkbox"]:checked + label .checkbox:before {
        opacity: 1;
    }

    input[type="checkbox"] {
        display: none;
    }

    .checkbox:hover {
        border-color: #f2cdcd;
    }

    .checkbox:hover:before {
        border-radius: 5px;
    }

    .checkbox:focus {
        outline: none;
        box-shadow: 0 0 3px #f2cdcd;
    }
</style>
