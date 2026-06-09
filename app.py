import os
import pickle
import pandas as pd
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash

from models import db, User
from preprocessing import preprocess_input

app = Flask(__name__)
app.config['SECRET_KEY'] = 'skyfare_super_secret_key'
# Use /tmp for SQLite on Vercel as its filesystem is read-only
if os.environ.get('VERCEL') or os.environ.get('VERCEL_ENV'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/skyfare.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skyfare.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth'

# Load the ML model
MODEL_PATH = 'flight_fare_model.pkl'
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully.")
except Exception as e:
    print("Error loading model:", e)
    model = None

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

# ==========================================
# Frontend Routes
# ==========================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/predict', methods=['GET'])
def predict_page():
    return render_template('predict.html')

@app.route('/performance')
def performance():
    return render_template('performance.html')

@app.route('/insights')
def insights():
    return render_template('insights.html')

@app.route('/auth', methods=['GET'])
def auth():
    if current_user.is_authenticated:
        return redirect(url_for('predict_page'))
    return render_template('auth.html')

# ==========================================
# API Routes
# ==========================================

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    user = User(username=data.get('username'), email=data.get('email'))
    user.set_password(data.get('password'))
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Registration successful'}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data.get('email')).first()
    if user and user.check_password(data.get('password')):
        login_user(user)
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/auth/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.json
    try:
        # Preprocess
        input_vector = preprocess_input(data)
        
        # Predict
        if model is None:
            return jsonify({'error': 'Model not loaded on server'}), 500
            
        prediction = model.predict(input_vector)[0]
        
        return jsonify({'fare': float(prediction)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/dashboard/stats', methods=['GET'])
def dashboard_stats():
    # Load dataset to get stats dynamically
    try:
        df = pd.read_excel('Flight_Fare.xlsx')
        stats = {
            'total_records': len(df),
            'total_features': len(df.columns),
            'unique_airlines': df['Airline'].nunique(),
            'missing_values': int(df.isnull().sum().sum()),
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard/data', methods=['GET'])
def dashboard_data():
    try:
        df = pd.read_excel('Flight_Fare.xlsx')
        # Group by Airline for avg price
        airline_prices = df.groupby('Airline')['Price'].mean().to_dict()
        source_dist = df['Source'].value_counts().to_dict()
        dest_dist = df['Destination'].value_counts().to_dict()
        
        return jsonify({
            'airline_prices': airline_prices,
            'source_distribution': source_dist,
            'destination_distribution': dest_dist
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
