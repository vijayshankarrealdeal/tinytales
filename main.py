from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from routes.api_router import router

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "https://tinytales-1847a.web.app","https://tinytales-1847a.firebaseapp.com/"],  # Your Flutter web domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)


@app.get("/video_story")
def get_video_story():
    file_path = "data_link.json"
    with open(file_path, "r") as f:
        data = json.load(f)
    return data
