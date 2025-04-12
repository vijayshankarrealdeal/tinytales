from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from routes.api_router import router

app = FastAPI()

# Allow origins (adjust for production)
origins = [
    "https://tinytales-1847a.web.app/",  # <-- for development; in production, use your frontend URL
    # "https://your-flutter-app.web.app",
    # "https://tinytales.web.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allowed origins
    allow_credentials=True,
    allow_methods=["*"],    # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],    # Authorization, Content-Type, etc.
)


app.include_router(router)


    
@app.get("/video_story")
def get_video_story():
    file_path = "data_link.json"
    with open(file_path, "r") as f:
        data = json.load(f)
    return data