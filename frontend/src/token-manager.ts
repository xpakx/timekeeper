import { tokenStorage } from "./storage";
import { get } from 'svelte/store';
import jwt_decode from 'jwt-decode';
export { getToken };

function getToken(): String {
    let token: String = get(tokenStorage);
    if (!token || token == '') {
        return token;
    }
    try {
        let token_data: any = jwt_decode(token.valueOf());
        let expiration: number = token_data.exp*1000; 
        console.log(expiration);
        console.log(Date.now());
        if (expiration > Date.now()) {
            console.log("unexpired");
            return token;
        }
        return 'refreshed' // TODO
    } catch (_) {
        return token;
    }
}