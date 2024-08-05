from fastapi import FastAPI
from routers import project
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# CORS 설정
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8001",
    # 추가로 필요한 도메인을 여기에 추가
]

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영 환경에서는 특정 출처만 허용하도록 수정해야 합니다
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 루트 경로 설정


@app.get("/")
async def read_root():
    return {"message": "Welcome to the RAG-Contract application. Use /api for API endpoints."}


# 프로젝트 라우터 등록
app.include_router(project.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
