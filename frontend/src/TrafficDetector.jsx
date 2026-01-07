import React, { useRef, useState, useEffect, useCallback } from 'react';
import Webcam from 'react-webcam';

const API_URL = import.meta.env.VITE_API_URL || '';

const TrafficDetector = ({ onBack }) => {
    const webcamRef = useRef(null);
    const canvasRef = useRef(null);
    const [isDetecting, setIsDetecting] = useState(false);
    const [detections, setDetections] = useState([]);
    const [error, setError] = useState(null);

    const videoConstraints = {
        width: 640,
        height: 480,
        facingMode: "environment"
    };

    const detectFrame = useCallback(async () => {
        if (!webcamRef.current || !canvasRef.current || !isDetecting) return;

        const video = webcamRef.current.video;
        if (video.readyState !== 4) return;

        const canvas = canvasRef.current;
        const context = canvas.getContext('2d');

        // Match canvas size to video
        if (canvas.width !== video.videoWidth || canvas.height !== video.videoHeight) {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
        }

        // Get image from webcam
        const imageSrc = webcamRef.current.getScreenshot();
        if (!imageSrc) return;

        try {
            // Convert base64 to blob
            const res = await fetch(imageSrc);
            const blob = await res.blob();
            const formData = new FormData();
            formData.append('image', blob, 'frame.jpg');

            const response = await fetch(`${API_URL}/api/detect-traffic`, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                drawDetections(data.detections, context);
                setDetections(data.detections);
            }
        } catch (err) {
            console.error("Detection error:", err);
            // Don't set global error to avoid blocking UI on transient network fail
        }
    }, [isDetecting]);

    useEffect(() => {
        let interval;
        if (isDetecting) {
            interval = setInterval(detectFrame, 3000); // Check every 3 seconds for CLIP models (slower than YOLO)
        } else {
            if (interval) clearInterval(interval);
            if (canvasRef.current) {
                const ctx = canvasRef.current.getContext('2d');
                ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
            }
            setDetections([]);
        }
        return () => {
            if (interval) clearInterval(interval);
        };
    }, [isDetecting, detectFrame]);

    const drawDetections = (detections, context) => {
        context.clearRect(0, 0, context.canvas.width, context.canvas.height);

        // CLIP detections via API don't typically return bounding boxes, just labels and confidence.
        // So we will just display the detected labels on the screen.

        context.font = 'bold 24px Arial';
        let y = 40;

        if (detections.length === 0) {
            // clear
            return;
        }

        detections.forEach(det => {
            const label = `${det.label} ${(det.confidence * 100).toFixed(0)}%`;

            // Draw background
            const textWidth = context.measureText(label).width;
            context.fillStyle = 'rgba(0,0,0,0.6)';
            context.fillRect(10, y - 30, textWidth + 20, 40);

            // Draw text
            context.fillStyle = '#00FF00'; // Green text
            if (det.label.includes('jam') || det.label.includes('heavy') || det.label.includes('accident')) {
                context.fillStyle = '#FF4444'; // Red for bad traffic
            }
            context.fillText(label, 20, y);
            y += 50;
        });
    };

    return (
        <div className="flex flex-col items-center w-full max-w-md mx-auto p-4">
            <h2 className="text-xl font-bold mb-4 text-gray-800">Traffic Congestion Detector</h2>

            {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4 w-full">
                    {error}
                </div>
            )}

            <div className="relative w-full rounded-lg overflow-hidden shadow-xl bg-black aspect-[4/3] mb-6">
                <Webcam
                    ref={webcamRef}
                    audio={false}
                    screenshotFormat="image/jpeg"
                    videoConstraints={videoConstraints}
                    className="absolute top-0 left-0 w-full h-full object-cover"
                    onUserMediaError={(e) => setError("Camera access denied: " + e)}
                />
                <canvas
                    ref={canvasRef}
                    className="absolute top-0 left-0 w-full h-full pointer-events-none"
                />
                {!isDetecting && (
                    <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-40">
                        <p className="text-white font-medium bg-black bg-opacity-50 px-4 py-2 rounded backdrop-blur-sm">
                            Ready to Scan
                        </p>
                    </div>
                )}
            </div>

            <div className="w-full space-y-3">
                <button
                    onClick={() => setIsDetecting(!isDetecting)}
                    className={`w-full py-3 px-4 rounded-xl text-white font-semibold shadow-lg transition-all active:scale-95 flex items-center justify-center gap-2
                        ${isDetecting
                            ? 'bg-red-500 hover:bg-red-600 shadow-red-500/30'
                            : 'bg-blue-600 hover:bg-blue-700 shadow-blue-600/30'
                        }`}
                >
                    {isDetecting ? (
                        <>
                            <span className="w-2 h-2 bg-white rounded-full animate-pulse"/>
                            Stop Detection
                        </>
                    ) : (
                        <>
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                            Start Live Detection
                        </>
                    )}
                </button>

                <p className="text-xs text-gray-500 text-center">
                    AI analyzes traffic density in real-time.
                </p>

                <button
                    onClick={onBack}
                    className="w-full py-2 text-gray-600 hover:text-gray-900 font-medium transition-colors"
                >
                    ← Back to Home
                </button>
            </div>

            {detections.length > 0 && (
                <div className="mt-4 w-full p-4 bg-white rounded-lg shadow border border-gray-100">
                    <h3 className="text-sm font-semibold text-gray-700 mb-2">Detailed Analysis:</h3>
                    <ul className="space-y-1">
                        {detections.map((det, idx) => (
                            <li key={idx} className="flex justify-between text-sm">
                                <span className="capitalize text-gray-800">{det.label}</span>
                                <span className="font-mono text-gray-500">{(det.confidence * 100).toFixed(1)}%</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default TrafficDetector;
