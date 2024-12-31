import React, { useState } from 'react';
import DrawingCanvas from './components/DrawingCanvas';
import PredictionDisplay from './components/PredictionDisplay';
import ThemeToggle from './components/ThemeToggle';

const App: React.FC = () => {
  const [mode, setMode] = useState<'train' | 'test'>('test');
  const [prediction, setPrediction] = useState<number | null>(null);
  const [confidence, setConfidence] = useState<number>(0);
  const [requestedDigit, setRequestedDigit] = useState<number | null>(null);

  const handleModeChange = (newMode: 'train' | 'test') => {
    setMode(newMode);
    if (newMode === 'train') {
      setRequestedDigit(Math.floor(Math.random() * 10));
    } else {
      setRequestedDigit(null);
    }
  };

  return (
    <div className="min-h-screen p-4">
      <div className="max-w-4xl mx-auto">
        <header className="relative flex justify-center items-center mb-6">
          <h1 className="text-5xl font-bold text-gray-800 dark:text-white">
            Digit Recognition App
          </h1>
          <div className="absolute right-0">
            <ThemeToggle />
          </div>
        </header>

        <div className="flex justify-center gap-4 mb-8">
          <button
            onClick={() => handleModeChange('train')}
            className={`px-6 py-2 rounded-lg text-lg ${
              mode === 'train'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 dark:bg-gray-700'
            }`}
          >
            Train
          </button>
          <button
            onClick={() => handleModeChange('test')}
            className={`px-6 py-2 rounded-lg text-lg ${
              mode === 'test'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 dark:bg-gray-700'
            }`}
          >
            Test
          </button>
        </div>

        {mode === 'train' && requestedDigit !== null && (
          <div className="text-center mb-8">
            <div className="text-2xl font-medium text-gray-700 dark:text-gray-300">
              Please draw the digit: 
              <span className="ml-2 text-3xl font-bold text-blue-600 dark:text-blue-400">
                {requestedDigit}
              </span>
            </div>
          </div>
        )}

        <div className="flex flex-col items-center">
          <DrawingCanvas
            mode={mode}
            onPrediction={(digit, conf) => {
              if (mode === 'train' && digit === -1) {
                // Special case: generate new random digit after training
                setRequestedDigit(Math.floor(Math.random() * 10));
              } else {
                setPrediction(digit);
                setConfidence(conf);
              }
            }}
            requestedDigit={requestedDigit}
          />

          {mode === 'test' && (
            <PredictionDisplay prediction={prediction} confidence={confidence} />
          )}
        </div>
      </div>
    </div>
  );
};

export default App; 