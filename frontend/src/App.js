//by Hridayansh, Riya, Ishita, Lokendra
import React, { useState, useRef } from "react";
import EmotionResult from "./components/EmotionResult";
import Webcam from "react-webcam";

// Backend URL (local dev + easy deploy later)
const BACKEND_URL = "https://falacie-s.onrender.com";

function App() {
  const [imageSrc, setImageSrc] = useState(null);
  const [result, setResult] = useState(null);
  const webcamRef = useRef(null);

  const captureImage = async () => {
    if (!webcamRef.current) return;

    const image = webcamRef.current.getScreenshot();
    if (!image) {
      alert("Unable to capture image, please try again.");
      return;
    }

    setImageSrc(image);
    setResult(null);

    try {
      const response = await fetch(`${BACKEND_URL}/detect_emotion/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image }),
      });

      if (response.ok) {
        const data = await response.json();
        setResult(data);
      } else {
        alert("Failed to detect emotion.");
      }
    } catch (error) {
      alert("Server error: " + error.message);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-4 text-center">
      <h1 className="text-3xl font-bold mb-4">
        Emotion-Based Movie Recommender 🎬
      </h1>

      <div className="flex flex-col items-center">
        <Webcam
          audio={false}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          className="rounded shadow-md"
        />

        <button
          onClick={captureImage}
          className="mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Detect Emotion
        </button>

        {/* Captured image preview */}
        {imageSrc && (
          <img
            src={imageSrc}
            alt="captured"
            className="w-48 mt-3 rounded shadow-lg"
          />
        )}

        {/* Movie recommendations */}
        {result && (
          <EmotionResult emotion={result.emotion} movies={result.movies} />
        )}
      </div>
    </div>
  );
}

export default App;