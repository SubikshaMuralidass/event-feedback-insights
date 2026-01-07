from fastapi import FastAPI
from .routes import router
from .database import engine, Base
import app.models 

app = FastAPI(title="Event Feedback Insights API")
Base.metadata.create_all(bind=engine) #auto create tables
app.include_router(router)
