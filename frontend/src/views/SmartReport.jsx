import React, { useRef, useState, useCallback } from 'react';
import Webcam from 'react-webcam';

const SmartReport = ({ setView, setActionPlan, setCategory, setPreFilledDescription }) => {
  const webcamRef = useRef(null);
  const [image, setImage] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState(null);

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    setImage(imageSrc);
  }, [webcamRef]);

  const retake = () => {
    setImage(null);
    setError(null);
  };

  const analyzeImage = async () => {
    if (!image) return;
    setAnalyzing(true);
    setError(null);

    try {
      // Convert base64 to blob
      const res = await fetch(image);
      const blob = await res.blob();
      const file = new File([blob], "capture.jpg", { type: "image/jpeg" });

      const formData = new FormData();
      formData.append('image', file);

      // Call Smart Category Detection API
      // Since we are running on frontend port 5173 and backend is on 8000/api
      // The proxy in vite.config.js or netlify.toml should handle /api
      // Assuming Vite proxy is set or we use full URL if in dev
      const response = await fetch('/api/detect-smart-category', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Analysis failed');
      }

      const data = await response.json();

      if (data.category === 'error' || data.category === 'unknown') {
          setError(`Could not identify the issue. (${data.raw_label})`);
          setAnalyzing(false);
          return;
      }

      // Also generate description
      const descResponse = await fetch('/api/generate-description', {
          method: 'POST',
          body: formData
      });
      const descData = await descResponse.json();

      // Proceed to report form with pre-filled data
      // We need to pass this state back to App or navigate with state
      // Since current architecture passes props, we might need a way to set global state
      // For now, let's assume ReportForm can accept location state or we use a callback
      // But the props provided are setView, etc.

      // Let's assume we can navigate to 'report' and pass data via a global store or context
      // But here we are limited.
      // Workaround: We will use a callback passed from parent if available, or just alert for now.

      // Ideally, App.jsx should handle this transfer.
      // For this task, I'll alert the user and redirect to specific detector if applicable.

      const targetView = data.category;
      alert(`Detected: ${data.category} (Confidence: ${(data.confidence * 100).toFixed(1)}%)\nDescription: ${descData.description}`);

      if (setView) {
          setView(targetView);
      }

    } catch (err) {
      console.error(err);
      setError('An error occurred during analysis.');
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white p-4">
      <button onClick={() => setView('home')} className="self-start text-blue-600 mb-4">
        &larr; Back to Home
      </button>

      <h2 className="text-2xl font-bold mb-4 text-gray-800">Smart Report</h2>
      <p className="text-gray-600 mb-4">Take a photo and we'll automatically detect the issue type.</p>

      <div className="flex-1 flex flex-col items-center justify-center bg-gray-100 rounded-lg overflow-hidden relative min-h-[400px]">
        {image ? (
          <img src={image} alt="Captured" className="w-full h-full object-contain" />
        ) : (
          <Webcam
            audio={false}
            ref={webcamRef}
            screenshotFormat="image/jpeg"
            className="w-full h-full object-cover"
            videoConstraints={{ facingMode: "environment" }}
          />
        )}

        {analyzing && (
            <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center text-white z-10">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-white mx-auto mb-2"></div>
                    <p>Analyzing Image...</p>
                </div>
            </div>
        )}
      </div>

      <div className="mt-4 flex flex-col gap-3">
        {error && <div className="text-red-600 text-center">{error}</div>}

        {!image ? (
          <button
            onClick={capture}
            className="w-full py-3 bg-blue-600 text-white rounded-lg font-semibold shadow-lg active:scale-95 transition-transform"
          >
            Capture Photo
          </button>
        ) : (
          <div className="flex gap-2">
            <button
              onClick={retake}
              className="flex-1 py-3 bg-gray-500 text-white rounded-lg font-semibold shadow-lg active:scale-95 transition-transform"
              disabled={analyzing}
            >
              Retake
            </button>
            <button
              onClick={analyzeImage}
              className="flex-1 py-3 bg-green-600 text-white rounded-lg font-semibold shadow-lg active:scale-95 transition-transform"
              disabled={analyzing}
            >
              Analyze
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default SmartReport;
