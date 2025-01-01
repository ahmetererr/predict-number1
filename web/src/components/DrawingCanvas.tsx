import React, { useRef, useEffect, useState } from 'react';
import axios from 'axios';
import { API_URL } from '../config';

interface DrawingCanvasProps {
  mode: 'train' | 'test';
  onPrediction: (digit: number, confidence: number) => void;
  requestedDigit: number | null;
}

const DrawingCanvas: React.FC<DrawingCanvasProps> = ({
  mode,
  onPrediction,
  requestedDigit,
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [context, setContext] = useState<CanvasRenderingContext2D | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (canvas) {
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.strokeStyle = 'white';
        ctx.lineWidth = 10;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        setContext(ctx);
      }
    }
  }, []);

  const startDrawing = (e: React.MouseEvent<HTMLCanvasElement> | React.TouchEvent<HTMLCanvasElement>) => {
    setIsDrawing(true);
    const { offsetX, offsetY } = getCoordinates(e);
    context?.beginPath();
    context?.moveTo(offsetX, offsetY);
  };

  const draw = (e: React.MouseEvent<HTMLCanvasElement> | React.TouchEvent<HTMLCanvasElement>) => {
    if (!isDrawing) return;
    const { offsetX, offsetY } = getCoordinates(e);
    context?.lineTo(offsetX, offsetY);
    context?.stroke();
  };

  const stopDrawing = () => {
    setIsDrawing(false);
  };

  const getCoordinates = (e: React.MouseEvent<HTMLCanvasElement> | React.TouchEvent<HTMLCanvasElement>) => {
    if ('touches' in e) {
      const rect = canvasRef.current?.getBoundingClientRect();
      return {
        offsetX: e.touches[0].clientX - (rect?.left || 0),
        offsetY: e.touches[0].clientY - (rect?.top || 0),
      };
    }
    return {
      offsetX: e.nativeEvent.offsetX,
      offsetY: e.nativeEvent.offsetY,
    };
  };

  const clearCanvas = () => {
    if (context && canvasRef.current) {
      context.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
    }
  };

  const handleSubmit = async () => {
    if (!canvasRef.current) return;

    try {
      const imageData = canvasRef.current.toDataURL('image/png');
      console.log('Image data generated:', imageData.substring(0, 50) + '...');
      
      const blob = await (await fetch(imageData)).blob();
      console.log('Blob created:', blob.size, 'bytes');
      
      const formData = new FormData();
      formData.append('image', blob, 'digit.png');
      
      if (mode === 'train' && requestedDigit !== null) {
        formData.append('digit', requestedDigit.toString());
        console.log('Training mode with digit:', requestedDigit);
      }

      const endpoint = mode === 'test' ? '/predict' : '/train';
      const url = `${API_URL}${endpoint}`;
      console.log('Sending request to:', url);

      const response = await axios({
        method: 'post',
        url: url,
        data: formData,
        headers: {
          'Content-Type': 'multipart/form-data',
          'Accept': 'application/json'
        },
        withCredentials: false,
        timeout: 10000
      });

      console.log('Response received:', response.data);

      if (mode === 'test') {
        onPrediction(response.data.predicted_digit, response.data.confidence);
      } else {
        console.log('Training completed successfully');
        clearCanvas();
        onPrediction(-1, -1);
      }
    } catch (error) {
      console.error('Error in handleSubmit:', error);
      if (axios.isAxiosError(error)) {
        console.error('Axios error details:', {
          message: error.message,
          response: error.response?.data,
          status: error.response?.status,
          headers: error.response?.headers,
          config: error.config
        });
      } else {
        console.error('Non-Axios error:', error);
      }
    }
  };

  return (
    <div className="flex flex-col items-center gap-4">
      <canvas
        ref={canvasRef}
        width={280}
        height={280}
        className="border-2 border-gray-300 dark:border-gray-600 bg-black rounded-lg touch-none"
        onMouseDown={startDrawing}
        onMouseMove={draw}
        onMouseUp={stopDrawing}
        onMouseLeave={stopDrawing}
        onTouchStart={startDrawing}
        onTouchMove={draw}
        onTouchEnd={stopDrawing}
      />
      <div className="flex gap-4">
        <button
          onClick={clearCanvas}
          className="px-4 py-2 bg-gray-200 dark:bg-gray-700 rounded"
        >
          Clear
        </button>
        <button
          onClick={handleSubmit}
          className="px-4 py-2 bg-blue-600 text-white rounded"
        >
          {mode === 'train' ? 'Submit Training' : 'Test Prediction'}
        </button>
      </div>
    </div>
  );
};

export default DrawingCanvas; 