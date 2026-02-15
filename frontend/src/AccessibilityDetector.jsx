import React from 'react';
import GenericDetector from './components/GenericDetector';

const AccessibilityDetector = ({ onBack }) => {
    return (
        <GenericDetector
            apiEndpoint="detect-accessibility"
            title="Accessibility Inspector"
            description="Detects blocked ramps, broken elevators, and other accessibility barriers."
            onBack={onBack}
            color="blue"
            drawColor="blue"
            buttonColor="blue"
        />
    );
};

export default AccessibilityDetector;
