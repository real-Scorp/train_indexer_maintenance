import tkinter as tk
from tkinter import ttk
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data.database_manager import DatabaseManager
from models.indexer import Indexer
from models.measurement import Measurement
from datetime import datetime, timedelta

def test_database_operations():
    """Test basic database operations."""
    print("Testing database operations...")
    
    # Create a test database
    db = DatabaseManager("test_management.db")
    db.connect()
    db.create_tables()
    
    # Add test indexers
    print("Adding test indexers...")
    indexer1_success = db.add_indexer("IDX001", "North Platform", datetime.now().date(), "Test indexer 1")
    indexer2_success = db.add_indexer("IDX002", "South Platform", datetime.now().date(), "Test indexer 2")
    
    if indexer1_success and indexer2_success:
        print("✓ Successfully added test indexers")
    else:
        print("✗ Failed to add test indexers")
    
    # Add test measurements
    print("\nAdding test measurements...")
    today = datetime.now().date()
    
    # Add measurements for IDX001
    measurements_success = True
    for i in range(5):
        date = today - timedelta(days=i*15)  # Measurements every 15 days
        wear = i * 2.5  # Increasing wear values
        shims = 0.0 if i < 4 else 5.0  # Add shims at the last measurement
        
        success = db.add_measurement("IDX001", date, wear, shims, f"Measurement {i+1}")
        if not success:
            measurements_success = False
    
    # Add measurements for IDX002
    for i in range(3):
        date = today - timedelta(days=i*10)  # Measurements every 10 days
        wear = i * 3.2  # Different wear rate
        
        success = db.add_measurement("IDX002", date, wear, 0.0, f"Measurement {i+1}")
        if not success:
            measurements_success = False
    
    if measurements_success:
        print("✓ Successfully added test measurements")
    else:
        print("✗ Failed to add some measurements")
    
    # Retrieve and verify data
    print("\nRetrieving indexers...")
    indexers = db.get_indexers()
    print(f"Found {len(indexers)} indexers:")
    for idx in indexers:
        print(f"  - {idx[0]} (Location: {idx[1]})")
    
    print("\nRetrieving measurements for IDX001...")
    measurements = db.get_measurements("IDX001")
    print(f"Found {len(measurements)} measurements:")
    for m in measurements:
        print(f"  - Date: {m[2]}, Wear: {m[3]:.1f}mm, Shims: {m[4]:.1f}")
    
    # Test CSV export
    print("\nTesting CSV export...")
    export_success = db.export_to_csv("test_export.csv")
    
    if export_success:
        print(f"✓ Successfully exported data to test_export.csv")
    else:
        print("✗ Failed to export data")
    
    print("\nDatabase test completed!")

def test_ui():
    """Launch the UI for manual testing."""
    print("Launching UI for manual testing...")
    print("Please test the following features:")
    print("1. Adding a new indexer")
    print("2. Adding measurements to an indexer")
    print("3. Viewing data for a specific indexer")
    print("4. Viewing all data")
    print("5. Importing and exporting CSV files")
    print("\nClose the window when testing is complete.\n")
    
    # Import here to avoid circular imports
    from main import IndexerApp
    
    root = tk.Tk()
    app = IndexerApp(root)
    root.mainloop()

if __name__ == "__main__":
    # Run database operation tests
    test_database_operations()
    
    # Run UI tests
    user_input = input("\nWould you like to test the UI? (y/n): ")
    if user_input.lower() == 'y':
        test_ui()