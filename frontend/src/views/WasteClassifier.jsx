import React, { useRef, useState, useCallback } from 'react';
import Webcam from 'react-webcam';

const WasteClassifier = ({ onBack }) => {
  const webcamRef = useRef(null);
  const [image, setImage] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    setImage(imageSrc);
  }, [webcamRef]);

  const retake = () => {
    setImage(null);
    setResult(null);
    setError(null);
  };

  const analyzeImage = async () => {
    if (!image) return;
    setAnalyzing(true);
    setError(null);

    try {
      const res = await fetch(image);
      const blob = await res.blob();
      const file = new File([blob], "capture.jpg", { type: "image/jpeg" });

      const formData = new FormData();
      formData.append('image', file);

      const response = await fetch('/api/detect-waste-type', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Analysis failed');
      }

      const data = await response.json();
      setResult(data);

    } catch (err) {
      console.error(err);
      setError('An error occurred during analysis.');
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white p-4">
      <button onClick={onBack} className="self-start text-blue-600 mb-4">
        &larr; Back
      </button>

      <h2 className="text-2xl font-bold mb-4 text-green-700">Waste Classifier</h2>
      <p className="text-gray-600 mb-4">Identify waste type for proper disposal (Recycle/Organic/Hazard).</p>

      <div className="flex-1 flex flex-col items-center justify-center bg-gray-100 rounded-lg overflow-hidden relative min-h-[300px]">
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
                    <p>Classifying...</p>
                </div>
            </div>
        )}
      </div>

      {result && (
          <div className="mt-4 p-4 bg-green-50 rounded-lg border border-green-200">
              <h3 className="text-xl font-bold text-green-800 capitalize">{result.waste_type}</h3>
              <p className="text-green-600">Confidence: {(result.confidence * 100).toFixed(1)}%</p>

              <div className="mt-2">
                  <p className="text-sm text-gray-500 font-semibold">Other possibilities:</p>
                  <ul className="text-sm text-gray-600 list-disc list-inside">
                      {result.breakdown && result.breakdown.slice(1).map((item, idx) => (
                          <li key={idx}>{item.label} ({(item.score * 100).toFixed(0)}%)</li>
                      ))}
                  </ul>
              </div>
          </div>
      )}

      <div className="mt-4 flex flex-col gap-3">
        {error && <div className="text-red-600 text-center">{error}</div>}

        {!image ? (
          <button
            onClick={capture}
            className="w-full py-3 bg-green-600 text-white rounded-lg font-semibold shadow-lg active:scale-95 transition-transform"
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
            {!result && (
                <button
                onClick={analyzeImage}
                className="flex-1 py-3 bg-green-600 text-white rounded-lg font-semibold shadow-lg active:scale-95 transition-transform"
                disabled={analyzing}
                >
                Classify
                </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default WasteClassifier;
