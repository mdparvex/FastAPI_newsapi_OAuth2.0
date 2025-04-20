from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body, Depends, FastAPI
from app import database
from app import models
from app.auth import get_current_user, router as auth_router
from app import news_router


models.Base.metadata.create_all(bind=database.engine)

origins = ["*"]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#add router
app.include_router(auth_router)
app.include_router(news_router.router, prefix="/news", dependencies=[Depends(get_current_user)])

@app.get('/')
def root():
    return {"message": "Hello! App is connected perfectly"}
