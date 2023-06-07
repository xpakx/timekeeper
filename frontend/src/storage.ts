import { writable, type Writable } from 'svelte/store'
import { browser } from '$app/environment';

const stored = browser ? localStorage.token : '';
export const tokenStorage = <Writable<String>> writable(stored || '');

if (browser) {
    tokenStorage.subscribe((value) => localStorage.token = value);
}