from flask import Flask
from flask_cors import CORS
from routes.prediction import prediction_bp
from config import Config

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Register blueprints
app.register_blueprint(prediction_bp)

if __name__ == '__main__':
    app.run(debug=True)