import React from 'react';

interface PredictionDisplayProps {
  prediction: number | null;
  confidence: number;
}

const PredictionDisplay: React.FC<PredictionDisplayProps> = ({
  prediction,
  confidence,
}) => {
  if (prediction === null) return null;

  return (
    <div className="mt-6 p-4 bg-white dark:bg-gray-800 rounded-lg shadow">
      <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-2">
        Prediction Result
      </h2>
      <div className="text-gray-600 dark:text-gray-300">
        <p className="text-3xl font-bold mb-2">Digit: {prediction}</p>
        <p>Confidence: {(confidence * 100).toFixed(2)}%</p>
      </div>
    </div>
  );
};

export default PredictionDisplay; 