import numpy as np
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
from app.config import settings

class DigitRecognizer:
    def __init__(self):
        self.model_file = settings.MODEL_PATH + '.joblib'
        try:
            self.model = joblib.load(self.model_file)
        except:
            self.model = self._create_model()
            if not os.path.exists(os.path.dirname(self.model_file)):
                os.makedirs(os.path.dirname(self.model_file))
            joblib.dump(self.model, self.model_file)
    
    def _create_model(self):
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        return model
    
    def _preprocess_image(self, image: Image.Image) -> np.ndarray:
        # Resize image to 28x28
        image = image.resize(settings.INPUT_SHAPE)
        # Convert to numpy array and normalize
        img_array = np.array(image).astype('float32') / 255.0
        # Flatten the image for scikit-learn
        img_array = img_array.reshape(1, -1)
        return img_array
    
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
            # Preprocess the image
            processed_image = self._preprocess_image(image)
            
            # Partial fit with the new data
            if not hasattr(self.model, 'classes_'):
                self.model.fit(processed_image, [digit])
            else:
                # Create a new model with updated data
                X = processed_image
                y = [digit]
                if hasattr(self, '_previous_data'):
                    X = np.vstack([self._previous_data[0], processed_image])
                    y = self._previous_data[1] + [digit]
                self.model.fit(X, y)
                self._previous_data = (X, y)
            
            # Save the updated model
            joblib.dump(self.model, self.model_file)
            return True
        except Exception as e:
            print(f"Training error: {str(e)}")
            return False 