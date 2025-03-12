class Indexer:
    """Model representing a train indexer."""
    
    def __init__(self, indexer_id, location="", installation_date=None, notes=""):
        self.indexer_id = indexer_id
        self.location = location
        self.installation_date = installation_date
        self.notes = notes
        
    def to_dict(self):
        """Convert to dictionary for database storage."""
        return {
            "IndexerID": self.indexer_id,
            "Location": self.location,
            "InstallationDate": self.installation_date,
            "Notes": self.notes
        }