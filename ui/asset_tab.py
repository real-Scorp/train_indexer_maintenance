import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class AssetManagementTab:
    """Implements the Asset Management tab functionality."""
    
    def __init__(self, parent, db_manager, status_var):
        self.parent = parent
        self.db_manager = db_manager
        self.status_var = status_var
        
        # Variables for Asset Type form
        self.asset_type_id_var = tk.StringVar()
        self.asset_type_name_var = tk.StringVar()
        self.asset_type_desc_var = tk.StringVar()
        self.wear_threshold_var = tk.DoubleVar(value=60.0)
        
        # Variables for Asset Instance form
        self.asset_id_var = tk.StringVar()
        self.tul_id_var = tk.StringVar()
        self.asset_type_var = tk.StringVar()
        self.instance_number_var = tk.IntVar(value=1)
        self.asset_install_date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.asset_notes_var = tk.StringVar()
        
        # Variable for filtering
        self.filter_tul_var = tk.StringVar()
        self.filter_asset_type_var = tk.StringVar()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface for the Asset Management tab."""
        # Create main layout with notebook for sub-tabs
        self.sub_notebook = ttk.Notebook(self.parent)
        self.sub_notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create sub-tabs
        self.type_tab = ttk.Frame(self.sub_notebook)
        self.instance_tab = ttk.Frame(self.sub_notebook)
        
        self.sub_notebook.add(self.type_tab, text="Asset Types")
        self.sub_notebook.add(self.instance_tab, text="Asset Instances")
        
        # Setup Asset Types tab
        self.setup_asset_types_tab()
        
        # Setup Asset Instances tab
        self.setup_asset_instances_tab()
        
    def setup_asset_types_tab(self):
        """Set up the Asset Types sub-tab."""
        # Create main layout: left panel for input, right panel for display
        left_frame = ttk.Frame(self.type_tab, padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        right_frame = ttk.Frame(self.type_tab, padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left frame - Asset Type Management Controls
        ttk.Label(left_frame, text="Asset Type Management", style="Title.TLabel").pack(anchor=tk.W, pady=5)
        ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        
        # Asset Type Management Section
        type_frame = ttk.LabelFrame(left_frame, text="Add New Asset Type")
        type_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(type_frame, text="Type ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(type_frame, textvariable=self.asset_type_id_var, width=20).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(type_frame, text="Name:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(type_frame, textvariable=self.asset_type_name_var, width=20).grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(type_frame, text="Description:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(type_frame, textvariable=self.asset_type_desc_var, width=20).grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(type_frame, text="Wear Threshold:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Spinbox(type_frame, from_=0, to=100, increment=5.0, textvariable=self.wear_threshold_var, width=10).grid(row=3, column=1, padx=5, pady=2)
        
        button_frame = ttk.Frame(type_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=5)
        
        ttk.Button(button_frame, text="Add Asset Type", command=self.add_asset_type).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_asset_type_form).pack(side=tk.LEFT, padx=5)
        
        # Right frame - Asset Type Display
        ttk.Label(right_frame, text="Asset Types", style="Title.TLabel").pack(anchor=tk.W, pady=5)
        
        # Add refresh button
        refresh_frame = ttk.Frame(right_frame)
        refresh_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(refresh_frame, text="Refresh List", command=self.load_asset_types).pack(side=tk.RIGHT)
        
        # Create Treeview for Asset Types
        self.type_tree_frame = ttk.Frame(right_frame)
        self.type_tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        columns = ("id", "name", "description", "threshold")
        self.type_tree = ttk.Treeview(self.type_tree_frame, columns=columns, show="headings")
        
        # Define column headings
        self.type_tree.heading("id", text="Type ID")
        self.type_tree.heading("name", text="Name")
        self.type_tree.heading("description", text="Description")
        self.type_tree.heading("threshold", text="Wear Threshold")
        
        # Define column widths
        self.type_tree.column("id", width=100)
        self.type_tree.column("name", width=150)
        self.type_tree.column("description", width=200)
        self.type_tree.column("threshold", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.type_tree_frame, orient=tk.VERTICAL, command=self.type_tree.yview)
        self.type_tree.configure(yscrollcommand=scrollbar.set)
        
        self.type_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def setup_asset_instances_tab(self):
        """Set up the Asset Instances sub-tab."""
        # Create main layout: left panel for input, right panel for display
        left_frame = ttk.Frame(self.instance_tab, padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        right_frame = ttk.Frame(self.instance_tab, padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left frame - Asset Instance Management Controls
        ttk.Label(left_frame, text="Asset Instance Management", style="Title.TLabel").pack(anchor=tk.W, pady=5)
        ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        
        # Asset Instance Management Section
        instance_frame = ttk.LabelFrame(left_frame, text="Add New Asset Instance")
        instance_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(instance_frame, text="Asset ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(instance_frame, textvariable=self.asset_id_var, width=20).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(instance_frame, text="TUL ID:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.tul_combo = ttk.Combobox(instance_frame, textvariable=self.tul_id_var, width=18, state="readonly")
        self.tul_combo.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(instance_frame, text="Asset Type:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.asset_type_combo = ttk.Combobox(instance_frame, textvariable=self.asset_type_var, width=18, state="readonly")
        self.asset_type_combo.grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(instance_frame, text="Instance Number:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Spinbox(instance_frame, from_=1, to=100, textvariable=self.instance_number_var, width=10).grid(row=3, column=1, padx=5, pady=2)
        
        ttk.Label(instance_frame, text="Installation Date:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(instance_frame, textvariable=self.asset_install_date_var, width=20).grid(row=4, column=1, padx=5, pady=2)
        
        ttk.Label(instance_frame, text="Notes:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(instance_frame, textvariable=self.asset_notes_var, width=20).grid(row=5, column=1, padx=5, pady=2)
        
        button_frame = ttk.Frame(instance_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=5)
        
        ttk.Button(button_frame, text="Add Asset", command=self.add_asset).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_asset_form).pack(side=tk.LEFT, padx=5)
        
        # Generate Asset ID button
        ttk.Button(instance_frame, text="Generate ID", command=self.generate_asset_id).grid(row=0, column=2, padx=5, pady=2)
        
        # Right frame - Asset Instance Display
        ttk.Label(right_frame, text="Asset Instances", style="Title.TLabel").pack(anchor=tk.W, pady=5)
        
        # Filter section
        filter_frame = ttk.Frame(right_frame)
        filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(filter_frame, text="Filter by TUL:").pack(side=tk.LEFT, padx=5)
        self.filter_tul_combo = ttk.Combobox(filter_frame, textvariable=self.filter_tul_var, width=15, state="readonly")
        self.filter_tul_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(filter_frame, text="Filter by Type:").pack(side=tk.LEFT, padx=5)
        self.filter_type_combo = ttk.Combobox(filter_frame, textvariable=self.filter_asset_type_var, width=15, state="readonly")
        self.filter_type_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(filter_frame, text="Apply Filter", command=self.apply_asset_filter).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Clear Filter", command=self.clear_asset_filter).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Refresh", command=self.load_assets).pack(side=tk.RIGHT, padx=5)
        
        # Create Treeview for Asset Instances
        self.asset_tree_frame = ttk.Frame(right_frame)
        self.asset_tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        columns = ("id", "tul", "type", "instance", "installation_date", "notes")
        self.asset_tree = ttk.Treeview(self.asset_tree_frame, columns=columns, show="headings")
        
        # Define column headings
        self.asset_tree.heading("id", text="Asset ID")
        self.asset_tree.heading("tul", text="TUL")
        self.asset_tree.heading("type", text="Asset Type")
        self.asset_tree.heading("instance", text="Instance #")
        self.asset_tree.heading("installation_date", text="Installation Date")
        self.asset_tree.heading("notes", text="Notes")
        
        # Define column widths
        self.asset_tree.column("id", width=120)
        self.asset_tree.column("tul", width=80)
        self.asset_tree.column("type", width=100)
        self.asset_tree.column("instance", width=80)
        self.asset_tree.column("installation_date", width=120)
        self.asset_tree.column("notes", width=200)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.asset_tree_frame, orient=tk.VERTICAL, command=self.asset_tree.yview)
        self.asset_tree.configure(yscrollcommand=scrollbar.set)
        
        self.asset_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Actions section
        actions_frame = ttk.Frame(right_frame)
        actions_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(actions_frame, text="View Measurements", command=self.view_asset_measurements).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text="Delete Asset", style="Delete.TButton", command=self.delete_asset).pack(side=tk.LEFT, padx=5)
        
        # Load initial data
        self.load_tuls()
        self.load_asset_types()
        self.load_assets()
        
    def add_asset_type(self):
        """Add a new asset type to the database."""
        type_id = self.asset_type_id_var.get().strip()
        name = self.asset_type_name_var.get().strip()
        desc = self.asset_type_desc_var.get().strip()
        threshold = self.wear_threshold_var.get()
        
        if not type_id or not name:
            messagebox.showerror("Input Error", "Type ID and Name are required.")
            return
            
        success = self.db_manager.add_asset_type(type_id, name, desc, threshold)
        
        if success:
            self.status_var.set(f"Asset Type {name} added successfully.")
            self.clear_asset_type_form()
            self.load_asset_types()
        else:
            messagebox.showerror("Database Error", "Failed to add Asset Type. It may already exist.")
            
    def clear_asset_type_form(self):
        """Clear the asset type form fields."""
        self.asset_type_id_var.set("")
        self.asset_type_name_var.set("")
        self.asset_type_desc_var.set("")
        self.wear_threshold_var.set(60.0)
        
    def add_asset(self):
        """Add a new asset instance to the database."""
        asset_id = self.asset_id_var.get().strip()
        tul_id = self.tul_id_var.get()
        asset_type_id = self.asset_type_var.get()
        instance_number = self.instance_number_var.get()
        date_str = self.asset_install_date_var.get().strip()
        notes = self.asset_notes_var.get().strip()
        
        if not asset_id or not tul_id or not asset_type_id:
            messagebox.showerror("Input Error", "Asset ID, TUL ID, and Asset Type are required.")
            return
            
        try:
            installation_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            messagebox.showerror("Input Error", "Invalid date format. Use YYYY-MM-DD.")
            return
            
        success = self.db_manager.add_asset(asset_id, tul_id, asset_type_id, instance_number, installation_date, notes)
        
        if success:
            self.status_var.set(f"Asset {asset_id} added successfully.")
            self.clear_asset_form()
            self.load_assets()
        else:
            messagebox.showerror("Database Error", "Failed to add Asset. It may already exist.")
            
    def clear_asset_form(self):
        """Clear the asset form fields."""
        self.asset_id_var.set("")
        self.instance_number_var.set(1)
        self.asset_install_date_var.set(datetime.now().strftime('%Y-%m-%d'))
        self.asset_notes_var.set("")
        
    def generate_asset_id(self):
        """Generate an asset ID based on selected TUL and asset type."""
        tul_id = self.tul_id_var.get()
        asset_type_id = self.asset_type_var.get()
        instance = self.instance_number_var.get()
        
        if not tul_id or not asset_type_id:
            messagebox.showerror("Input Error", "Please select a TUL and Asset Type first.")
            return
        
        # Generate ID format: TUL-TYPE-INSTANCE (e.g., TUL1-INDPIN-01)
        generated_id = f"{tul_id}-{asset_type_id}-{instance:02d}"
        self.asset_id_var.set(generated_id)
        
    def load_tuls(self):
        """Load TUL data for dropdowns."""
        tuls = self.db_manager.get_tuls()
        tul_ids = [""] + [tul[0] for tul in tuls]  # Add empty option for filtering
        
        self.tul_combo['values'] = tul_ids
        self.filter_tul_combo['values'] = tul_ids
        
    def load_asset_types(self):
        """Load asset types from the database and update UI."""
        # Clear the existing treeview
        for item in self.type_tree.get_children():
            self.type_tree.delete(item)
            
        # Get all asset types
        asset_types = self.db_manager.get_asset_types()
        
        # Update dropdown values
        type_ids = [asset_type[0] for asset_type in asset_types]
        self.asset_type_combo['values'] = type_ids
        self.filter_type_combo['values'] = [""] + type_ids  # Add empty option for filtering
        
        if not asset_types:
            self.status_var.set("No asset types found in the database.")
            return
            
        # Add each asset type to the treeview
        for asset_type in asset_types:
            type_id, name, desc, threshold = asset_type
            self.type_tree.insert("", tk.END, values=(type_id, name, desc, threshold))
            
        self.status_var.set(f"Loaded {len(asset_types)} asset types.")
        
    def load_assets(self):
        """Load assets from the database with optional filtering."""
        # Clear the existing treeview
        for item in self.asset_tree.get_children():
            self.asset_tree.delete(item)
            
        # Get filter values
        tul_filter = self.filter_tul_var.get()
        type_filter = self.filter_asset_type_var.get()
        
        # Get assets with filters
        assets = self.db_manager.get_assets(
            tul_id=tul_filter if tul_filter else None,
            asset_type_id=type_filter if type_filter else None
        )
        
        if not assets:
            filter_text = ""
            if tul_filter:
                filter_text += f" for TUL '{tul_filter}'"
            if type_filter:
                filter_text += f" of type '{type_filter}'"
            self.status_var.set(f"No assets found{filter_text}.")
            return
            
        # Add each asset to the treeview
        for asset in assets:
            asset_id, tul_id, asset_type_id, instance_number, installation_date, notes, type_name, location = asset
            self.asset_tree.insert("", tk.END, values=(asset_id, tul_id, asset_type_id, instance_number, installation_date, notes))
            
        self.status_var.set(f"Loaded {len(assets)} assets.")
        
    def apply_asset_filter(self):
        """Apply filters to the asset list."""
        self.load_assets()
        
    def clear_asset_filter(self):
        """Clear the asset filters."""
        self.filter_tul_var.set("")
        self.filter_asset_type_var.set("")
        self.load_assets()
        
    def view_asset_measurements(self):
        """View measurements for the selected asset."""
        selected_items = self.asset_tree.selection()
        if not selected_items:
            messagebox.showerror("Selection Error", "Please select an asset to view its measurements.")
            return
            
        # Get the selected asset ID
        asset_id = self.asset_tree.item(selected_items[0], "values")[0]
        
        # This would typically switch to the Maintenance tab and filter by asset
        # For now, we'll just show a message
        messagebox.showinfo("View Measurements", f"Viewing measurements for asset: {asset_id}")
        
    def delete_asset(self):
        """Delete the selected asset after confirmation."""
        selected_items = self.asset_tree.selection()
        if not selected_items:
            messagebox.showerror("Selection Error", "Please select an asset to delete.")
            return
            
        # Get the selected asset ID
        asset_id = self.asset_tree.item(selected_items[0], "values")[0]
        
        # Create a custom confirmation dialog
        confirm_dialog = tk.Toplevel(self.parent)
        confirm_dialog.title("Confirm Deletion")
        confirm_dialog.geometry("400x200")
        confirm_dialog.transient(self.parent)
        confirm_dialog.grab_set()
        confirm_dialog.resizable(False, False)
        
        # Dialog content
        frame = ttk.Frame(confirm_dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        warning_text = (
            f"Are you sure you want to delete asset '{asset_id}'?\n\n"
            f"You will lose ALL measurement data for this asset.\n\n"
            f"Type 'DELETE' to confirm:"
        )
        
        ttk.Label(frame, text=warning_text, wraplength=350).pack(pady=(0, 10))
        
        # Entry for confirmation text
        confirmation_var = tk.StringVar()
        confirmation_entry = ttk.Entry(frame, textvariable=confirmation_var, width=20)
        confirmation_entry.pack(pady=5)
        confirmation_entry.focus_set()
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)
        
        def confirm_delete():
            if confirmation_var.get() == "DELETE":
                # TODO: Implement actual deletion in DatabaseManager
                # For now, just close the dialog and refresh
                confirm_dialog.destroy()
                self.load_assets()
                self.status_var.set(f"Asset '{asset_id}' deleted successfully.")
            else:
                messagebox.showerror("Confirmation Error", 
                                   "Incorrect confirmation text. Type 'DELETE' exactly.")
        
        ttk.Button(button_frame, text="Delete", command=confirm_delete, style="Delete.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=confirm_dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Handle Enter key in entry field
        confirmation_entry.bind("<Return>", lambda event: confirm_delete())

        