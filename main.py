import tkinter as tk
from tkinter import ttk
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data.database_manager import DatabaseManager
from models.prediction_model import WearPredictionModel
from ui.tul_tab import TULManagementTab
from ui.asset_tab import AssetManagementTab
from ui.maintenance_tab import MaintenanceTab
from ui.prediction_tab import PredictionTab
from ui.comparison_tab import ComparisonTab

def is_dark_mode():
    """Check if the system is in dark mode (macOS)."""
    try:
        import subprocess
        result = subprocess.run(
            ['defaults', 'read', '-g', 'AppleInterfaceStyle'], 
            capture_output=True, 
            text=True
        )
        return result.stdout.strip() == 'Dark'
    except Exception:
        # If there's any error, assume light mode
        return False

class TULApp:
    """Main application for TUL asset wear prediction and maintenance tracking."""
    
    def __init__(self, root):
        self.root = root
        self.db_manager = DatabaseManager()
        self.prediction_model = WearPredictionModel()
        
        # Initialize database
        self.db_manager.connect()
        self.db_manager.create_tables()
        
        # Set up the UI
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        self.root.title("TUL Asset Maintenance Tracker")
        self.root.geometry("1200x800")
        
        # Set up styles for the UI
        self.setup_styles()
        
        # Create main notebook with tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.tul_tab = ttk.Frame(self.notebook)
        self.asset_tab = ttk.Frame(self.notebook)
        self.maintenance_tab = ttk.Frame(self.notebook)
        self.prediction_tab = ttk.Frame(self.notebook)
        self.comparison_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tul_tab, text="TUL Management")
        self.notebook.add(self.asset_tab, text="Asset Management")
        self.notebook.add(self.maintenance_tab, text="Maintenance Records")
        self.notebook.add(self.prediction_tab, text="Wear Prediction")
        self.notebook.add(self.comparison_tab, text="Comparison Analysis")

        # Company footer
        footer_frame = ttk.Frame(self.root)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        company_label = ttk.Label(
            footer_frame, 
            text="Developed by OreChain Labs 🧬", 
            font=('Arial', 12, 'italic'),
            foreground='#555555',  # Dark gray color
            anchor=tk.E  # Right-aligned
        )
        company_label.pack(side=tk.TOP, fill=tk.X, padx=10, pady=2)
        company_label.configure(anchor=tk.CENTER)

        # Add status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Initialize tabs
        self.tul_management_tab = TULManagementTab(self.tul_tab, self.db_manager, self.status_var)
        self.asset_management_tab = AssetManagementTab(self.asset_tab, self.db_manager, self.status_var)
        self.maintenance_tab_ui = MaintenanceTab(self.maintenance_tab, self.db_manager, self.status_var)
        self.prediction_tab_ui = PredictionTab(self.prediction_tab, self.db_manager, self.prediction_model, self.status_var)
        self.comparison_tab_ui = ComparisonTab(self.comparison_tab, self.db_manager, self.prediction_model, self.status_var)
    
    def setup_styles(self):
        """Set up custom styles for the application."""
        style = ttk.Style()
        
        # Check if dark mode is enabled
        is_dark = is_dark_mode()
        
        if is_dark:
            # Dark mode theme
            style.configure("TFrame", background="#2E2E2E")
            style.configure("TLabel", background="#2E2E2E", foreground="#FFFFFF")
            style.configure("TButton", background="#505050", foreground="#FFFFFF")
            style.configure("TEntry", fieldbackground="#3E3E3E", foreground="#FFFFFF")
            style.configure("TCombobox", fieldbackground="#3E3E3E", foreground="#FFFFFF")
            style.configure("TNotebook", background="#2E2E2E", tabmargins=[2, 5, 2, 0])
            style.configure("TNotebook.Tab", background="#2E2E2E", foreground="#FFFFFF", padding=[10, 2])
            style.map("TNotebook.Tab", background=[("selected", "#505050")])
            
            style.configure("Delete.TButton", foreground="#FF6B6B")
        else:
            # Light mode theme
            style.configure("Delete.TButton", foreground="#D32F2F")
        
        # Common styles
        style.configure("Title.TLabel", font=("Arial", 14, "bold"))
        style.configure("Subtitle.TLabel", font=("Arial", 12, "bold"))

def main(): 
    """Main function to start the application."""
    root = tk.Tk()
    app = TULApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()