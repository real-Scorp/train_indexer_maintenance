import sys
import os
import random
import math
from datetime import datetime, timedelta
import sqlite3

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.database_manager import DatabaseManager

def generate_sample_data():
    """Generate realistic sample data with maintenance before thresholds are exceeded."""
    print("Generating sample data with realistic wear patterns and maintenance events...")
    
    # Initialize the database manager
    db_manager = DatabaseManager()
    db_manager.connect()
    db_manager.create_tables()
    
    # Clear existing data if requested
    if input("Clear existing data? (y/n): ").lower() == 'y':
        try:
            conn = sqlite3.connect(db_manager.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Measurements")
            cursor.execute("DELETE FROM Assets")
            conn.commit()
            conn.close()
            print("Existing measurements and assets cleared.")
        except Exception as e:
            print(f"Error clearing data: {e}")
    
    # Get existing TULs
    tuls = db_manager.get_tuls()
    if not tuls:
        print("No TULs found. Please run the application first to initialize the database.")
        return
    
    # Get asset types
    asset_types = db_manager.get_asset_types()
    if not asset_types:
        print("No asset types found. Please run the application first to initialize the database.")
        return
    
    # Generate assets and measurements
    today = datetime.now().date()
    three_years_ago = today - timedelta(days=3*365)
    
    # For each TUL, create 8 pinions and 8 rollers
    for tul in tuls:
        tul_id = tul[0]
        print(f"Adding assets and measurements for {tul_id}...")
        
        # Randomly select outliers
        pinion_outlier = random.randint(1, 8)
        roller_outlier = random.randint(1, 8)
        
        print(f"  - Outlier pinion: #{pinion_outlier}")
        print(f"  - Outlier roller: #{roller_outlier}")
        
        # Add 8 Pinions per TUL
        for i in range(1, 9):
            asset_id = f"{tul_id}-INDPIN-{i:02d}"
            install_date = three_years_ago + timedelta(days=random.randint(0, 30))  # Installed ~3 years ago
            
            # Add the asset
            db_manager.add_asset(
                asset_id=asset_id,
                tul_id=tul_id,
                asset_type_id="INDPIN",
                instance_number=i,
                installation_date=install_date,
                notes=f"Pinion {i} for {tul_id}"
            )
            
            # Set outlier status
            is_outlier = (i == pinion_outlier)
            
            # Generate measurements every 12 weeks
            generate_measurements(
                db_manager, 
                asset_id, 
                install_date, 
                is_outlier=is_outlier, 
                is_pinion=True,
                outlier_factor=1.5  # Outliers wear 50% faster (reduced from 80%)
            )
        
        # Add 8 Rollers per TUL
        for i in range(1, 9):
            asset_id = f"{tul_id}-INDROL-{i:02d}"
            install_date = three_years_ago + timedelta(days=random.randint(0, 30))  # Installed ~3 years ago
            
            # Add the asset
            db_manager.add_asset(
                asset_id=asset_id,
                tul_id=tul_id,
                asset_type_id="INDROL",
                instance_number=i,
                installation_date=install_date,
                notes=f"Roller {i} for {tul_id}"
            )
            
            # Set outlier status
            is_outlier = (i == roller_outlier)
            
            # Generate measurements every 12 weeks
            generate_measurements(
                db_manager, 
                asset_id, 
                install_date, 
                is_outlier=is_outlier, 
                is_pinion=False,
                outlier_factor=1.4  # Outliers wear 40% faster (reduced from 70%)
            )
    
    print("Sample data generation complete!")

def generate_measurements(db_manager, asset_id, install_date, is_outlier=False, is_pinion=True, outlier_factor=1.5):
    """Generate measurements every 12 weeks with realistic maintenance events that reset wear to 0."""
    today = datetime.now().date()
    
    # Get asset type and its threshold
    asset_type_id = "INDPIN" if is_pinion else "INDROL"
    
    # Find the appropriate threshold for this asset type
    asset_types = db_manager.get_asset_types()
    threshold = None
    for at in asset_types:
        if at[0] == asset_type_id:
            threshold = at[3]  # WearThreshold value
            break
    
    if threshold is None:
        threshold = 60.0 if is_pinion else 45.0  # Default values if not found
    
    # Set maintenance threshold to 90% of wear threshold
    maintenance_threshold = threshold * 0.9
    
    # Set up wear rate parameters based on asset type
    if is_pinion:
        # Pinions wear faster
        base_wear_rate = random.uniform(1.8, 2.4)  # mm per 30 days (reduced from 2.6-3.2)
    else:
        # Rollers wear slower
        base_wear_rate = random.uniform(1.2, 1.8)  # mm per 30 days (reduced from 1.6-2.4)
    
    # Enhance wear rate for outliers
    if is_outlier:
        base_wear_rate *= outlier_factor
    
    # Measurements occur every 12 weeks (84 days)
    measurement_interval = 84  # 12 weeks
    
    # Generate measurement dates spanning 3 years
    measurement_dates = []
    current_date = install_date + timedelta(days=measurement_interval)
    
    while current_date <= today:
        measurement_dates.append(current_date)
        current_date += timedelta(days=measurement_interval)
    
    # Generate wear values for each date
    last_maintenance_date = install_date
    accumulated_wear = 0.0
    maintenance_count = 0
    
    # Create acceleration/deceleration pattern
    # This will generate a value between 0.7 and 1.3 that varies over time
    def wear_multiplier(days):
        # Create a pattern that varies over time
        cycle1 = math.sin(days / 180 * math.pi)  # Long cycle (180 days)
        cycle2 = math.sin(days / 60 * math.pi) * 0.3  # Medium cycle (60 days)
        cycle3 = math.sin(days / 20 * math.pi) * 0.1  # Short cycle (20 days)
        
        # Combine cycles and normalize to range 0.7-1.3
        multiplier = 1.0 + (cycle1 + cycle2 + cycle3) * 0.3
        
        # Add some randomness
        multiplier += random.uniform(-0.05, 0.05)
        
        return round(multiplier, 2)  # Round to 2 decimal places
    
    # Schedule some random maintenance events (about 1-2 per year)
    # These simulate scheduled maintenance rather than threshold-based
    scheduled_maintenance_dates = set()
    num_years = min(3, (today - install_date).days // 365)
    
    for year in range(num_years):
        # Add 1-2 random maintenance dates per year
        maintenance_count = random.randint(1, 2)
        year_start = install_date + timedelta(days=year*365)
        
        for _ in range(maintenance_count):
            # Random day within this year
            random_day = random.randint(0, 364)
            maint_date = year_start + timedelta(days=random_day)
            if maint_date <= today and (maint_date - install_date).days >= 60:  # At least 60 days after installation
                scheduled_maintenance_dates.add(maint_date)
    
    # Generate and add measurements
    last_wear_value = 0.0
    for idx, date in enumerate(measurement_dates):
        # Calculate days since last maintenance
        days_since_maintenance = (date - last_maintenance_date).days
        
        # Calculate wear rate with acceleration/deceleration
        current_rate = base_wear_rate * wear_multiplier(days_since_maintenance)
        
        # Calculate wear since last measurement or maintenance
        period_wear = current_rate * days_since_maintenance / 30
        accumulated_wear += period_wear
        
        # Round to 2 decimal places for realism
        wear_value = round(accumulated_wear, 2)
        
        # Check for maintenance conditions:
        # 1. Scheduled maintenance occurred before this measurement
        # 2. Wear value exceeded maintenance threshold
        
        # Find the most recent scheduled maintenance before this measurement
        scheduled_maintenance_before = False
        for maint_date in scheduled_maintenance_dates:
            if last_maintenance_date < maint_date < date:
                scheduled_maintenance_before = True
                last_maintenance_date = maint_date
                break
        
        # Check if wear threshold would be exceeded
        threshold_exceeded = wear_value >= maintenance_threshold
        
        if scheduled_maintenance_before:
            # Reset accumulated wear for this measurement due to scheduled maintenance
            notes = f"Scheduled maintenance performed on {last_maintenance_date}. Wear reset from approximately {last_wear_value:.2f} mm to 0 mm."
            accumulated_wear = 0.0
            wear_value = 0.0
            maintenance_count += 1
        elif threshold_exceeded:
            # Reset wear due to exceeding threshold
            notes = f"Maintenance performed as wear reached {wear_value:.2f} mm (threshold: {maintenance_threshold:.2f} mm). Wear reset to 0 mm."
            last_maintenance_date = date
            accumulated_wear = 0.0
            wear_value = 0.0
            maintenance_count += 1
        elif is_outlier and wear_value > (threshold * 0.6):
            notes = f"Higher than expected wear rate ({current_rate:.2f} mm/month), monitoring closely"
        else:
            notes = f"Regular 12-week measurement, current wear rate: {current_rate:.2f} mm/month"
        
        # Store current wear value for reference in next cycle
        last_wear_value = wear_value
        
        # Add the measurement to the database (with ShimsAdded=0)
        db_manager.add_measurement(
            asset_id=asset_id,
            measurement_date=date,
            wear_value=wear_value,
            shims_added=0,  # Keep this for now until we refactor to remove shims
            notes=notes
        )
    
    # Log summary
    print(f"Added {len(measurement_dates)} measurements for {asset_id}")
    print(f"  - {maintenance_count} maintenance events that reset wear to 0")
    print(f"  - Base rate: {base_wear_rate:.2f}mm/month (Outlier: {is_outlier})")

if __name__ == "__main__":
    generate_sample_data()