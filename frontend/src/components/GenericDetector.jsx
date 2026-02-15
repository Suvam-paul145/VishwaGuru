import React, { useRef, useState, useEffect } from 'react';

const API_URL = import.meta.env.VITE_API_URL || '';

const GenericDetector = ({
    apiEndpoint,
    title,
    description,
    onBack,
    color = '#00FF00', // Default green
    drawColor = '#00FF00',
    buttonColor = 'blue' // Tailwind color name (e.g., 'blue', 'red')
}) => {
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const [isDetecting, setIsDetecting] = useState(false);
    const [error, setError] = useState(null);

    // Helper to get hex from tailwind-like names if passed, or just use color prop
    // Simple mapping for common colors used in app
    const getColorHex = (c) => {
        const colors = {
            'green': '#22c55e',
            'red': '#ef4444',
            'blue': '#3b82f6',
            'yellow': '#eab308',
            'orange': '#f97316',
            'purple': '#a855f7',
            'pink': '#ec4899',
            'cyan': '#06b6d4',
            'teal': '#14b8a6',
            'indigo': '#6366f1',
            'gray': '#6b7280'
        };
        return colors[c] || c || '#00FF00';
    };

    const strokeColor = getColorHex(drawColor);

    const startCamera = async () => {
        setError(null);
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    facingMode: 'environment',
                    width: { ideal: 640 },
                    height: { ideal: 480 }
                }
            });
            if (videoRef.current) {
                videoRef.current.srcObject = stream;
            }
        } catch (err) {
            setError("Could not access camera: " + err.message);
            setIsDetecting(false);
        }
    };

    const stopCamera = () => {
        if (videoRef.current && videoRef.current.srcObject) {
            const tracks = videoRef.current.srcObject.getTracks();
            tracks.forEach(track => track.stop());
            videoRef.current.srcObject = null;
        }
    };

    const drawDetections = (detections, context) => {
        context.clearRect(0, 0, context.canvas.width, context.canvas.height);

        // If detections is not an array (e.g. error or empty object), return
        if (!Array.isArray(detections)) return;

        detections.forEach((det, index) => {
            // Check for bounding box
            if (det.box && Array.isArray(det.box) && det.box.length === 4) {
                const [x1, y1, x2, y2] = det.box;

                context.strokeStyle = strokeColor;
                context.lineWidth = 4;
                context.strokeRect(x1, y1, x2 - x1, y2 - y1);

                // Draw label background
                context.font = 'bold 18px Arial';
                const label = `${det.label} ${(det.confidence * 100).toFixed(0)}%`;
                const textWidth = context.measureText(label).width;

                context.fillStyle = 'rgba(0,0,0,0.5)';
                context.fillRect(x1, y1 > 20 ? y1 - 25 : y1, textWidth + 10, 25);

                context.fillStyle = strokeColor;
                context.fillText(label, x1 + 5, y1 > 20 ? y1 - 7 : y1 + 18);
            } else {
                // Zero-shot detection (no box, just label list)
                context.font = 'bold 20px Arial';

                // Use semi-transparent background of the theme color
                // Need to convert hex to rgba for transparency? Or just use a fixed dark bg
                context.fillStyle = 'rgba(0, 0, 0, 0.6)';

                const label = `${det.label} ${(det.confidence * 100).toFixed(0)}%`;
                const textWidth = context.measureText(label).width;

                const yPos = 40 + (index * 50);
                context.fillRect(10, yPos - 30, textWidth + 20, 40);

                context.fillStyle = strokeColor;
                context.fillText(label, 20, yPos - 4);
            }
        });
    };

    const detectFrame = async () => {
        if (!videoRef.current || !canvasRef.current || !isDetecting) return;

        const video = videoRef.current;
        if (video.readyState !== 4) return;

        const canvas = canvasRef.current;
        const context = canvas.getContext('2d');

        if (canvas.width !== video.videoWidth || canvas.height !== video.videoHeight) {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
        }

        // Draw video frame
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Capture frame
        canvas.toBlob(async (blob) => {
            if (!blob) return;

            const formData = new FormData();
            formData.append('image', blob, 'frame.jpg');

            try {
                // Remove /api prefix if provided in endpoint to avoid double slash,
                // but usually endpoint passed as 'detect-pothole' or '/api/detect-pothole'
                // Let's assume endpoint is full path relative to API_URL or just the suffix
                const endpoint = apiEndpoint.startsWith('/') ? apiEndpoint : `/api/${apiEndpoint}`;
                const url = `${API_URL}${endpoint}`;

                const response = await fetch(url, {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    const data = await response.json();
                    // Handle different response structures
                    // Some return { detections: [...] }, some might return list directly (unlikely based on codebase)
                    const detections = data.detections || [];
                    drawDetections(detections, context);
                }
            } catch (err) {
                console.error("Detection error:", err);
            }
        }, 'image/jpeg', 0.8);
    };

    useEffect(() => {
        let interval;
        if (isDetecting) {
            startCamera();
            interval = setInterval(detectFrame, 2000);
        } else {
            stopCamera();
            if (interval) clearInterval(interval);
            if (canvasRef.current) {
                const ctx = canvasRef.current.getContext('2d');
                ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
            }
        }
        return () => {
            stopCamera();
            if (interval) clearInterval(interval);
        };
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [isDetecting]);

    const btnClass = isDetecting
        ? 'bg-red-600 hover:bg-red-700'
        : `bg-${buttonColor}-600 hover:bg-${buttonColor}-700`;

    return (
        <div className="mt-6 flex flex-col items-center w-full">
            <h2 className="text-xl font-semibold mb-4 text-center">{title}</h2>

            {error && <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">{error}</div>}

            <div className="relative w-full max-w-md bg-black rounded-lg overflow-hidden shadow-lg mb-6">
                <div className="relative">
                     <video
                        ref={videoRef}
                        autoPlay
                        playsInline
                        muted
                        className="w-full h-auto block"
                        style={{ opacity: isDetecting ? 1 : 0.5 }}
                    />
                    <canvas
                        ref={canvasRef}
                        className="absolute top-0 left-0 w-full h-full pointer-events-none"
                    />
                    {!isDetecting && (
                        <div className="absolute inset-0 flex items-center justify-center">
                            <p className="text-white font-medium bg-black bg-opacity-50 px-4 py-2 rounded">
                                Camera Paused
                            </p>
                        </div>
                    )}
                </div>
            </div>

            <button
                onClick={() => setIsDetecting(!isDetecting)}
                className={`w-full max-w-md py-3 px-4 rounded-lg text-white font-medium shadow-md transition transform active:scale-95 ${btnClass}`}
            >
                {isDetecting ? 'Stop Detection' : `Start ${title}`}
            </button>

            <p className="text-sm text-gray-500 mt-2 text-center max-w-md">
                {description || "Point your camera at the scene. Detections will be highlighted in real-time."}
            </p>

            <button
                onClick={onBack}
                className="mt-6 text-gray-600 hover:text-gray-900 underline"
            >
                Back to Home
            </button>
        </div>
    );
};

export default GenericDetector;
