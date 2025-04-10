//by Hridayansh, Riya, Ishita, Lokendra
import React, { useState, useRef } from "react";
import EmotionResult from "./components/EmotionResult";
import Webcam from "react-webcam";

function App() {
  const [imageSrc, setImageSrc] = useState(null);
  const [result, setResult] = useState(null);
  const webcamRef = useRef(null);

  const captureImage = async () => {
    const image = webcamRef.current.getScreenshot();
    setImageSrc(image);
    setResult(null);

    try {
      const response = await fetch("http://localhost:8000/detect_emotion/", {
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
      <h1 className="text-3xl font-bold mb-4">Emotion-Based Movie Recommender 🎬</h1>
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
        {result && <EmotionResult emotion={result.emotion} movies={result.movies} />}
      </div>
    </div>
  );
}

export default App;