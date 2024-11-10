import api from "../http/api.js";

export default class AuthService {
    static async login(username: string, password: string): Promise<any> {//+
        return api.post('/auth/token', { username, password }, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } });//+
    }
    static async registration(username: string, password: string): Promise<any> {
        return api.post('/auth/register',{username, password}, {headers: {'Content-Type': 'application/json'}});
    }
}