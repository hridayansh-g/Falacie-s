# by Hridayansh, Riya, Ishita, Lokendra
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import numpy as np
import cv2
import sys
import types

# ---- moviepy stub (Render par video features use nahi kar rahe) ----
# fer internally moviepy.editor import karta hai, isliye yaha fake module inject kar rahe hain.
if "moviepy" not in sys.modules:
    moviepy_stub = types.ModuleType("moviepy")
    editor_stub = types.ModuleType("editor")
    moviepy_stub.editor = editor_stub
    sys.modules["moviepy"] = moviepy_stub
    sys.modules["moviepy.editor"] = editor_stub
# ------------------------------------------------------------------ #

from fer import FER
from tmdb import get_movies_by_emotion

app = FastAPI(title="Falacie Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # production me specific domain rakh sakte ho
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImageData(BaseModel):
    image: str  # base64 data URL (data:image/jpeg;base64,...)

# FER detector (TensorFlow model load hoga yaha)
detector = FER()

# Root route (Render health check + manual test)
@app.get("/")
async def root():
    return {"status": "ok", "message": "Falacie backend is running 🚀"}

@app.post("/detect_emotion/")
async def detect_emotion(data: ImageData):
    try:
        # "data:image/jpeg;base64,...." → base64 part split
        if "," in data.image:
            b64_data = data.image.split(",")[1]
        else:
            b64_data = data.image

        img_data = base64.b64decode(b64_data)
        np_arr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Failed to decode image")

        # FER se emotions detect
        result = detector.detect_emotions(img)

        if not result:
            # face detect nahi hua → neutral + generic movies
            return {
                "emotion": "neutral",
                "movies": get_movies_by_emotion("neutral"),
            }

        emotions = result[0]["emotions"]
        dominant = max(emotions, key=emotions.get)

        movies = get_movies_by_emotion(dominant)
        return {"emotion": dominant, "movies": movies}

    except Exception as e:
        print("Error in /detect_emotion/:", e)
        raise HTTPException(status_code=500, detail="Failed to detect emotion")