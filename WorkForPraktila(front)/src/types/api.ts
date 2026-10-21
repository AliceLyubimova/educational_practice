// СУЩЕСТВУЮЩИЕ ТИПЫ 
export interface UserResponse {
    id: number;
    email: string;
    name: string;
    age: number;
    gender: string;
    looking_for: string;
    city: string;
    bio?: string;
    avatar?: string;
    avatar_url?: string;
    income: number;
    appearance: number;
    education: string;
    religion: string;
    kindness: number;
    interests: string[];
    is_active?: boolean;
}

export interface CandidateInfo {
    candidate_id: number;
    candidate_name: string;
    candidate_age?: number;
    candidate_city?: string;
    candidate_avatar?: string;
    compatibility_score: number;
    best_criterion?: string;
    worst_criterion?: string;
    average_similarity?: number;
}

export interface PhotoResponse {
    photo_id: string;
    filename: string;
    file_size: number;
    content_type: string;
    uploaded_at: string;
    is_avatar: boolean;
    url: string;
}

export interface LikeRequest {
    from_user_id: number;
    to_user_id: number;
}

export interface LikeActionResponse {
    status: string;
    is_match: boolean;
    compatibility_score: number | null;
    message: string;
}

export interface MatchResponse {
    matches: CandidateInfo[];
}

export interface RecommendationsResponse {
    user_id: number;
    recommendations: CandidateInfo[];
    total_candidates: number;
}

export interface RegisterRequest {
    email: string;
    password: string;
    name: string;
    age: number;
    gender: 'male' | 'female';
    looking_for: 'male' | 'female';
    city: string;
    bio?: string;
}

export interface LoginRequest {
    email: string;
    password: string;
}

export interface UploadPhotoResponse {
    photo_id: string;
    message: string;
    url: string;
}

export interface GetUserPhotosResponse {
    photos: PhotoResponse[];
    count: number;
}

export interface UpdateUserRequest {
    name?: string;
    age?: number;
    gender?: 'male' | 'female';
    looking_for?: 'male' | 'female';
    city?: string;
    bio?: string;
    income?: number;
    appearance?: number;
    education?: string;
    religion?: string;
    kindness?: number;
    interests?: string[];
}

export interface ApiError {
    detail?: string;
    message?: string;
}

export interface FullUserProfile extends UserResponse {
    photos: PhotoResponse[];
}
