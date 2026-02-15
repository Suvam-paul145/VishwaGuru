import React from 'react';
import GenericDetector from './components/GenericDetector';

const ConstructionSafetyDetector = ({ onBack }) => {
    return (
        <GenericDetector
            apiEndpoint="detect-construction-safety"
            title="Construction Safety Monitor"
            description="Identify safety hazards at construction sites like missing barriers or exposed wiring."
            onBack={onBack}
            color="orange"
            drawColor="orange"
            buttonColor="orange"
        />
    );
};

export default ConstructionSafetyDetector;
