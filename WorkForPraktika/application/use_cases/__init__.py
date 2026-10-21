from application.use_cases.auth_case import (
    RegisterUseCase,
    LoginUseCase,
    EmailAlreadyExistsError,
    InvalidCredentialsError,
)

from application.use_cases.user_case import (
    GetAllUsersUseCase,
    GetUserByIdUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase,
    UserNotFoundError,
)

from application.use_cases.ahp_case import (
    CalculateWeightsUseCase,
    SaveWeightsUseCase,
    GetWeightsUseCase,
)

from application.use_cases.compability_case import (
    CalculateCompatibilityUseCase,
    GetRecommendationsUseCase,
    NoCandidatesError,
)

from application.use_cases.likes_case import (
    LikeUserUseCase,
    GetReceivedLikesUseCase,
    GetGivenLikesUseCase,
    GetMatchesUseCase,
    SelfLikeError,
)

__all__ = [
    # Auth
    "RegisterUseCase",
    "LoginUseCase",
    "EmailAlreadyExistsError",
    "InvalidCredentialsError",
    # Users
    "GetAllUsersUseCase",
    "GetUserByIdUseCase",
    "UpdateUserUseCase",
    "DeleteUserUseCase",
    "UserNotFoundError",
    # AHP
    "CalculateWeightsUseCase",
    "SaveWeightsUseCase",
    "GetWeightsUseCase",
    # Compatibility
    "CalculateCompatibilityUseCase",
    "GetRecommendationsUseCase",
    "NoCandidatesError",
    # Likes
    "LikeUserUseCase",
    "GetReceivedLikesUseCase",
    "GetGivenLikesUseCase",
    "GetMatchesUseCase",
    "SelfLikeError",
]
