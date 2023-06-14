import { refreshStorage, tokenStorage } from "./storage";
import { get } from 'svelte/store';
import jwt_decode from 'jwt-decode';
import { goto } from "$app/navigation";
export { getToken };
let apiUri = "http://localhost:8000";

async function getToken(): Promise<String> {
    let token: String = get(tokenStorage);
    if (!token || token == '') {
        return Promise.resolve(token);
    }
    try {
        let token_data: any = jwt_decode(token.valueOf());
        let expiration: number = token_data.exp*1000; 
        if (expiration > Date.now()) {
            console.log("unexpired");
            return Promise.resolve(token);
        }
        let new_token = await refreshToken();
        return Promise.resolve(new_token);
    } catch (_) {
        return Promise.resolve(token);
    }
}

async function refreshToken(): Promise<String> {
    let token: String = get(refreshStorage);
    if (!token || token == '') {
        goto("/");
    }
    let body = { 'refresh_token': token};

    try {
        let response = await fetch(`${apiUri}/users/refresh`, {
            method: "POST",
            body: JSON.stringify(body),
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (response.ok) {
            const fromEndpoint = await response.json();
            tokenStorage.set(fromEndpoint.token);
            refreshStorage.set(fromEndpoint.refresh_token);
            return Promise.resolve(fromEndpoint.token);
        } else {
            if (response.status == 401) {
                goto('/logout');
            }
            // TODO
        }
    } catch (err) {
        // TODO
    }
    return Promise.resolve('');
}