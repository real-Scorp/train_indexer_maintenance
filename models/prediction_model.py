# File: models/prediction_model.py

import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import pickle

class WearPredictionModel:
    """Handles the polynomial regression modeling for wear prediction."""
    
    def __init__(self, degree=2):
        self.model = None
        self.poly_features = None
        self.degree = degree
        
    def fit(self, days, wear_values):
        """Train the model on the provided data."""
        if len(days) < 3:
            return False, "Need at least 3 data points for prediction"
            
        # Reshape for sklearn
        X = np.array(days).reshape(-1, 1)
        y = np.array(wear_values)
        
        # Create polynomial features
        self.poly_features = PolynomialFeatures(degree=self.degree)
        X_poly = self.poly_features.fit_transform(X)
        
        # Train the model
        self.model = LinearRegression()
        self.model.fit(X_poly, y)
        
        return True, "Model trained successfully"
        
    def predict(self, days):
        """Predict wear for the given days."""
        if self.model is None or self.poly_features is None:
            return None, "Model not trained"
            
        # Convert to numpy array and reshape
        X = np.array(days).reshape(-1, 1)
        
        # Transform to polynomial features
        X_poly = self.poly_features.transform(X)
        
        # Predict
        predictions = self.model.predict(X_poly)
        
        return predictions, "Prediction completed"
        
    def calculate_threshold_crossing(self, start_day, days_ahead, start_date, threshold):
        """Calculate when wear crosses the maintenance threshold."""
        if self.model is None or self.poly_features is None:
            return None, "Model not trained"
            
        # Generate sequence of days for prediction
        future_days = range(start_day, start_day + days_ahead + 1)
        
        # Predict wear for those days
        predictions, _ = self.predict(future_days)
        
        # Find where prediction crosses threshold
        for i, pred in enumerate(predictions):
            if pred >= threshold:
                # Calculate the date
                crossing_date = start_date + timedelta(days=i)
                days_until = i
                return crossing_date, days_until
                
        return None, "Threshold not reached within prediction window"
        
    def save_model(self, filename):
        """Save trained model to file."""
        if self.model is None:
            return False, "No model to save"
            
        try:
            with open(filename, 'wb') as f:
                pickle.dump((self.model, self.poly_features, self.degree), f)
            return True, "Model saved successfully"
        except Exception as e:
            return False, f"Error saving model: {str(e)}"
            
    def load_model(self, filename):
        """Load trained model from file."""
        try:
            with open(filename, 'rb') as f:
                self.model, self.poly_features, self.degree = pickle.load(f)
            return True, "Model loaded successfully"
        except Exception as e:
            return False, f"Error loading model: {str(e)}"