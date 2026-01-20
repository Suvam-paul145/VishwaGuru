import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Mic, Square, Activity, Volume2, AlertTriangle } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || '';

const NoiseDetector = ({ onBack }) => {
    const [isRecording, setIsRecording] = useState(false);
    const [analyzing, setAnalyzing] = useState(false);
    const [detection, setDetection] = useState(null);
    const [error, setError] = useState(null);
    const mediaRecorderRef = useRef(null);
    const chunksRef = useRef([]);
    const navigate = useNavigate();

    const startRecording = async () => {
        setError(null);
        setDetection(null);
        chunksRef.current = [];
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const mediaRecorder = new MediaRecorder(stream);
            mediaRecorderRef.current = mediaRecorder;

            mediaRecorder.ondataavailable = (e) => {
                if (e.data.size > 0) {
                    chunksRef.current.push(e.data);
                }
            };

            mediaRecorder.onstop = async () => {
                const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
                analyzeAudio(blob);
                // Stop all tracks
                stream.getTracks().forEach(track => track.stop());
            };

            mediaRecorder.start();
            setIsRecording(true);
        } catch (err) {
            console.error(err);
            setError("Could not access microphone. Ensure you are using HTTPS and have granted permission.");
        }
    };

    const stopRecording = () => {
        if (mediaRecorderRef.current && isRecording) {
            mediaRecorderRef.current.stop();
            setIsRecording(false);
        }
    };

    const analyzeAudio = async (audioBlob) => {
        setAnalyzing(true);
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.webm');

        try {
            const response = await fetch(`${API_URL}/api/detect-audio`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error("Analysis failed");

            const data = await response.json();
            // Expected format from HF Audio Classification:
            // [{"score": 0.9, "label": "dog_bark"}, ...] OR {"detections": [...]}
            // My backend returns {"detections": ...}

            let results = [];
            if (data.detections && Array.isArray(data.detections)) {
                results = data.detections;
            } else if (Array.isArray(data)) {
                results = data;
            }

            if (results.length > 0) {
                 // Sort by score
                 const sorted = results.sort((a, b) => (b.score || 0) - (a.score || 0));
                 setDetection(sorted[0]);
            } else {
                 setDetection(null);
                 setError("No distinct sound detected.");
            }
        } catch (err) {
            console.error(err);
            setError("Failed to analyze audio. Please try again.");
        } finally {
            setAnalyzing(false);
        }
    };

    const handleReport = () => {
        if (detection) {
             navigate('/report', {
                state: {
                    category: 'noise', // Note: 'noise' category might need to be added to ReportForm dropdown if strict
                    description: `Noise Complaint: Detected ${detection.label} with ${((detection.score || 0) * 100).toFixed(0)}% confidence.`
                }
            });
        }
    };

    return (
        <div className="mt-6 flex flex-col items-center w-full max-w-md mx-auto p-4">
             <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                <Volume2 className="text-blue-600" />
                Noise Pollution Detector
             </h2>

             <div className={`w-48 h-48 rounded-full flex items-center justify-center mb-8 transition-all duration-500 ${isRecording ? 'bg-red-50 ring-4 ring-red-100' : 'bg-blue-50'}`}>
                {analyzing ? (
                     <Activity size={64} className="text-blue-600 animate-pulse" />
                ) : (
                    <button
                        onClick={isRecording ? stopRecording : startRecording}
                        className={`w-32 h-32 rounded-full flex items-center justify-center shadow-lg transition transform active:scale-95 ${isRecording ? 'bg-red-500 hover:bg-red-600' : 'bg-blue-600 hover:bg-blue-700'}`}
                    >
                        {isRecording ? <Square size={40} className="text-white fill-current" /> : <Mic size={40} className="text-white" />}
                    </button>
                )}
             </div>

             <div className="text-center mb-8 h-12">
                 {isRecording && <p className="text-red-500 font-medium animate-pulse">Recording... Tap to stop</p>}
                 {analyzing && <p className="text-blue-600 font-medium">Analyzing audio signature...</p>}
                 {!isRecording && !analyzing && !detection && <p className="text-gray-500">Tap the microphone to record noise</p>}
             </div>

             {error && (
                <div className="w-full bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6 flex items-start gap-2">
                    <AlertTriangle size={20} className="mt-0.5 flex-shrink-0" />
                    <span>{error}</span>
                </div>
             )}

             {detection && (
                 <div className="w-full bg-white rounded-xl shadow-md border border-gray-100 overflow-hidden mb-6 animate-in fade-in slide-in-from-bottom-4">
                     <div className="p-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white">
                         <h3 className="font-bold text-lg">Analysis Result</h3>
                     </div>
                     <div className="p-6 text-center">
                         <p className="text-gray-500 text-sm uppercase tracking-wide mb-1">Detected Sound</p>
                         <p className="text-3xl font-bold text-gray-800 capitalize mb-2">{detection.label.replace(/_/g, ' ')}</p>
                         <div className="w-full bg-gray-100 rounded-full h-2 mb-1">
                             <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${(detection.score || 0) * 100}%` }}></div>
                         </div>
                         <p className="text-xs text-right text-gray-500">{((detection.score || 0) * 100).toFixed(1)}% Confidence</p>
                     </div>
                     <div className="p-4 bg-gray-50 border-t border-gray-100">
                         <button
                             onClick={handleReport}
                             className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition shadow-sm"
                         >
                             Report as Noise Pollution
                         </button>
                     </div>
                 </div>
             )}

             <button onClick={onBack} className="text-gray-500 hover:text-gray-900 underline">
                 Back to Home
             </button>
        </div>
    );
};

export default NoiseDetector;
