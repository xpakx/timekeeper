import { writable, type Writable } from 'svelte/store'

const stored = localStorage.token;
export const tokenStorage = <Writable<String>> writable(stored || '');
tokenStorage.subscribe((value) => localStorage.token = value);