import React from 'react';
import GenericDetector from './components/GenericDetector';

const WaterLeakDetector = ({ onBack }) => {
    return (
        <GenericDetector
            apiEndpoint="detect-water-leak"
            title="Water Leak Detector"
            description="Identify water leaks, burst pipes, and puddles in public areas."
            onBack={onBack}
            color="cyan"
            drawColor="cyan"
            buttonColor="cyan"
        />
    );
};

export default WaterLeakDetector;
