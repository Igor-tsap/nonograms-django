from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database.core import engine, Base
from puzzles.controller import router as puzzles_router
from users.controller import router as users_router
from attempts.controller import router as attempts_router
from chat.controller import router as chat_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Nonograms API", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_origins=["http://34.118.74.50", "http://34.118.74.50:8000", "http://localhost", "http://localhost:3000", "http://localhost:3001"],  # Next.js dev/prod ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(puzzles_router)
app.include_router(users_router)
app.include_router(attempts_router)
app.include_router(chat_router)


@app.get("/")
async def root():
    return {"message": "Nonograms API is working!"}