from datetime import datetime

class Measurement:
    """Model representing an indexer wear measurement."""
    
    def __init__(self, indexer_id, measurement_date=None, wear_value=0.0, 
                 shims_added=0.0, notes="", measurement_id=None):
        self.measurement_id = measurement_id
        self.indexer_id = indexer_id
        self.measurement_date = measurement_date or datetime.now().date()
        self.wear_value = wear_value
        self.shims_added = shims_added
        self.notes = notes
        
    def to_dict(self):
        """Convert to dictionary for database storage."""
        return {
            "MeasurementID": self.measurement_id,
            "IndexerID": self.indexer_id,
            "MeasurementDate": self.measurement_date,
            "WearValue": self.wear_value,
            "ShimsAdded": self.shims_added,
            "Notes": self.notes
        }