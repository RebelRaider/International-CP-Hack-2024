import api from "../http/api.js";

export default class Personality {
    static async uploadCandidateData(formData: any): Promise<any> {
        return api.post('/card/', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
    }

    static async getPersonalityList(limit: number, offset: number): Promise<any> {
        return api.get(`/card/`, { params: { limit, offset } } );
    }
    static async createVacancy(title: string, description:string, salary: number): Promise<any> {
        return api.post(`/vacancy/`, { title, description, salary }, { headers: { 'Content-Type': 'application/json' } } );
    }
    static async getVacancyList(limit: number, offset: number): Promise<any> {
        return api.get(`/vacancy/`, {params:{limit, offset}});
    }
}
