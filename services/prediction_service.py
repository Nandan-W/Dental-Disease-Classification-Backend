import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt

class PredictionService:
    def __init__(self):
        self.model = None
        self.categories = ['Caries', 'Gingivitis', 'Healthy']
        self.model_checkpoint_dir = 'model/'  # Directory where the model is stored
        self.load_model()

    def load_model(self):
        """ Load the model from the specified directory. """
        try:
            model_files = [f for f in os.listdir(self.model_checkpoint_dir) if f.endswith('.h5')]
            
            if model_files:
                latest_model = max(model_files, key=lambda f: os.path.getmtime(os.path.join(self.model_checkpoint_dir, f)))
                
                self.model = tf.keras.models.load_model(os.path.join(self.model_checkpoint_dir, latest_model))
                print(f"Loaded model: {latest_model}")
            else:
                print("No .h5 model found.")
                self.model = None
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None

    def preprocess_image(self, image_path):
        """ Preprocess the image to fit the model input requirements. """
        try:
            img = image.load_img(image_path, target_size=(150, 150))  # Resize image to match input size of model
            img_array = image.img_to_array(img) / 255.0  # Rescale to [0, 1]
            img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
            return img_array
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None

    def predict(self, image_path):
        """ Perform prediction on a given image and return the results. """
        if not self.model:
            return [{"category": "Error1", "percentage": 0}]
        
        img_array = self.preprocess_image(image_path)
        if img_array is None:
            return [{"category": "Error", "percentage": 0}]
        
        try:
            # Make the prediction using the model
            predictions = self.model.predict(img_array)[0]
            
            # Get the predicted class index (highest probability)
            predicted_class = np.argmax(predictions, axis=0)
            
            # Map the predicted class index to its label
            predicted_label = self.categories[predicted_class]
            percentage = predictions[predicted_class] * 100
            
            # Output the result
            print(f"Predicted Class: {predicted_label} ({percentage:.2f}%)")
            
            # Optionally, display the image with the predicted label
            img = image.load_img(image_path, target_size=(150, 150))  # Load image again for display
            plt.imshow(img)
            plt.title(f"Predicted: {predicted_label} ({percentage:.2f}%)")
            plt.show()

            # Return the results as a dictionary
            return [{"category": predicted_label, "percentage": float(percentage)}]
        
        except Exception as e:
            print(f"Error making prediction: {e}")
            return [{"category": "Error", "percentage": 0}]
