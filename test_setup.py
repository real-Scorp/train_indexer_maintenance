from data.database_manager import DatabaseManager
from models.indexer import Indexer
from models.measurement import Measurement
from models.prediction_model import WearPredictionModel
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt

def test_database():
    """Test database setup and operations."""
    print("Testing database connection...")
    db = DatabaseManager("test.db")
    db.connect()
    db.create_tables()
    print("Database created successfully!")
    
def test_prediction_model():
    """Test prediction model functionality."""
    print("Testing prediction model...")
    
    # Create some sample data
    days = list(range(10))
    # Non-linear wear pattern (polynomial)
    wear = [0.0, 0.5, 1.5, 3.0, 5.0, 7.5, 10.5, 14.0, 18.0, 22.5]
    
    # Train model
    model = WearPredictionModel(degree=2)
    success, message = model.fit(days, wear)
    print(f"Model training: {message}")
    
    # Predict future
    future_days = list(range(15))
    predictions, _ = model.predict(future_days)
    
    # Calculate threshold crossing
    today = datetime.now().date()
    crossing_date, days_until = model.calculate_threshold_crossing(
        start_day=days[-1], 
        days_ahead=30, 
        start_date=today, 
        threshold=25.0
    )
    
    if crossing_date:
        print(f"Maintenance needed on: {crossing_date} (in {days_until} days)")
    else:
        print("No maintenance needed within prediction window")
    
    # Plot results
    plt.figure(figsize=(10, 6))
    plt.scatter(days, wear, color='blue', label='Actual Data')
    plt.plot(future_days, predictions, color='red', label='Predictions')
    plt.axhline(y=25.0, color='green', linestyle='--', label='Maintenance Threshold')
    plt.xlabel('Days')
    plt.ylabel('Wear (mm)')
    plt.title('Indexer Wear Prediction')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('prediction_test.png')
    plt.close()
    
    print("Prediction test complete! Check prediction_test.png for results.")

if __name__ == "__main__":
    test_database()
    test_prediction_model()

