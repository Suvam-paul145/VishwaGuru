import React from 'react';
import GenericDetector from './components/GenericDetector';

const PublicFacilitiesDetector = ({ onBack }) => {
    return (
        <GenericDetector
            apiEndpoint="detect-public-facilities"
            title="Public Facilities Inspector"
            description="Detect damage to benches, playgrounds, bus stops, and other public assets."
            onBack={onBack}
            color="blue"
            drawColor="blue"
            buttonColor="blue"
        />
    );
};

export default PublicFacilitiesDetector;
