import React, { useState, useEffect, useRef } from 'react';

const NoiseDetector = ({ onBack }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [decibels, setDecibels] = useState(0);
  const [maxDecibels, setMaxDecibels] = useState(0);
  const [error, setError] = useState(null);

  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);
  const dataArrayRef = useRef(null);
  const sourceRef = useRef(null);
  const rafIdRef = useRef(null);
  const streamRef = useRef(null);

  useEffect(() => {
    return () => {
      stopRecording();
    };
  }, []);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
      streamRef.current = stream;

      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
      analyserRef.current = audioContextRef.current.createAnalyser();
      sourceRef.current = audioContextRef.current.createMediaStreamSource(stream);

      sourceRef.current.connect(analyserRef.current);

      analyserRef.current.fftSize = 256;
      const bufferLength = analyserRef.current.frequencyBinCount;
      dataArrayRef.current = new Uint8Array(bufferLength);

      setIsRecording(true);
      setError(null);
      setMaxDecibels(0);

      updateDecibels();
    } catch (err) {
      console.error("Error accessing microphone:", err);
      setError("Could not access microphone. Please ensure permissions are granted.");
    }
  };

  const stopRecording = () => {
    if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
    }
    if (audioContextRef.current) {
        audioContextRef.current.close();
    }
    if (rafIdRef.current) {
        cancelAnimationFrame(rafIdRef.current);
    }
    setIsRecording(false);
  };

  const updateDecibels = () => {
    if (!analyserRef.current) return;

    analyserRef.current.getByteFrequencyData(dataArrayRef.current);

    // Calculate average volume
    let sum = 0;
    for (let i = 0; i < dataArrayRef.current.length; i++) {
        sum += dataArrayRef.current[i];
    }
    const average = sum / dataArrayRef.current.length;

    // Map approximate 0-255 range to 0-100 dB (Rough approximation for UI)
    // Real dB calculation requires calibration.
    const approximateDb = Math.round((average / 255) * 100);

    setDecibels(approximateDb);
    setMaxDecibels(prev => Math.max(prev, approximateDb));

    rafIdRef.current = requestAnimationFrame(updateDecibels);
  };

  const getStatusColor = (db) => {
      if (db < 50) return 'text-green-600';
      if (db < 70) return 'text-yellow-600';
      return 'text-red-600';
  };

   const getStatusText = (db) => {
      if (db < 50) return 'Normal';
      if (db < 70) return 'Loud';
      return 'Hazardous';
  };

  return (
    <div className="flex flex-col h-full p-4">
        <div className="flex justify-between items-center mb-6">
            <button onClick={onBack} className="text-blue-600 font-medium">
                &larr; Back
            </button>
            <h2 className="text-xl font-bold text-gray-800">Noise Level Detector</h2>
            <div className="w-8"></div>
        </div>

        <div className="flex-1 flex flex-col items-center justify-center space-y-8">
            <div className="relative w-64 h-64 flex items-center justify-center">
                {/* Outer Circle */}
                <div className={`absolute inset-0 rounded-full border-4 opacity-20 ${getStatusColor(decibels).replace('text', 'border')}`}></div>

                {/* Pulse Animation */}
                {isRecording && (
                    <div
                        className={`absolute inset-0 rounded-full opacity-20 animate-ping ${getStatusColor(decibels).replace('text', 'bg')}`}
                        style={{ animationDuration: `${1000 - decibels * 5}ms`}}
                    ></div>
                )}

                {/* Main Value */}
                <div className="text-center">
                    <div className={`text-6xl font-bold ${getStatusColor(decibels)}`}>
                        {decibels}
                    </div>
                    <div className="text-gray-500 text-lg">dB</div>
                </div>
            </div>

            <div className="text-center space-y-2">
                 <p className={`text-xl font-semibold ${getStatusColor(decibels)}`}>
                    {getStatusText(decibels)}
                </p>
                <p className="text-gray-500 text-sm">
                    Max Recorded: <span className="font-semibold text-gray-700">{maxDecibels} dB</span>
                </p>
            </div>

            {error && (
                <div className="text-red-500 text-sm bg-red-50 p-2 rounded">
                    {error}
                </div>
            )}
        </div>

        <div className="mt-auto pt-6">
            {!isRecording ? (
                <button
                    onClick={startRecording}
                    className="w-full bg-blue-600 text-white py-3 rounded-xl font-bold hover:bg-blue-700 transition"
                >
                    Start Measuring
                </button>
            ) : (
                <button
                    onClick={stopRecording}
                    className="w-full bg-red-600 text-white py-3 rounded-xl font-bold hover:bg-red-700 transition"
                >
                    Stop
                </button>
            )}
            <p className="text-xs text-gray-400 text-center mt-3">
                *Values are approximate and rely on device microphone sensitivity.
            </p>
        </div>
    </div>
  );
};

export default NoiseDetector;
