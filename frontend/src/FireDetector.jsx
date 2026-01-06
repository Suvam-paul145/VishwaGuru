import React, { useRef, useState, useCallback, Suspense } from 'react';
import Webcam from 'react-webcam';
import { Camera, X, Check, AlertTriangle, AlertOctagon } from 'lucide-react';

const FireDetector = ({ onBack }) => {
  const webcamRef = useRef(null);
  const [imgSrc, setImgSrc] = useState(null);
  const [detections, setDetections] = useState([]);
  const [loading, setLoading] = useState(false);

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    setImgSrc(imageSrc);
  }, [webcamRef]);

  const retake = () => {
    setImgSrc(null);
    setDetections([]);
  };

  const analyzeImage = async () => {
    if (!imgSrc) return;

    setLoading(true);
    try {
      // Convert base64 to blob
      const res = await fetch(imgSrc);
      const blob = await res.blob();
      const file = new File([blob], "capture.jpg", { type: "image/jpeg" });

      const formData = new FormData();
      formData.append('image', file);

      const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/detect-fire`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Detection failed');
      }

      const data = await response.json();
      setDetections(data.detections || []);
    } catch (error) {
      console.error("Error detecting fire:", error);
      alert("Failed to analyze image. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const videoConstraints = {
    facingMode: "environment"
  };

  return (
    <div className="flex flex-col items-center p-4 min-h-screen bg-orange-50">
      <div className="w-full max-w-md bg-white rounded-xl shadow-lg overflow-hidden">
        <div className="bg-orange-600 p-4 text-white flex justify-between items-center">
          <h2 className="text-xl font-bold flex items-center gap-2">
            <AlertOctagon size={24} />
            Fire Detector
          </h2>
          <button onClick={onBack} className="p-1 hover:bg-orange-700 rounded-full">
            <X size={24} />
          </button>
        </div>

        <div className="p-4">
          <div className="relative rounded-lg overflow-hidden bg-gray-900 aspect-video mb-4 shadow-inner">
            {!imgSrc ? (
              <Webcam
                audio={false}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                videoConstraints={videoConstraints}
                className="w-full h-full object-cover"
              />
            ) : (
              <img src={imgSrc} alt="Captured" className="w-full h-full object-cover" />
            )}

            {loading && (
              <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 z-10">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
              </div>
            )}
          </div>

          <div className="flex justify-center gap-4 mb-6">
            {!imgSrc ? (
              <button
                onClick={capture}
                className="flex items-center gap-2 px-6 py-3 bg-orange-600 text-white rounded-full font-semibold shadow-md hover:bg-orange-700 transition-colors"
              >
                <Camera size={20} />
                Capture
              </button>
            ) : (
              <>
                <button
                  onClick={retake}
                  className="flex items-center gap-2 px-6 py-3 bg-gray-500 text-white rounded-full font-semibold shadow-md hover:bg-gray-600 transition-colors"
                >
                  <X size={20} />
                  Retake
                </button>
                <button
                  onClick={analyzeImage}
                  disabled={loading}
                  className="flex items-center gap-2 px-6 py-3 bg-green-600 text-white rounded-full font-semibold shadow-md hover:bg-green-700 transition-colors disabled:opacity-50"
                >
                  <Check size={20} />
                  Analyze
                </button>
              </>
            )}
          </div>

          {detections.length > 0 ? (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <h3 className="font-bold text-red-800 mb-2 flex items-center gap-2">
                <AlertTriangle size={18} />
                Detected Hazards:
              </h3>
              <ul className="space-y-2">
                {detections.map((det, idx) => (
                  <li key={idx} className="flex justify-between items-center bg-white p-2 rounded shadow-sm border border-red-100">
                    <span className="font-medium text-gray-800 capitalize">{det.label}</span>
                    <span className="text-sm bg-red-100 text-red-800 px-2 py-1 rounded-full">
                      {Math.round(det.confidence * 100)}%
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          ) : imgSrc && !loading && (
            <div className="text-center text-gray-500 italic mt-2">
              Tap "Analyze" to check for fire or smoke.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default FireDetector;
