from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import numpy as np
import cv2
import sys
import types

# ---- moviepy stub: fer ko sirf Video ke liye chahiye, hum video use hi nahi kar rahe ----
# Render par moviepy/pillow ke issues se bachne ke liye ek dummy module bana rahe hain.
if "moviepy" not in sys.modules:
    moviepy_stub = types.ModuleType("moviepy")
    editor_stub = types.ModuleType("editor")
    moviepy_stub.editor = editor_stub
    sys.modules["moviepy"] = moviepy_stub
    sys.modules["moviepy.editor"] = editor_stub
# ------------------------------------------------------------------ #

from fer import FER
from tmdb import get_movies_by_emotion

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImageData(BaseModel):
    image: str

detector = FER()

@app.post("/detect_emotion/")
async def detect_emotion(data: ImageData):
    try:
        img_data = base64.b64decode(data.image.split(",")[1])
        np_arr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        result = detector.detect_emotions(img)

        if not result:
            return {"emotion": "neutral", "movies": get_movies_by_emotion("neutral")}

        emotions = result[0]["emotions"]
        dominant = max(emotions, key=emotions.get)

        movies = get_movies_by_emotion(dominant)
        return {"emotion": dominant, "movies": movies}

    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Failed to detect emotion")