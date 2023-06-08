import { writable, type Writable } from 'svelte/store'
import { browser } from '$app/environment';

const storedToken = browser ? localStorage.token : '';
export const tokenStorage = <Writable<String>> writable(storedToken || '');
const storedUsername = browser ? localStorage.username : '';
export const usernameStorage = <Writable<String>> writable(storedUsername || '');

if (browser) {
    tokenStorage.subscribe((value) => localStorage.token = value);
    usernameStorage.subscribe((value) => localStorage.username = value);
}