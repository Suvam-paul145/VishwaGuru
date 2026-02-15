import React from 'react';
import GenericDetector from './components/GenericDetector';

const TrafficSignDetector = ({ onBack }) => {
    return (
        <GenericDetector
            apiEndpoint="detect-traffic-sign"
            title="Traffic Sign Inspector"
            description="Point camera at traffic signs to detect damage, vandalism, or fading."
            onBack={onBack}
            color="yellow"
            drawColor="yellow"
            buttonColor="yellow"
        />
    );
};

export default TrafficSignDetector;
