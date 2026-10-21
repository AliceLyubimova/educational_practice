

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from presentation.api import (
    auth_router,
    user_router,
    ahp_router,
    compatibility_router,
    like_router,
    photo_router,
    comment_router,
)

# Создание

app = FastAPI(
    title="Сервис подбора супруга",
    description="API для сервиса знакомств с интеллектуальным подбором",
    version="1.0.0",
)

# CORS порты 

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  
        "http://localhost:3000",  
        "http://127.0.0.1:5173",   
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Руты 

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(ahp_router)
app.include_router(compatibility_router)
app.include_router(like_router)
app.include_router(photo_router)
app.include_router(comment_router)

@app.get("/")
def home():
    """Проверка, что сервер запущен."""
    return {
        "message": "Сервис подбора супруга работает!",
        "docs": "/docs",
        "version": "1.0.0",
    }


# Запуск

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
