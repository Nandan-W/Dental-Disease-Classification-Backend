from flask import Blueprint, request, jsonify
from services.prediction_service import PredictionService
from utils.file_handler import allowed_file, save_upload
import os

prediction_bp = Blueprint('prediction', __name__)
prediction_service = PredictionService()

@prediction_bp.route('/api/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    try:
        # Save and process the image
        print("image received file= ",file)
        image_path = save_upload(file)
        results = prediction_service.predict(image_path)
        
        # Clean up uploaded file
        os.remove(image_path)
        
        return jsonify({'results': results})

    except Exception as e:
        return jsonify({'error': str(e)}), 500