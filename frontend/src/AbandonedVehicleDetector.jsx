import React from 'react';
import GenericDetector from './components/GenericDetector';

const AbandonedVehicleDetector = ({ onBack }) => {
    return (
        <GenericDetector
            apiEndpoint="detect-abandoned-vehicle"
            title="Abandoned Vehicle Detector"
            description="Identify abandoned, wrecked, or rusted vehicles on public property."
            onBack={onBack}
            color="gray"
            drawColor="gray"
            buttonColor="gray"
        />
    );
};

export default AbandonedVehicleDetector;
