# File: ui/data_tab.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from datetime import datetime



class DataManagementTab:
    """Implements the Data Management tab functionality."""
    
    def __init__(self, parent, db_manager, status_var):
        self.parent = parent
        self.db_manager = db_manager
        self.status_var = status_var
        self.indexer_var = tk.StringVar()
        self.location_var = tk.StringVar()
        self.installation_date_var = tk.StringVar()
        self.notes_var = tk.StringVar()
        self.setup_ui()


        
        
    def setup_ui(self):
        """Set up the user interface for the data tab."""
        # Create main frames
        left_frame = ttk.Frame(self.parent, padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        right_frame = ttk.Frame(self.parent, padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left frame - Data Management Controls
        ttk.Label(left_frame, text="Data Management", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=5)
        ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        
        # Indexer Management Section
        ttk.Label(left_frame, text="Indexer Management", font=('Arial', 11)).pack(anchor=tk.W, pady=5)
        
        indexer_frame = ttk.LabelFrame(left_frame, text="Add New Indexer")
        indexer_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(indexer_frame, text="Indexer ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(indexer_frame, textvariable=self.indexer_var, width=20).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(indexer_frame, text="Location:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(indexer_frame, textvariable=self.location_var, width=20).grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(indexer_frame, text="Installation Date:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        date_entry = ttk.Entry(indexer_frame, textvariable=self.installation_date_var, width=20)
        date_entry.grid(row=2, column=1, padx=5, pady=2)
        date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        ttk.Label(indexer_frame, text="Notes:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(indexer_frame, textvariable=self.notes_var, width=20).grid(row=3, column=1, padx=5, pady=2)
        
        button_frame = ttk.Frame(indexer_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=5)
        
        ttk.Button(button_frame, text="Add Indexer", command=self.add_indexer).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_indexer_form).pack(side=tk.LEFT, padx=5)
        
        # Measurement Management Section
        ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(left_frame, text="Measurement Management", font=('Arial', 11)).pack(anchor=tk.W, pady=5)
        
        measurement_frame = ttk.LabelFrame(left_frame, text="Add New Measurement")
        measurement_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(measurement_frame, text="Select Indexer:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.indexer_combo = ttk.Combobox(measurement_frame, width=18, state="readonly")
        self.indexer_combo.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(measurement_frame, text="Measurement Date:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.measurement_date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        date_entry = ttk.Entry(measurement_frame, textvariable=self.measurement_date_var, width=20)
        date_entry.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(measurement_frame, text="Wear Value (mm):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.wear_var = tk.DoubleVar()
        ttk.Spinbox(measurement_frame, from_=0, to=50, increment=0.1, textvariable=self.wear_var, width=18).grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(measurement_frame, text="Shims Added:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.shims_var = tk.DoubleVar()
        ttk.Spinbox(measurement_frame, from_=0, to=20, increment=0.5, textvariable=self.shims_var, width=18).grid(row=3, column=1, padx=5, pady=2)
        
        ttk.Label(measurement_frame, text="Notes:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        self.measurement_notes_var = tk.StringVar() 
        ttk.Entry(measurement_frame, textvariable=self.measurement_notes_var, width=20).grid(row=4, column=1, padx=5, pady=2)
        
        button_frame = ttk.Frame(measurement_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=5)
        
        ttk.Button(button_frame, text="Add Measurement", command=self.add_measurement).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_measurement_form).pack(side=tk.LEFT, padx=5)
        
        # Data Import/Export Section
        ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(left_frame, text="Data Import/Export", font=('Arial', 11)).pack(anchor=tk.W, pady=5)
        
        import_export_frame = ttk.Frame(left_frame)
        import_export_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(import_export_frame, text="Import from CSV", command=self.import_from_csv).pack(fill=tk.X, pady=2)
        ttk.Button(import_export_frame, text="Export to CSV", command=self.export_to_csv).pack(fill=tk.X, pady=2)
        
        # Right frame - Data Display
        ttk.Label(right_frame, text="Indexer Data", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=5)
        
        # Indexer selection for viewing
        selection_frame = ttk.Frame(right_frame)
        selection_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(selection_frame, text="Select Indexer:").pack(side=tk.LEFT, padx=5)
        self.view_indexer_combo = ttk.Combobox(selection_frame, width=20, state="readonly")
        self.view_indexer_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(selection_frame, text="View Data", command=self.view_indexer_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(selection_frame, text="View All", command=self.view_all_data).pack(side=tk.LEFT, padx=5)

        # Delete Indexer button
        style = ttk.Style()
        style.configure("Delete.TButton", foreground="red")
        ttk.Button(selection_frame, text="Delete Indexer", 
          command=self.delete_indexer, 
          style="Delete.TButton").pack(side=tk.LEFT, padx=5)

        # Treeview for data display
        self.tree_frame = ttk.Frame(right_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create Treeview widget
        self.tree = ttk.Treeview(self.tree_frame, columns=("Date", "Wear", "Shims", "Notes"), show="headings")
        self.tree.heading("Date", text="Measurement Date")
        self.tree.heading("Wear", text="Wear Value (mm)")
        self.tree.heading("Shims", text="Shims Added")
        self.tree.heading("Notes", text="Notes")
        
        self.tree.column("Date", width=120)
        self.tree.column("Wear", width=100)
        self.tree.column("Shims", width=100)
        self.tree.column("Notes", width=200)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load the initial data
        self.refresh_indexer_lists()
        
    def refresh_indexer_lists(self):
        """Refresh all comboboxes with current indexer IDs."""
        indexers = self.db_manager.get_indexers()
        indexer_ids = [row[0] for row in indexers]
        
        # Update comboboxes
        self.indexer_combo['values'] = indexer_ids
        self.view_indexer_combo['values'] = indexer_ids
        
        # Set default selection if available
        if indexer_ids:
            if not self.indexer_combo.get():
                self.indexer_combo.current(0)
            if not self.view_indexer_combo.get():
                self.view_indexer_combo.current(0)
                
    def add_indexer(self):
        """Add a new indexer to the database."""
        indexer_id = self.indexer_var.get().strip()
        location = self.location_var.get().strip()
        date_str = self.installation_date_var.get().strip()
        notes = self.notes_var.get().strip()
        
        if not indexer_id:
            messagebox.showerror("Input Error", "Indexer ID is required.")
            return
            
        try:
            installation_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            messagebox.showerror("Input Error", "Invalid date format. Use YYYY-MM-DD.")
            return
            
        success = self.db_manager.add_indexer(indexer_id, location, installation_date, notes)
        
        if success:
            self.status_var.set(f"Indexer {indexer_id} added successfully.")
            self.clear_indexer_form()
            self.refresh_indexer_lists()
        else:
            messagebox.showerror("Database Error", "Failed to add indexer. It may already exist.")
            
    def clear_indexer_form(self):
        """Clear the indexer form fields."""
        self.indexer_var.set("")
        self.location_var.set("")
        self.installation_date_var.set(datetime.now().strftime('%Y-%m-%d'))
        self.notes_var.set("")
        
    def add_measurement(self):
        """Add a new measurement to the database."""
        indexer_id = self.indexer_combo.get()
        date_str = self.measurement_date_var.get().strip()
        wear_value = self.wear_var.get()
        shims_added = self.shims_var.get()
        notes = self.measurement_notes_var.get().strip()
        
        if not indexer_id:
            messagebox.showerror("Input Error", "Please select an indexer.")
            return
            
        try:
            measurement_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            messagebox.showerror("Input Error", "Invalid date format. Use YYYY-MM-DD.")
            return
            
        success = self.db_manager.add_measurement(
            indexer_id, measurement_date, wear_value, shims_added, notes)
        
        if success:
            self.status_var.set(f"Measurement added for {indexer_id}.")
            self.clear_measurement_form()
            
            # Refresh view if current indexer is being viewed
            if self.view_indexer_combo.get() == indexer_id:
                self.view_indexer_data()
        else:
            messagebox.showerror("Database Error", "Failed to add measurement.")
            
    def clear_measurement_form(self):
        """Clear the measurement form fields."""
        self.measurement_date_var.set(datetime.now().strftime('%Y-%m-%d'))
        self.wear_var.set(0.0)
        self.shims_var.set(0.0)
        self.measurement_notes_var.set("")
        
    def view_indexer_data(self):
        """View data for the selected indexer."""
        indexer_id = self.view_indexer_combo.get()
        
        if not indexer_id:
            messagebox.showerror("Selection Error", "Please select an indexer to view.")
            return
            
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Get measurements for this indexer
        measurements = self.db_manager.get_measurements(indexer_id)
        
        if not measurements:
            self.status_var.set(f"No data found for indexer {indexer_id}.")
            return
            
        # Add data to treeview
        for row in measurements:
            # row format: [measurement_id, indexer_id, date, wear, shims, notes]
            date_str = row[2]
            wear = float(row[3])
            shims = float(row[4])
            notes = row[5] or ""
            
            self.tree.insert("", tk.END, values=(date_str, f"{wear:.2f}", f"{shims:.1f}", notes))
            
        self.status_var.set(f"Displaying data for indexer {indexer_id}.")
        
    def view_all_data(self):
        """View data for all indexers."""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Get all measurements
        measurements = self.db_manager.get_measurements()
        
        if not measurements:
            self.status_var.set("No data found in the database.")
            return
            
        # Add data to treeview
        for row in measurements:
            # row format: [measurement_id, indexer_id, date, wear, shims, notes]
            indexer_id = row[1]
            date_str = row[2]
            wear = float(row[3])
            shims = float(row[4])
            notes = row[5] or ""
            
            # Include indexer ID in display for all data view
            display_notes = f"[{indexer_id}] {notes}"
            
            self.tree.insert("", tk.END, values=(date_str, f"{wear:.2f}", f"{shims:.1f}", display_notes))
            
        self.status_var.set("Displaying data for all indexers.")
        
    def import_from_csv(self):
        """Import data from a CSV file."""
        filename = filedialog.askopenfilename(
            title="Select CSV File to Import",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not filename:
            return
            
        try:
            success = self.db_manager.import_from_csv(filename)
            if success:
                self.refresh_indexer_lists()
                self.status_var.set(f"Data imported successfully from {filename}")
                messagebox.showinfo("Import Successful", "Data has been imported from the CSV file.")
            else:
                messagebox.showerror("Import Error", "Failed to import data from CSV.")
        except Exception as e:
            messagebox.showerror("Import Error", f"Error importing data: {str(e)}")
            
    def export_to_csv(self):
        """Export data to a CSV file."""
        indexer_id = self.view_indexer_combo.get()
        
        # Determine export mode (all or specific indexer)
        if not indexer_id:
            export_all = messagebox.askyesno("Export Selection", 
                "No indexer selected. Export data for all indexers?")
            if not export_all:
                return
            selected_indexer = None
        else:
            export_selected = messagebox.askyesno("Export Selection",
                f"Export data for indexer {indexer_id} only?")
            selected_indexer = indexer_id if export_selected else None
        
        # Get file path for export
        filename = filedialog.asksaveasfilename(
            title="Save CSV File",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not filename:
            return
            
        try:
            success = self.db_manager.export_to_csv(filename, selected_indexer)
            if success:
                self.status_var.set(f"Data exported successfully to {filename}")
                messagebox.showinfo("Export Successful", "Data has been exported to the CSV file.")
            else:
                messagebox.showerror("Export Error", "Failed to export data to CSV.")
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting data: {str(e)}")

    def delete_indexer(self):
        """Delete the selected indexer after confirmation."""
        indexer_id = self.view_indexer_combo.get()
        
        if not indexer_id:
            messagebox.showerror("Selection Error", "Please select an indexer to delete.")
            return
            
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
            f"Are you sure you want to delete '{indexer_id}'?\n\n"
            f"You will lose ALL data on this indexer, including maintenance history.\n\n"
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
                success = self.db_manager.delete_indexer(indexer_id)
                if success:
                    self.status_var.set(f"Indexer '{indexer_id}' and all associated data deleted.")
                    self.refresh_indexer_lists()
                    confirm_dialog.destroy()
                    # Clear the tree view
                    for item in self.tree.get_children():
                        self.tree.delete(item)
                else:
                    messagebox.showerror("Deletion Error", 
                                    f"Failed to delete indexer '{indexer_id}'. Please try again.")
            else:
                messagebox.showerror("Confirmation Error", 
                                "Incorrect confirmation text. Type 'DELETE' exactly.")
        
        ttk.Button(button_frame, text="Delete", command=confirm_delete, style="Delete.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=confirm_dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Handle Enter key in entry field
        confirmation_entry.bind("<Return>", lambda event: confirm_delete())
        
        # Handle window close event
        confirm_dialog.protocol("WM_DELETE_WINDOW", confirm_dialog.destroy)

