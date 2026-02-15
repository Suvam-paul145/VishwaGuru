import React from 'react';
import GenericDetector from './components/GenericDetector';

const WasteDetector = ({ onBack }) => {
    return (
        <GenericDetector
            apiEndpoint="detect-waste"
            title="Waste Management Inspector"
            description="Classify waste types and detect overflowing bins or littering."
            onBack={onBack}
            color="green"
            drawColor="green"
            buttonColor="green"
        />
    );
};

export default WasteDetector;
