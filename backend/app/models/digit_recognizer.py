import numpy as np
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
import logging
from app.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DigitRecognizer:
    def __init__(self):
        self.model_file = settings.MODEL_PATH + '.joblib'
        try:
            self.model = joblib.load(self.model_file)
            logger.info("Model loaded successfully from %s", self.model_file)
        except Exception as e:
            logger.warning("Could not load model, creating new one: %s", str(e))
            self.model = self._create_model()
            if not os.path.exists(os.path.dirname(self.model_file)):
                os.makedirs(os.path.dirname(self.model_file))
            joblib.dump(self.model, self.model_file)
    
    def _create_model(self):
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        return model
    
    def _preprocess_image(self, image: Image.Image) -> np.ndarray:
        try:
            # Resize image to 28x28
            image = image.resize(settings.INPUT_SHAPE)
            # Convert to numpy array and normalize
            img_array = np.array(image).astype('float32') / 255.0
            # Flatten the image for scikit-learn
            img_array = img_array.reshape(1, -1)
            return img_array
        except Exception as e:
            logger.error("Error preprocessing image: %s", str(e))
            raise
    
    def predict(self, image: Image.Image) -> tuple[int, float]:
        # Preprocess the image
        processed_image = self._preprocess_image(image)
        
        # Make prediction
        predictions = self.model.predict_proba(processed_image)
        
        # Get the predicted digit and confidence
        predicted_digit = int(self.model.predict(processed_image)[0])
        confidence = float(predictions[0][predicted_digit])
        
        return predicted_digit, confidence
    
    def train(self, image: Image.Image, digit: int) -> bool:
        try:
            logger.info("Starting training with digit: %d", digit)
            
            # Preprocess the image
            logger.info("Preprocessing image...")
            processed_image = self._preprocess_image(image)
            logger.info("Image preprocessed successfully. Shape: %s", processed_image.shape)
            
            # Partial fit with the new data
            if not hasattr(self.model, 'classes_'):
                logger.info("First training instance, initializing model...")
                self.model.fit(processed_image, [digit])
                self._previous_data = (processed_image, [digit])
            else:
                logger.info("Updating existing model...")
                # Create a new model with updated data
                if hasattr(self, '_previous_data'):
                    X = np.vstack([self._previous_data[0], processed_image])
                    y = self._previous_data[1] + [digit]
                else:
                    X = processed_image
                    y = [digit]
                logger.info("Training with data shape: X=%s, y=%s", X.shape, y)
                self.model.fit(X, y)
                self._previous_data = (X, y)
            
            # Save the updated model
            logger.info("Saving model to %s", self.model_file)
            joblib.dump(self.model, self.model_file)
            logger.info("Training completed successfully")
            return True
        except Exception as e:
            logger.error("Training failed: %s", str(e), exc_info=True)
            return False 