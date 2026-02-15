import React from 'react';
import GenericDetector from './components/GenericDetector';

const CrowdDetector = ({ onBack }) => {
    return (
        <GenericDetector
            apiEndpoint="detect-crowd"
            title="Crowd Density Monitor"
            description="Monitor crowd density and detect potential safety hazards."
            onBack={onBack}
            color="purple"
            drawColor="purple"
            buttonColor="purple"
        />
    );
};

export default CrowdDetector;
