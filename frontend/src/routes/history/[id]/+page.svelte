<script lang="ts">
    import { goto } from "$app/navigation";
    import { getToken } from "../../../token-manager";
    import { page } from '$app/stores';
    let apiUri = "http://localhost:8000";
    let message: String;
    let id = Number($page.params.id);
    getHistory();

    let timers: {
        id: number;
        start_time: Date;
        end_time?: Date;
        state: String;
        timer_id: number;
        timer: {
            name: string;
            duration_s: number;
            autofinish: boolean;
        };
    }[];

    async function getHistory() {
        let token: String = await getToken();
        if(!token || token == '') {
            return;
        }

        try {
            let response = await fetch(`${apiUri}/timers/${id}/history`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                let fromEndpoint = await response.json();
                timers = fromEndpoint.map((t: any) => {
                    return {
                        id: t.id,
                        start_time: new Date(t.start_time),
                        end_time: t.end_time
                            ? new Date(t.end_time)
                            : undefined,
                        state: t.state,
                        timer_id: t.timer_id,
                        timer: t.timer
                    };
                });
            } else {
                if (response.status == 401) {
                    goto('/logout');
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
    <title>History</title>
</svelte:head>


{#if timers && timers.length > 0}
    {#each timers as timer}
        <div class="timer-container">
           <span class="timer-name"> {timer.timer.name}</span>
           {timer.state}
        </div>
    {/each}
{/if}