
import AuthService from "../services/AuthService";
import Personality from "../services/Personality";

export default class Store {
    isAuth = false;
    isLoading = false;
    isPersonality = []
    isPersonalityList = []
    isVacancyList = []

    setAuth(bool:boolean){
        this.isAuth = bool;
    }

    setLoading(bool: boolean){
        this.isLoading = bool;
    }

    setPersonality(data: any){
        this.isPersonality = data;
    }

    setPersonalityList(data: any){
        this.isPersonalityList = data;
    }

    setVacancyList(data: any){
        this.isVacancyList = data;
    }

    async login(username:string,password:string){
        this.setLoading(true);
        try {
            const response = await AuthService.login(username, password);
            localStorage.setItem('token', response.data.access_token);
            this.setAuth(true);
        } catch(e) {
            console.log('Error login', e);
        } finally {
            this.setLoading(false);
        }
    }
    async registration(username:string,password:string){
        try {
            const response = await AuthService.registration(username, password);
            localStorage.setItem('token', response.data.access_token);
            this.setAuth(true);
        } catch(e) {
            console.log('Error registration', e);
        }
    }
    async uploadCandidateData(formData: any){
        try {
            const response = await Personality.uploadCandidateData(formData);
            this.setPersonality(response.data);
            return response.data;
        } catch(e) {
            console.log('Error upload candidate data', e);
        }
}
    async getPersonalityList(limit: number, offset: number){
        try {
            const response = await Personality.getPersonalityList(limit, offset);
            this.setPersonalityList(response.data);
            return response.data;
        } catch(e) {
            console.log('Error get personality', e);
        }
    }
    async createVacancy(title: string, description: string, salary: number){
        try {
            const response = await Personality.createVacancy(title, description, salary);
            return response.data;
        } catch(e) {
            console.log('Error create vacancy', e);
        }
    }

    async getVacancyList(limit: number, offset: number){
        try {
            const response = await Personality.getVacancyList(limit, offset);
            this.setVacancyList(response.data);
            return response.data;
        } catch(e){
            console.log('Error get vacancy list', e);
        }
    }
}