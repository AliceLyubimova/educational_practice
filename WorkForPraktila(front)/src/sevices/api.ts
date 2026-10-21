const API_BASE_URL = 'http://127.0.0.1:8000/api';
import type {
    UserResponse,
    CandidateInfo,
    PhotoResponse,
    LikeRequest,
    LikeActionResponse,
    MatchResponse,
    RecommendationsResponse,
    RegisterRequest,
    LoginRequest,
    UploadPhotoResponse,
    GetUserPhotosResponse
} from '../types/api';

class ApiService {
    private async request<T>(
        endpoint: string, 
        options?: RequestInit
    ): Promise<T> {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options?.headers,
            },
            ...options,
        });

        if (!response.ok) {
            let errorMessage = 'Ошибка запроса';
            try {
                const error = await response.json();
                errorMessage = error.detail || error.message || errorMessage;
            } catch (e) {
                errorMessage = `HTTP ${response.status}: ${response.statusText}`;
            }
            throw new Error(errorMessage);
        }

        // Для пустых ответов
        if (response.status === 204) {
            return {} as T;
        }

        return response.json();
    }

    private async requestBlob(endpoint: string): Promise<Blob> {
        const response = await fetch(`${API_BASE_URL}${endpoint}`);
        if (!response.ok) {
            throw new Error('Ошибка загрузки изображения');
        }
        return response.blob();
    }

    // АВТОРИЗАЦИЯ
    
    async register(data: RegisterRequest) {
        return this.request<{ user_id: number; email: string; name: string; message: string }>(
            '/register',
            { method: 'POST', body: JSON.stringify(data) }
        );
    }

    async login(data: LoginRequest) {
        return this.request<{ user_id: number; email: string; name: string; message: string }>(
            '/login',
            { method: 'POST', body: JSON.stringify(data) }
        );
    }

    // ПОЛЬЗОВАТЕЛИ
    
    async getUserById(userId: number) {
        return this.request<UserResponse>(`/people/${userId}`);
    }

    async getAllUsers() {
        return this.request<{ users: UserResponse[]; total: number }>('/people');
    }

    async updateUser(userId: number, data: Partial<UserResponse>) {
        return this.request<{ message: string; updated_fields: string[] }>(
            `/people/${userId}`,
            { method: 'PUT', body: JSON.stringify(data) }
        );
    }

    async deleteUser(userId: number) {
        return this.request<{ message: string }>(
            `/people/${userId}`,
            { method: 'DELETE' }
        );
    }

    // ФОТО
    
    async uploadPhoto(userId: number, photoBase64: string, filename?: string) {
        return this.request<UploadPhotoResponse>(
            `/photos/upload/${userId}`,
            { 
                method: 'POST', 
                body: JSON.stringify({ photo_base64: photoBase64, filename }) 
            }
        );
    }

    async getUserPhotos(userId: number) {
        return this.request<GetUserPhotosResponse>(`/photos/user/${userId}`);
    }

    async setAvatar(userId: number, photoId: string) {
        return this.request<{ message: string; photo_id: string }>(
            `/photos/avatar/${userId}`,
            { 
                method: 'PUT', 
                body: JSON.stringify({ photo_id: photoId }) 
            }
        );
    }

    async deletePhoto(userId: number, photoId: string) {
        return this.request<{ message: string }>(
            `/photos/${userId}/${photoId}`,
            { method: 'DELETE' }
        );
    }

    getPhotoUrl(photoId: string): string {
        return `${API_BASE_URL}/photos/${photoId}`;
    }

    async getPhotoBlob(photoId: string): Promise<Blob> {
        return this.requestBlob(`/photos/${photoId}`);
    }

    // ЛАЙКИ 
    
    async like(data: LikeRequest) {
        return this.request<LikeActionResponse>(
            '/like',
            { method: 'POST', body: JSON.stringify(data) }
        );
    }

    async getReceivedLikes(userId: number) {
        return this.request<{ received_likes: CandidateInfo[] }>(
            `/likes/received/${userId}`
        );
    }

    async getGivenLikes(userId: number) {
        return this.request<{ given_likes: CandidateInfo[] }>(
            `/likes/given/${userId}`
        );
    }

    async getMatches(userId: number) {
        return this.request<MatchResponse>(`/matches/${userId}`);
    }

    // СОВМЕСТИМОСТЬ 
    
    async getRecommendations(userId: number, limit: number = 10) {
        return this.request<RecommendationsResponse>(
            `/compatibility/recommendations/${userId}?limit=${limit}`
        );
    }

    async calculateCompatibility(userId: number, candidateIds?: number[]) {
        return this.request<any>(
            '/compatibility/calculate',
            { 
                method: 'POST', 
                body: JSON.stringify({ 
                    user_id: userId, 
                    candidate_ids: candidateIds,
                    use_saved_weights: true 
                }) 
            }
        );
    }

    // МАИ 
    
    

    async calculateWeights(criteria: string[], comparisons: any[]) {
        return this.request<any>(
            '/ahp/calculate',
            { 
                method: 'POST', 
                body: JSON.stringify({ criteria, comparisons }) 
            }
        );
    }

    // ДРУГОГОЙ ПОЛЬЗОВАТЕЛЬ
    async getUserProfileWithPhotos(userId: number) {
        return this.request<UserResponse & { photos: PhotoResponse[] }>(`/profile/${userId}`);
    }

    async getWeights(userId: number) {
        return this.request<{ user_id: number; raw_weights: Record<string, number>; criteria_list: string[] }>(
            `/ahp/weights/${userId}`
        );
    }

    async saveWeights(userId: number, rawWeights: Record<string, number>) {
        return this.request<{ message: string; raw_weights: Record<string, number> }>(
            `/ahp/weights/${userId}`,
            { method: 'PUT', body: JSON.stringify({ weights: rawWeights }) }
        );
    }

    async addComment(userId: number, targetUserId: number, text: string) {
        return this.request<{ id: number; message: string }>('/comments', {
            method: 'POST',
            body: JSON.stringify({ user_id: userId, target_user_id: targetUserId, text }),
        });
    }

    async getComments(targetUserId: number) {
        return this.request<{ comments: Array<{ id: number; user_id: number; user_name: string; text: string; created_at: string }> }>(
            `/comments/${targetUserId}`
        );
    }
}



export const api = new ApiService();
