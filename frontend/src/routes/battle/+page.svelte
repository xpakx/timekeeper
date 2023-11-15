<script lang="ts">
    import { goto } from "$app/navigation";
    import { getToken } from "../../token-manager";
    import type { Battle } from "../../types/Battle";
    import BattleCard from "../../components/BattleCard.svelte";
    import type { MoveResponse, PostTurn, SkillResult, StageChange, StatusChange } from "../../types/MoveResponse";
    import type { UserHeroBattle } from "../../types/UserHeroBattle";
    import HeroCard from "../../components/HeroCard.svelte";
    let apiUri = "http://localhost:8000";
    let message: String;
    getCurrentBattle();
    let battle: Battle = {
        id: 1,
        finished: false,
        hero: {
            id: 1,
            incubated: false,
            hp: 10,
            current_hp: 50,
            damage: 5,
            level: 1,
            hero: {
                id: 1,
                name: "Bulbasaur",
                title: "",
                num: 1,
                rarity: "rare",
                hero_type: "grass",
                secondary_hero_type: "poison",
            },
            skillset: [
                {
                    id: 1,
                    name: "Tackle",
                    priority: 0,
                    accuracy: 100,
                    power: 35,
                    max_usages: 35,
                    move_type: "normal",
                    move_category: "physical",
                },
                {
                    id: 2,
                    name: "Growl",
                    priority: 0,
                    accuracy: 100,
                    power: 0,
                    max_usages: 40,
                    move_type: "normal",
                    move_category: "physical",
                },
                {
                    id: 1,
                    name: "Leech Seed",
                    priority: 0,
                    accuracy: 90,
                    power: 0,
                    max_usages: 10,
                    move_type: "grass",
                    move_category: "physical",
                },
                {
                    id: 1,
                    name: "Vine Whip",
                    priority: 0,
                    accuracy: 100,
                    power: 35,
                    max_usages: 10,
                    move_type: "grass",
                    move_category: "physical",
                },
            ],
        },
        enemy: {
            id: 2,
            incubated: false,
            current_hp: 9,
            level: 1,
            hero: {
                id: 2,
                name: "Charmander",
                title: "",
                num: 4,
                rarity: "rare",
                hero_type: "fire",
            },
        },
    };

    let battleMessages: String[] = [];

    async function getCurrentBattle() {
        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        try {
            let response = await fetch(`${apiUri}/battles`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                let fromEndpoint = await response.json();
                battle = fromEndpoint;
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

    async function makeMove(num: number) {
        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        let body = {
            id: num,
            move: "skill",
        };
        try {
            let response = await fetch(`${apiUri}/battles/${battle.id}`, {
                method: "POST",
                body: JSON.stringify(body),
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                let result: MoveResponse = await response.json();
                applyChanges(result);
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

    async function flee() {
        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        let body = {
            move: "flee",
        };
        try {
            let response = await fetch(`${apiUri}/battles/${battle.id}`, {
                method: "POST",
                body: JSON.stringify(body),
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                let fromEndpoint = await response.json();
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

    async function useItem(id: number) {
        let token: String = await getToken();
        if (!token || token == "") {
            return;
        }

        let body = {
            id: id,
            move: "item",
        };
        try {
            let response = await fetch(`${apiUri}/battles/${battle.id}`, {
                method: "POST",
                body: JSON.stringify(body),
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                let fromEndpoint = await response.json();
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

    function applyChanges(changes: MoveResponse) {
        if (changes.hero_first) {
            applyTurn(changes.turn.first, battle.hero.hero.name, battle.enemy.hero.name);
            applyPostTurn(changes.turn.first_changes, battle.hero.hero.name, battle.enemy.hero.name);
            applyTurn(changes.turn.second, battle.enemy.hero.name, battle.hero.hero.name);
            applyPostTurn(changes.turn.second_changes, battle.enemy.hero.name, battle.hero.hero.name);
        } else {
            applyTurn(changes.turn.first, battle.enemy.hero.name, battle.hero.hero.name);
            applyPostTurn(changes.turn.first_changes, battle.enemy.hero.name, battle.hero.hero.name);
            applyTurn(changes.turn.second, battle.hero.hero.name, battle.enemy.hero.name);
            applyPostTurn(changes.turn.second_changes, battle.hero.hero.name, battle.enemy.hero.name);
        }
    }

    function applyTurn(result: SkillResult, firstName: String, secondName: String) {
        if (!result.skill && !result.status_skill) {
            return;
        }
        battleMessages.push(`${firstName} used ${result.name}.`);

        if (!result.able.able) {
            if (result.able.reason == "paralyzed") {
                battleMessages.push(`${firstName} is paralyzed! It can't move!`);
            }
            else if (result.able.reason == "asleep") {
                battleMessages.push(`${firstName} is fast asleep!`);
            }
            else if (result.able.reason == "frozen") {
                battleMessages.push(`${firstName} is frozen solid!`);
            }
            return;
        }
        if (result.missed) {
            battleMessages.push(`${firstName}'s attack missed!`);
            return;
        }
        if (result.skill) {
            if (result.skill.critical) {
                battleMessages.push("A critical hit!")
            }
            if (result.skill.effectiveness == 0) {
                battleMessages.push(`It doesn't affect ${secondName}.`);
            }
            else if (result.skill.effectiveness < 1) {
                battleMessages.push("It's not very effective…")
            }
            else if (result.skill.effectiveness > 1) {
                battleMessages.push("It's super effective!")
            }
            // apply result.skill.damage;
            for (let status of result.skill.secondary_status_changes) {
                applyEffect(secondName, status, true);
            }
        } else if (result.status_skill) {
            let name = result.self_targetted ? firstName : secondName;
            for (let status of result.status_skill.status_changes) {
                applyEffect(name, status);
            }
            for (let stage of result.status_skill.stage_changes) {
                applyStage(name, stage);
            }
            
        }
        if (result.fainted) {
            battleMessages.push(`${firstName} fainted!`);
        }
        if (result.second_fainted) {
            battleMessages.push(`${secondName} fainted!`);
        }
    }

    function applyEffect(name: String, status: StatusChange, side_effect: boolean = false) {
        if (status.effect == 'immune' && !side_effect) {
            battleMessages.push(`It doesn't affect ${name}…`);
            return;
        }
        if (status.effect == 'affected' && !side_effect) {
            battleMessages.push(`${name} is already ${status.status}…`);
            return;
        }
        if (status.effect == 'missed' && !side_effect) {
            battleMessages.push('…but it failed.');
            return;
        }
        if (status.status == "asleep") {
            battleMessages.push(`${name} fell asleep!`);
        } else if (status.status == "paralyzed") {
            battleMessages.push(`${name} is paralyzed! It may be unable to move!`);
        } else if (status.status == "frozen") {
            battleMessages.push(`${name} was frozen solid!`);
        } else if (status.status == "poisoned") {
            battleMessages.push(`${name} was poisoned!`);
        } else if (status.status == "burn") {
            battleMessages.push(`${name} was sustained a burn!`);
        } else if (status.status == "leech seed") {
            battleMessages.push(`${name} was seeded!`);
        }
    }

    function applyStage(name: String, stage: StageChange) {
        if (stage.change > 2) {
            battleMessages.push(`${name}'s ${stage.stage} rose drastically!`);
        } else if (stage.change == 2) {
            battleMessages.push(`${name}'s ${stage.stage} rose sharply!`);
        } else if (stage.change == 1) {
            battleMessages.push(`${name}'s ${stage.stage} rose!`);
        } else if (stage.change == -1) {
            battleMessages.push(`${name}'s ${stage.stage} fell!`);
        } else if (stage.change == -2) {
            battleMessages.push(`${name}'s ${stage.stage} harshly fell!`);
        } else {
            battleMessages.push(`${name}'s ${stage.stage} severely fell!`);
        }
    }
    
    function applyPostTurn(result: PostTurn, firstName: String, secondName: String) {
        for (let effect of result.changes) {
            applyPostEffect(firstName, effect.reason, effect.status_end)
        }
        if (result.fainted) {
            battleMessages.push(`${firstName} fainted!`);
        }
        if (result.second_fainted) {
            battleMessages.push(`${secondName} fainted!`);
        }
    }

    function applyPostEffect(name: String, status: String, status_end: boolean) {
        if (status == "asleep" && status_end) {
            battleMessages.push(`${name} woke up!`);
        } else if (status == "frozen" && status_end) {
            battleMessages.push(`${name} thawed out!`);
        } else if (status == "poisoned") {
            battleMessages.push(`${name} is hurt by poison!`);
        } else if (status == "burn") {
            battleMessages.push(`${name} is hurt by its burn!`);
        } else if (status == "leech seed") {
            battleMessages.push(`The ${name}'s health is sapped by leech seed!`);
        }
    }
</script>

<svelte:head>
    <title>Battle</title>
</svelte:head>

{#if battle}
    <BattleCard
        {battle}
        on:skill={(event) => makeMove(event.detail.num)}
        on:item={(event) => useItem(event.detail.id)}
        on:flee={flee}
    />
{:else}
    <div>No active battle</div>
{/if}

<style>
</style>
