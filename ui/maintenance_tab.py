import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class MaintenanceTab:
    """Implements the Maintenance Records tab functionality for the expanded asset system."""
    
    def __init__(self, parent, db_manager, status_var):
        self.parent = parent
        self.db_manager = db_manager
        self.status_var = status_var
        
        # Variables for maintenance form
        self.tul_var = tk.StringVar()
        self.asset_type_var = tk.StringVar()
        self.asset_var = tk.StringVar()
        self.wear_var = tk.DoubleVar(value=0.0)
        self.shims_var = tk.DoubleVar(value=0.0)
        self.notes_var = tk.StringVar()
        self.date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        
        # Variables for filtering
        self.filter_tul_var = tk.StringVar()
        self.filter_asset_type_var = tk.StringVar()
        self.filter_asset_var = tk.StringVar()
        
        # Create the UI
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface for the maintenance tab."""
        # Create main layout: left panel for input, right panel for display
        left_frame = ttk.Frame(self.parent, padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        right_frame = ttk.Frame(self.parent, padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    
        style = ttk.Style()
        style.configure("Delete.TButton", foreground="red")

        # Left frame - Maintenance Records Input
        ttk.Label(left_frame, text="Add Maintenance Record", style="Title.TLabel").pack(anchor=tk.W, pady=5)
        
        # Asset selection and data entry
        input_frame = ttk.LabelFrame(left_frame, text="Maintenance Details")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # TUL, Asset Type, and Asset selection
        ttk.Label(input_frame, text="TUL:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.tul_combo = ttk.Combobox(input_frame, textvariable=self.tul_var, width=15, state="readonly")
        self.tul_combo.grid(row=0, column=1, padx=5, pady=5)
        self.tul_combo.bind("<<ComboboxSelected>>", self.on_tul_selected)
        
        ttk.Label(input_frame, text="Asset Type:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.asset_type_combo = ttk.Combobox(input_frame, textvariable=self.asset_type_var, width=15, state="readonly")
        self.asset_type_combo.grid(row=1, column=1, padx=5, pady=5)
        self.asset_type_combo.bind("<<ComboboxSelected>>", self.on_asset_type_selected)
        
        ttk.Label(input_frame, text="Asset:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.asset_combo = ttk.Combobox(input_frame, textvariable=self.asset_var, width=15, state="readonly")
        self.asset_combo.grid(row=2, column=1, padx=5, pady=5)
        
        # Measurement details
        ttk.Label(input_frame, text="Date:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        date_entry = ttk.Entry(input_frame, textvariable=self.date_var, width=15)
        date_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Wear Measurement (mm):").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Spinbox(input_frame, from_=0, to=100, increment=0.1, textvariable=self.wear_var, width=15).grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Shims Added:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Spinbox(input_frame, from_=0, to=20, increment=0.5, textvariable=self.shims_var, width=15).grid(row=5, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Notes:").grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.notes_var, width=20).grid(row=6, column=1, padx=5, pady=5)
        
        # Add buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Add Record", command=self.add_maintenance_record).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        
        # Right frame - Maintenance History Display
        ttk.Label(right_frame, text="Maintenance History", style="Title.TLabel").pack(anchor=tk.W, pady=5)
        
        # Filter controls
        filter_frame = ttk.Frame(right_frame)
        filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(filter_frame, text="Filter by TUL:").pack(side=tk.LEFT, padx=5)
        self.filter_tul_combo = ttk.Combobox(filter_frame, textvariable=self.filter_tul_var, width=10, state="readonly")
        self.filter_tul_combo.pack(side=tk.LEFT, padx=5)
        self.filter_tul_combo.bind("<<ComboboxSelected>>", self.on_filter_tul_selected)
        
        ttk.Label(filter_frame, text="Asset Type:").pack(side=tk.LEFT, padx=5)
        self.filter_type_combo = ttk.Combobox(filter_frame, textvariable=self.filter_asset_type_var, width=10, state="readonly")
        self.filter_type_combo.pack(side=tk.LEFT, padx=5)
        self.filter_type_combo.bind("<<ComboboxSelected>>", self.on_filter_type_selected)
        
        ttk.Label(filter_frame, text="Asset:").pack(side=tk.LEFT, padx=5)
        self.filter_asset_combo = ttk.Combobox(filter_frame, textvariable=self.filter_asset_var, width=15, state="readonly")
        self.filter_asset_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(filter_frame, text="Apply Filter", command=self.filter_records).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Clear Filters", command=self.clear_filters).pack(side=tk.LEFT, padx=5)
        
        # Create a Treeview for maintenance records
        self.tree_frame = ttk.Frame(right_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        columns = ("date", "tul", "asset_type", "asset", "wear", "shims", "notes")
        self.history_tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", selectmode="browse")
        
        # Define column headings
        self.history_tree.heading("date", text="Date")
        self.history_tree.heading("tul", text="TUL")
        self.history_tree.heading("asset_type", text="Asset Type")
        self.history_tree.heading("asset", text="Asset")
        self.history_tree.heading("wear", text="Wear (mm)")
        self.history_tree.heading("shims", text="Shims Added")
        self.history_tree.heading("notes", text="Notes")
        
        # Define column widths
        self.history_tree.column("date", width=90)
        self.history_tree.column("tul", width=70)
        self.history_tree.column("asset_type", width=90)
        self.history_tree.column("asset", width=100)
        self.history_tree.column("wear", width=80)
        self.history_tree.column("shims", width=80)
        self.history_tree.column("notes", width=200, stretch=tk.YES)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add context menu
        self.context_menu = tk.Menu(self.history_tree, tearoff=0)
        self.context_menu.add_command(label="View Details", command=self.view_record_details)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Delete Record", command=self.delete_record)
        
        self.history_tree.bind("<Button-3>", self.show_context_menu)
        self.history_tree.bind("<Delete>", lambda event: self.delete_record())

        # Create a button panel for record operations
        button_panel = ttk.Frame(right_frame)
        button_panel.pack(fill=tk.X, pady=5)

        ttk.Button(button_panel, text="View Details", command=self.view_record_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_panel, text="Delete Record", command=self.delete_record, 
                style="Delete.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_panel, text="Refresh", command=self.load_all_maintenance_records).pack(side=tk.RIGHT, padx=5)
        
        # Load the initial data
        self.refresh_dropdowns()
        self.load_all_maintenance_records()
        
    def refresh_dropdowns(self):
        """Refresh all dropdown lists."""
        # Load TULs
        tuls = self.db_manager.get_tuls()
        tul_ids = [row[0] for row in tuls]
        
        self.tul_combo['values'] = tul_ids
        self.filter_tul_combo['values'] = [""] + tul_ids  # Add empty option for filtering
        
        # Load Asset Types
        asset_types = self.db_manager.get_asset_types()
        asset_type_ids = [row[0] for row in asset_types]
        
        self.asset_type_combo['values'] = asset_type_ids
        self.filter_type_combo['values'] = [""] + asset_type_ids  # Add empty option for filtering
        
    def on_tul_selected(self, event=None):
        """Handle TUL selection to update asset list."""
        tul_id = self.tul_var.get()
        asset_type_id = self.asset_type_var.get()
        
        if tul_id:
            self.update_asset_list(tul_id, asset_type_id)
    
    def on_asset_type_selected(self, event=None):
        """Handle asset type selection to update asset list."""
        tul_id = self.tul_var.get()
        asset_type_id = self.asset_type_var.get()
        
        if asset_type_id:
            self.update_asset_list(tul_id, asset_type_id)
    
    def update_asset_list(self, tul_id=None, asset_type_id=None):
        """Update the asset dropdown based on selected TUL and/or asset type."""
        assets = self.db_manager.get_assets(tul_id=tul_id, asset_type_id=asset_type_id)
        asset_ids = [asset[0] for asset in assets]
        
        self.asset_combo['values'] = asset_ids
        if asset_ids:
            self.asset_combo.current(0)
        else:
            self.asset_var.set("")
    
    def on_filter_tul_selected(self, event=None):
        """Handle filter TUL selection."""
        tul_id = self.filter_tul_var.get()
        asset_type_id = self.filter_asset_type_var.get()
        
        # Update asset type options if needed
        if tul_id:
            assets = self.db_manager.get_assets(tul_id=tul_id)
            asset_types = set(asset[2] for asset in assets)
            self.filter_type_combo['values'] = [""] + list(asset_types)
        
        # Update asset list
        self.update_filter_asset_list(tul_id, asset_type_id)
    
    def on_filter_type_selected(self, event=None):
        """Handle filter asset type selection."""
        tul_id = self.filter_tul_var.get()
        asset_type_id = self.filter_asset_type_var.get()
        
        # Update TUL options if needed
        if asset_type_id and not tul_id:
            assets = self.db_manager.get_assets(asset_type_id=asset_type_id)
            tuls = set(asset[1] for asset in assets)
            self.filter_tul_combo['values'] = [""] + list(tuls)
        
        # Update asset list
        self.update_filter_asset_list(tul_id, asset_type_id)
    
    def update_filter_asset_list(self, tul_id=None, asset_type_id=None):
        """Update the filter asset dropdown based on selected TUL and/or asset type."""
        assets = self.db_manager.get_assets(
            tul_id=tul_id if tul_id else None,
            asset_type_id=asset_type_id if asset_type_id else None
        )
        asset_ids = [asset[0] for asset in assets]
        
        self.filter_asset_combo['values'] = [""] + asset_ids
        self.filter_asset_var.set("")
    
    def add_maintenance_record(self):
        """Add a new maintenance record."""
        asset_id = self.asset_var.get()
        if not asset_id:
            messagebox.showerror("Input Error", "Please select an asset.")
            return
            
        date_str = self.date_var.get().strip()
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            messagebox.showerror("Input Error", "Invalid date format. Please use YYYY-MM-DD.")
            return
            
        wear = self.wear_var.get()
        shims = self.shims_var.get()
        notes = self.notes_var.get()
        
        # Add to database
        success = self.db_manager.add_measurement(asset_id, date, wear, shims, notes)
        
        if success:
            self.status_var.set(f"Maintenance record added for {asset_id}")
            self.clear_form()
            self.load_all_maintenance_records()
        else:
            messagebox.showerror("Database Error", "Failed to add maintenance record.")
            
    def clear_form(self):
            """Clear the maintenance form."""
            self.wear_var.set(0.0)
            self.shims_var.set(0.0)
            self.notes_var.set("")
            self.date_var.set(datetime.now().strftime('%Y-%m-%d'))
    
    def filter_records(self):
        """Apply filters to show specific maintenance records."""
        self.load_filtered_records()
        
    def clear_filters(self):
        """Clear all filters and show all records."""
        self.filter_tul_var.set("")
        self.filter_asset_type_var.set("")
        self.filter_asset_var.set("")
        self.load_all_maintenance_records()
    
    def load_filtered_records(self):
        """Load maintenance records with the current filters applied."""
        # Clear existing data
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
            
        # Get filter values
        tul_id = self.filter_tul_var.get() if self.filter_tul_var.get() else None
        asset_type_id = self.filter_asset_type_var.get() if self.filter_asset_type_var.get() else None
        asset_id = self.filter_asset_var.get() if self.filter_asset_var.get() else None
        
        # Build filter description
        filter_desc = ""
        if asset_id:
            filter_desc = f"for asset '{asset_id}'"
        elif tul_id and asset_type_id:
            filter_desc = f"for {asset_type_id} assets in {tul_id}"
        elif tul_id:
            filter_desc = f"for all assets in {tul_id}"
        elif asset_type_id:
            filter_desc = f"for all {asset_type_id} assets"
        
        # Get measurements with filters
        measurements = self.db_manager.get_measurements(
            asset_id=asset_id,
            tul_id=tul_id,
            asset_type_id=asset_type_id
        )
        
        if not measurements:
            self.status_var.set(f"No maintenance records found {filter_desc}")
            return
            
        # Sort by date (newest first)
        measurements.sort(key=lambda m: datetime.strptime(m[2], '%Y-%m-%d'), reverse=True)
        
        # Add to treeview
        for m in measurements:
            measurement_id = m[0]
            asset_id = m[1]
            date = m[2]
            wear = float(m[3])
            shims = float(m[4])
            notes = m[5] or ""
            tul_id = m[6]
            asset_type_id = m[7]
            
            self.history_tree.insert("", tk.END, iid=str(measurement_id),
                                    values=(date, tul_id, asset_type_id, asset_id, f"{wear:.1f}", f"{shims:.1f}", notes))
            
        self.status_var.set(f"Showing {len(measurements)} maintenance records {filter_desc}")
        
    def load_all_maintenance_records(self):
        """Load all maintenance records into the treeview."""
        # Clear existing data
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
            
        # Get all measurements
        measurements = self.db_manager.get_measurements()
        
        if not measurements:
            self.status_var.set("No maintenance records found")
            return
            
        # Sort by date (newest first)
        measurements.sort(key=lambda m: datetime.strptime(m[2], '%Y-%m-%d'), reverse=True)
        
        # Add to treeview
        for m in measurements:
            measurement_id = m[0]
            asset_id = m[1]
            date = m[2]
            wear = float(m[3])
            shims = float(m[4])
            notes = m[5] or ""
            tul_id = m[6]
            asset_type_id = m[7]
            
            self.history_tree.insert("", tk.END, iid=str(measurement_id),
                                    values=(date, tul_id, asset_type_id, asset_id, f"{wear:.1f}", f"{shims:.1f}", notes))
            
        self.status_var.set(f"Showing all maintenance records ({len(measurements)} total)")
        
    def show_context_menu(self, event):
        """Show the context menu on right-click."""
        item = self.history_tree.identify_row(event.y)
        if item:
            self.history_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
            
    def view_record_details(self):
        """View details of the selected maintenance record."""
        selected_item = self.history_tree.selection()
        if not selected_item:
            return
            
        record_id = selected_item[0]
        values = self.history_tree.item(record_id, "values")
        
        # Create a details window
        details_window = tk.Toplevel(self.parent)
        details_window.title("Maintenance Record Details")
        details_window.geometry("400x320")
        details_window.transient(self.parent)
        details_window.grab_set()
        
        # Display details
        detail_frame = ttk.Frame(details_window, padding=20)
        detail_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(detail_frame, text="Maintenance Record Details", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=10)
        
        details = [
            ("Date:", values[0]),
            ("TUL:", values[1]),
            ("Asset Type:", values[2]),
            ("Asset ID:", values[3]),
            ("Wear Measurement:", f"{values[4]} mm"),
            ("Shims Added:", values[5]),
            ("Notes:", values[6])
        ]
        
        for i, (label, value) in enumerate(details):
            row_frame = ttk.Frame(detail_frame)
            row_frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(row_frame, text=label, width=15, font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
            ttk.Label(row_frame, text=value, wraplength=250).pack(side=tk.LEFT, padx=5)
        
        # Add close button
        ttk.Button(detail_frame, text="Close", command=details_window.destroy).pack(pady=15)

    def delete_record(self):
        """Delete the selected maintenance record."""
        selected_item = self.history_tree.selection()
        if not selected_item:
            messagebox.showinfo("Selection Required", "Please select a record to delete.")
            return
            
        record_id = selected_item[0]
        values = self.history_tree.item(record_id, "values")
        
        # Get record information for confirmation message
        date = values[0]
        tul_id = values[1]
        asset_id = values[3]
        wear = values[4]
        
        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete this record?\n\n"
            f"TUL: {tul_id}\n"
            f"Asset: {asset_id}\n"
            f"Date: {date}\n"
            f"Wear: {wear}",
            icon=messagebox.WARNING
        )
        
        if confirm:
            # Delete from database
            success = self.db_manager.delete_measurement(int(record_id))
            
            if success:
                # Remove from treeview
                self.history_tree.delete(record_id)
                self.status_var.set(f"Record deleted for {asset_id} on {date}")
            else:
                messagebox.showerror("Database Error", "Failed to delete record from database.")