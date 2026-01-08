import React, { useRef, useState, useCallback } from 'react';
import Webcam from 'react-webcam';
import { Camera, RefreshCw, AlertTriangle, CheckCircle, XCircle } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || '';

const FireDetector = ({ onBack }) => {
  const webcamRef = useRef(null);
  const [image, setImage] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [facingMode, setFacingMode] = useState('environment');

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    setImage(imageSrc);
    analyzeImage(imageSrc);
  }, [webcamRef]);

  const analyzeImage = async (imageSrc) => {
    setAnalyzing(true);
    setError(null);
    setResult(null);

    try {
      // Convert base64 to blob
      const res = await fetch(imageSrc);
      const blob = await res.blob();
      const formData = new FormData();
      formData.append('image', blob, 'capture.jpg');

      const response = await fetch(`${API_URL}/api/detect-fire`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Detection failed');
      }

      const data = await response.json();
      setResult(data.detections);
    } catch (err) {
      console.error(err);
      setError('Failed to analyze image. Please try again.');
    } finally {
      setAnalyzing(false);
    }
  };

  const reset = () => {
    setImage(null);
    setResult(null);
    setError(null);
  };

  const switchCamera = () => {
    setFacingMode((prev) => (prev === 'user' ? 'environment' : 'user'));
  };

  return (
    <div className="flex flex-col h-full bg-black text-white rounded-xl overflow-hidden relative">
        {onBack && (
            <button
                onClick={onBack}
                className="absolute top-4 left-4 z-20 bg-gray-800/50 p-2 rounded-full text-white"
            >
                &larr; Back
            </button>
        )}
      {!image ? (
        <div className="relative h-full flex flex-col">
          <Webcam
            audio={false}
            ref={webcamRef}
            screenshotFormat="image/jpeg"
            videoConstraints={{ facingMode }}
            className="h-full w-full object-cover"
          />
          <div className="absolute bottom-8 left-0 right-0 flex justify-center items-center gap-8">
            <button
                onClick={switchCamera}
                className="p-3 bg-gray-800/50 rounded-full hover:bg-gray-700/50 transition"
            >
                <RefreshCw size={24} />
            </button>
            <button
              onClick={capture}
              className="p-4 bg-red-600 rounded-full hover:bg-red-700 transition shadow-lg border-4 border-white/20"
            >
              <Camera size={32} />
            </button>
            <div className="w-12"></div> {/* Spacer for alignment */}
          </div>
        </div>
      ) : (
        <div className="h-full flex flex-col p-4 overflow-y-auto">
          <img src={image} alt="Captured" className="rounded-lg mb-4 w-full h-64 object-cover" />

          <div className="flex-1">
            {analyzing && (
              <div className="flex flex-col items-center justify-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-red-500 mb-2"></div>
                <p className="text-gray-300">Analyzing for fire or smoke...</p>
              </div>
            )}

            {error && (
              <div className="bg-red-900/50 text-red-200 p-4 rounded-lg flex items-center gap-2 mb-4">
                <AlertTriangle size={20} />
                <span>{error}</span>
              </div>
            )}

            {result && (
              <div className="space-y-4">
                <h3 className="text-xl font-bold border-b border-gray-700 pb-2">Analysis Results</h3>
                {result.length > 0 ? (
                  result.map((det, index) => (
                    <div key={index} className="bg-gray-800 p-4 rounded-lg flex justify-between items-center border border-red-500/30">
                      <div>
                        <p className="font-bold text-lg capitalize text-red-400">{det.label}</p>
                        <p className="text-sm text-gray-400">Confidence: {(det.confidence * 100).toFixed(1)}%</p>
                      </div>
                      <AlertTriangle className="text-red-500" size={24} />
                    </div>
                  ))
                ) : (
                  <div className="bg-gray-800 p-4 rounded-lg flex items-center gap-3">
                    <CheckCircle className="text-green-500" size={24} />
                    <p>No fire or smoke detected.</p>
                  </div>
                )}

                {result.length > 0 && (
                    <div className="mt-4 p-4 bg-red-900/30 border border-red-500/50 rounded-lg">
                        <h4 className="font-bold text-red-200 mb-2">Emergency Action:</h4>
                        <ul className="list-disc list-inside text-sm text-gray-300 space-y-1">
                            <li>Call 101 immediately if confirmed fire.</li>
                            <li>Evacuate the area safely.</li>
                            <li>Do not attempt to extinguish large fires yourself.</li>
                        </ul>
                    </div>
                )}
              </div>
            )}
          </div>

          <button
            onClick={reset}
            className="mt-4 w-full py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-semibold transition"
          >
            Scan Again
          </button>
        </div>
      )}
    </div>
  );
};

export default FireDetector;
