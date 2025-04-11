from fastapi import FastAPI
import json
from routes.api_router import router

app = FastAPI()

app.include_router(router)


    
@app.get("/video_story")
def get_video_story():
    file_path = "data_link.json"
    with open(file_path, "r") as f:
        data = json.load(f)
    return data