from application.dto.requests import (
    RegisterRequest,
    LoginRequest,
    UpdateUserRequest,
    CriteriaComparison,
    CalculateWeightsRequest,
    SaveWeightsRequest,
    CompatibilityRequest,
    LikeRequest,
)

from application.dto.responses import (
    UserResponse,
    UserListResponse,
    AuthResponse,
    WeightsResponse,
    SavedWeightsResponse,
    CandidateInfo,
    CompatibilityResponse,
    RecommendationsResponse,
    LikeInfoResponse,
    LikesListResponse,
    LikeActionResponse,
    MatchResponse,
)

__all__ = [
    # Requests
    "RegisterRequest",
    "LoginRequest",
    "UpdateUserRequest",
    "CriteriaComparison",
    "CalculateWeightsRequest",
    "SaveWeightsRequest",
    "CompatibilityRequest",
    "LikeRequest",
    # Responses
    "UserResponse",
    "UserListResponse",
    "AuthResponse",
    "WeightsResponse",
    "SavedWeightsResponse",
    "CandidateInfo",
    "CompatibilityResponse",
    "RecommendationsResponse",
    "LikeInfoResponse",
    "LikesListResponse",
    "LikeActionResponse",
    "MatchResponse",
]
