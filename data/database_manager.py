# File: data/database_manager.py

import sqlite3
import os
import pandas as pd
from datetime import datetime

class DatabaseManager:
    """Handles database connections and operations for the expanded asset management system."""
    
    def __init__(self, db_path="./tul_maintenance.db"):
        self.db_path = db_path
        self.connection = None
        
    def connect(self):
        """Establish connection to the SQLite database."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            return True
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return False
        
    def create_tables(self):
        """Create necessary tables if they don't exist."""
        if not self.connection:
            self.connect()
            
        try:
            cursor = self.connection.cursor()
            
            # Create TULs table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS TULs (
                TULID TEXT PRIMARY KEY,
                Location TEXT,
                InstallationDate DATE,
                Notes TEXT
            )
            ''')
            
            # Create AssetTypes table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS AssetTypes (
                AssetTypeID TEXT PRIMARY KEY,
                Name TEXT,
                Description TEXT,
                WearThreshold REAL
            )
            ''')
            
            # Create Assets table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Assets (
                AssetID TEXT PRIMARY KEY,
                TULID TEXT,
                AssetTypeID TEXT,
                InstanceNumber INTEGER,
                InstallationDate DATE,
                Notes TEXT,
                FOREIGN KEY (TULID) REFERENCES TULs(TULID),
                FOREIGN KEY (AssetTypeID) REFERENCES AssetTypes(AssetTypeID)
            )
            ''')
            
            # Create Measurements table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Measurements (
                MeasurementID INTEGER PRIMARY KEY AUTOINCREMENT,
                AssetID TEXT,
                MeasurementDate DATE,
                WearValue REAL,
                ShimsAdded REAL,
                Notes TEXT,
                FOREIGN KEY (AssetID) REFERENCES Assets(AssetID)
            )
            ''')
            
            # Add default asset types if they don't exist
            cursor.execute("SELECT COUNT(*) FROM AssetTypes")
            count = cursor.fetchone()[0]
            
            if count == 0:
                # Insert default asset types
                asset_types = [
                    ("INDPIN", "Indexer Pinion", "Train indexer pinion gear", 60.0),
                    ("INDROL", "Index Support Roller", "Support roller for the indexer system", 45.0)
                ]
                
                cursor.executemany(
                    "INSERT INTO AssetTypes (AssetTypeID, Name, Description, WearThreshold) VALUES (?, ?, ?, ?)",
                    asset_types
                )
            
            # Add default TULs if they don't exist
            cursor.execute("SELECT COUNT(*) FROM TULs")
            count = cursor.fetchone()[0]
            
            if count == 0:
                # Insert default TULs
                tuls = [
                    ("TUL1", "Train Unloader 1", datetime.now().date(), ""),
                    ("TUL2", "Train Unloader 2", datetime.now().date(), ""),
                    ("TUL3", "Train Unloader 3", datetime.now().date(), "")
                ]
                
                cursor.executemany(
                    "INSERT INTO TULs (TULID, Location, InstallationDate, Notes) VALUES (?, ?, ?, ?)",
                    tuls
                )
            
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Table creation error: {e}")
            return False
    
    # Basic CRUD operations for TULs
    def add_tul(self, tul_id, location, installation_date, notes=""):
        """Add a new TUL to the database."""
        if not self.connection:
            self.connect()
            
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO TULs (TULID, Location, InstallationDate, Notes) VALUES (?, ?, ?, ?)",
                (tul_id, location, installation_date, notes)
            )
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding TUL: {e}")
            return False
    
    def get_tuls(self):
        """Get all TULs from the database."""
        if not self.connection:
            self.connect()
            
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT TULID, Location, InstallationDate, Notes FROM TULs ORDER BY TULID")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting TULs: {e}")
            return []
    
    def delete_tul(self, tul_id):
        """Delete a TUL and all its associated assets and measurements."""
        if not self.connection:
            self.connect()
            
        try:
            cursor = self.connection.cursor()
            
            # First get all assets for this TUL
            cursor.execute("SELECT AssetID FROM Assets WHERE TULID = ?", (tul_id,))
            assets = cursor.fetchall()
            
            # Delete all measurements for these assets
            for asset in assets:
                cursor.execute("DELETE FROM Measurements WHERE AssetID = ?", (asset[0],))
            
            # Delete all assets for this TUL
            cursor.execute("DELETE FROM Assets WHERE TULID = ?", (tul_id,))
            
            # Finally delete the TUL
            cursor.execute("DELETE FROM TULs WHERE TULID = ?", (tul_id,))
            
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting TUL: {e}")
            return False
    
    # Basic CRUD operations for Asset Types
    def add_asset_type(self, type_id, name, description, wear_threshold):
        """Add a new asset type to the database."""
        if not self.connection:
            self.connect()
            
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO AssetTypes (AssetTypeID, Name, Description, WearThreshold) VALUES (?, ?, ?, ?)",
                (type_id, name, description, wear_threshold)
            )
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding asset type: {e}")
            return False
    
    def get_asset_types(self):
        """Get all asset types from the database."""
        if not self.connection:
            self.connect()
            
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT AssetTypeID, Name, Description, WearThreshold FROM AssetTypes ORDER BY Name")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting asset types: {e}")
            return []
    
    def delete_asset_type(self, type_id):
        """Delete an asset type if no assets are using it."""
        if not self.connection:
            self.connect()
            
        try:
            cursor = self.connection.cursor()
            
            # Check if any assets use this type
            cursor.execute("SELECT COUNT(*) FROM Assets WHERE AssetTypeID = ?", (type_id,))
            count = cursor.fetchone()[0]
            
            if count > 0:
                return False, f"Cannot delete asset type {type_id}. It is used by {count} assets."
            
            # Delete the asset type
            cursor.execute("DELETE FROM AssetTypes WHERE AssetTypeID = ?", (type_id,))
            self.connection.commit()
            return True, ""
        except sqlite3.Error as e:
            print(f"Error deleting asset type: {e}")
            return False, str(e)
    
    # Basic CRUD operations for Assets
    def add_asset(self, asset_id, tul_id, asset_type_id, instance_number, installation_date, notes=""):
        """Add a new asset to the database."""
        if not self.connection:
            self.connect()
            
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO Assets (AssetID, TULID, AssetTypeID, InstanceNumber, InstallationDate, Notes) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (asset_id, tul_id, asset_type_id, instance_number, installation_date, notes)
            )
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding asset: {e}")
            return False
    
    def get_assets(self, tul_id=None, asset_type_id=None):
        """Get assets filtered by TUL and/or asset type."""
        if not self.connection:
            self.connect()
            
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT a.AssetID, a.TULID, a.AssetTypeID, a.InstanceNumber, a.InstallationDate, a.Notes,
                       t.Name as AssetTypeName, tul.Location
                FROM Assets a
                JOIN AssetTypes t ON a.AssetTypeID = t.AssetTypeID
                JOIN TULs tul ON a.TULID = tul.TULID
            """
            
            params = []
            if tul_id and asset_type_id:
                query += " WHERE a.TULID = ? AND a.AssetTypeID = ?"
                params = [tul_id, asset_type_id]
            elif tul_id:
                query += " WHERE a.TULID = ?"
                params = [tul_id]
            elif asset_type_id:
                query += " WHERE a.AssetTypeID = ?"
                params = [asset_type_id]
                
            query += " ORDER BY a.TULID, a.AssetTypeID, a.InstanceNumber"
            
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting assets: {e}")
            return []
    
    def delete_asset(self, asset_id):
        """Delete an asset and all its associated measurements."""
        if not self.connection:
            self.connect()
            
        try:
            cursor = self.connection.cursor()
            
            # Delete all measurements for this asset
            cursor.execute("DELETE FROM Measurements WHERE AssetID = ?", (asset_id,))
            
            # Delete the asset
            cursor.execute("DELETE FROM Assets WHERE AssetID = ?", (asset_id,))
            
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting asset: {e}")
            return False
    
    # CRUD operations for Measurements
    def add_measurement(self, asset_id, measurement_date, wear_value, shims_added=0, notes=""):
        """Add a new measurement record."""
        if not self.connection:
            self.connect()
            
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO Measurements (AssetID, MeasurementDate, WearValue, ShimsAdded, Notes) "
                "VALUES (?, ?, ?, ?, ?)",
                (asset_id, measurement_date, wear_value, shims_added, notes)
            )
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding measurement: {e}")
            return False
    
    def get_measurements(self, asset_id=None, tul_id=None, asset_type_id=None):
        """Get measurements filtered by asset, TUL, and/or asset type."""
        if not self.connection:
            self.connect()
            
        try:
            cursor = self.connection.cursor()
            
            base_query = """
                SELECT m.MeasurementID, m.AssetID, m.MeasurementDate, m.WearValue, m.ShimsAdded, m.Notes,
                       a.TULID, a.AssetTypeID, a.InstanceNumber, t.Name as AssetTypeName
                FROM Measurements m
                JOIN Assets a ON m.AssetID = a.AssetID
                JOIN AssetTypes t ON a.AssetTypeID = t.AssetTypeID
            """
            
            params = []
            if asset_id:
                query = base_query + " WHERE m.AssetID = ? ORDER BY m.MeasurementDate"
                params = [asset_id]
            elif tul_id and asset_type_id:
                query = base_query + " WHERE a.TULID = ? AND a.AssetTypeID = ? ORDER BY a.InstanceNumber, m.MeasurementDate"
                params = [tul_id, asset_type_id]
            elif tul_id:
                query = base_query + " WHERE a.TULID = ? ORDER BY a.AssetTypeID, a.InstanceNumber, m.MeasurementDate"
                params = [tul_id]
            elif asset_type_id:
                query = base_query + " WHERE a.AssetTypeID = ? ORDER BY a.TULID, a.InstanceNumber, m.MeasurementDate"
                params = [asset_type_id]
            else:
                query = base_query + " ORDER BY a.TULID, a.AssetTypeID, a.InstanceNumber, m.MeasurementDate"
            
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting measurements: {e}")
            return []
    
    def delete_measurement(self, measurement_id):
        """Delete a measurement record by ID."""
        if not self.connection:
            self.connect()
            
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM Measurements WHERE MeasurementID = ?", (measurement_id,))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting measurement: {e}")
            return False
    
    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None