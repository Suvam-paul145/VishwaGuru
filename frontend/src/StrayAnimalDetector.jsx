import React, { useRef, useState, useCallback } from 'react';
import Webcam from 'react-webcam';

const StrayAnimalDetector = ({ onBack }) => {
  const webcamRef = useRef(null);
  const [imgSrc, setImgSrc] = useState(null);
  const [detections, setDetections] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    setImgSrc(imageSrc);
  }, [webcamRef]);

  const retake = () => {
    setImgSrc(null);
    setDetections([]);
    setError(null);
  };

  const detectStrayAnimal = async () => {
    if (!imgSrc) return;

    setLoading(true);
    setError(null);

    try {
      const blob = await (await fetch(imgSrc)).blob();
      const formData = new FormData();
      formData.append('image', blob, 'capture.jpg');

      const response = await fetch(`${import.meta.env.VITE_API_URL || ''}/api/detect-stray-animal`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Detection failed');
      }

      const data = await response.json();
      setDetections(data.detections || []);
    } catch (err) {
      console.error(err);
      setError('Failed to process image. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex justify-between items-center mb-4">
          <button onClick={onBack} className="text-blue-600 font-medium">
            &larr; Back
          </button>
          <h2 className="text-xl font-bold text-gray-800">Stray Animal Detector</h2>
          <div className="w-8"></div> {/* Spacer */}
      </div>

      <div className="flex-1 flex flex-col items-center justify-center bg-black rounded-lg overflow-hidden relative min-h-[300px]">
        {imgSrc ? (
          <img src={imgSrc} alt="Captured" className="w-full h-full object-contain" />
        ) : (
          <Webcam
            audio={false}
            ref={webcamRef}
            screenshotFormat="image/jpeg"
            className="w-full h-full object-contain"
            videoConstraints={{ facingMode: "environment" }}
          />
        )}

        {loading && (
          <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center z-10">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
          </div>
        )}
      </div>

      <div className="mt-4 space-y-3">
        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded-lg text-sm text-center">
            {error}
          </div>
        )}

        {detections.length > 0 && (
          <div className="bg-green-50 border border-green-200 p-4 rounded-lg">
            <h3 className="font-bold text-green-800 mb-2">Detections:</h3>
            <ul className="list-disc pl-5 space-y-1">
              {detections.map((det, index) => (
                <li key={index} className="text-green-700">
                  {det.label} ({Math.round(det.confidence * 100)}%)
                </li>
              ))}
            </ul>
          </div>
        )}

        {detections.length === 0 && imgSrc && !loading && !error && (
             <div className="bg-gray-50 border border-gray-200 p-4 rounded-lg text-center text-gray-600">
                No stray animals detected.
            </div>
        )}

        <div className="flex gap-4">
          {!imgSrc ? (
            <button
              onClick={capture}
              className="flex-1 bg-blue-600 text-white py-3 rounded-xl font-bold hover:bg-blue-700 transition"
            >
              Capture Photo
            </button>
          ) : (
            <>
              <button
                onClick={retake}
                className="flex-1 bg-gray-500 text-white py-3 rounded-xl font-bold hover:bg-gray-600 transition"
              >
                Retake
              </button>
              <button
                onClick={detectStrayAnimal}
                className="flex-1 bg-green-600 text-white py-3 rounded-xl font-bold hover:bg-green-700 transition"
              >
                Analyze
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default StrayAnimalDetector;
