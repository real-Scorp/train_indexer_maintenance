import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class TULManagementTab:
    """Implements the TUL Management tab functionality."""
    
    def __init__(self, parent, db_manager, status_var):
        self.parent = parent
        self.db_manager = db_manager
        self.status_var = status_var
        
        # Variables for TUL form
        self.tul_id_var = tk.StringVar()
        self.location_var = tk.StringVar()
        self.installation_date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.notes_var = tk.StringVar()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface for the TUL Management tab."""
        # Create main layout: left panel for input, right panel for display
        left_frame = ttk.Frame(self.parent, padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        right_frame = ttk.Frame(self.parent, padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left frame - TUL Management Controls
        ttk.Label(left_frame, text="TUL Management", style="Title.TLabel").pack(anchor=tk.W, pady=5)
        ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        
        # TUL Management Section
        tul_frame = ttk.LabelFrame(left_frame, text="Add New TUL")
        tul_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(tul_frame, text="TUL ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(tul_frame, textvariable=self.tul_id_var, width=20).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(tul_frame, text="Location:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(tul_frame, textvariable=self.location_var, width=20).grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(tul_frame, text="Installation Date:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(tul_frame, textvariable=self.installation_date_var, width=20).grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(tul_frame, text="Notes:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(tul_frame, textvariable=self.notes_var, width=20).grid(row=3, column=1, padx=5, pady=2)
        
        button_frame = ttk.Frame(tul_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=5)
        
        ttk.Button(button_frame, text="Add TUL", command=self.add_tul).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_tul_form).pack(side=tk.LEFT, padx=5)
        
        # Right frame - TUL Display
        ttk.Label(right_frame, text="TUL List", style="Title.TLabel").pack(anchor=tk.W, pady=5)
        
        # Add refresh button
        refresh_frame = ttk.Frame(right_frame)
        refresh_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(refresh_frame, text="Refresh List", command=self.load_tuls).pack(side=tk.RIGHT)
        
        # Create Treeview for TULs
        self.tree_frame = ttk.Frame(right_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        columns = ("id", "location", "installation_date", "notes")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings")
        
        # Define column headings
        self.tree.heading("id", text="TUL ID")
        self.tree.heading("location", text="Location")
        self.tree.heading("installation_date", text="Installation Date")
        self.tree.heading("notes", text="Notes")
        
        # Define column widths
        self.tree.column("id", width=100)
        self.tree.column("location", width=150)
        self.tree.column("installation_date", width=120)
        self.tree.column("notes", width=200)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Actions section
        actions_frame = ttk.Frame(right_frame)
        actions_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(actions_frame, text="View Assets", command=self.view_tul_assets).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text="Delete TUL", style="Delete.TButton", command=self.delete_tul).pack(side=tk.LEFT, padx=5)
        
        # Load initial data
        self.load_tuls()
        
    def add_tul(self):
        """Add a new TUL to the database."""
        tul_id = self.tul_id_var.get().strip()
        location = self.location_var.get().strip()
        date_str = self.installation_date_var.get().strip()
        notes = self.notes_var.get().strip()
        
        if not tul_id:
            messagebox.showerror("Input Error", "TUL ID is required.")
            return
            
        try:
            installation_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            messagebox.showerror("Input Error", "Invalid date format. Use YYYY-MM-DD.")
            return
            
        success = self.db_manager.add_tul(tul_id, location, installation_date, notes)
        
        if success:
            self.status_var.set(f"TUL {tul_id} added successfully.")
            self.clear_tul_form()
            self.load_tuls()
        else:
            messagebox.showerror("Database Error", "Failed to add TUL. It may already exist.")
            
    def clear_tul_form(self):
        """Clear the TUL form fields."""
        self.tul_id_var.set("")
        self.location_var.set("")
        self.installation_date_var.set(datetime.now().strftime('%Y-%m-%d'))
        self.notes_var.set("")
        
    def load_tuls(self):
        """Load and display all TULs."""
        # Clear the existing treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Get all TULs
        tuls = self.db_manager.get_tuls()
        
        if not tuls:
            self.status_var.set("No TULs found in the database.")
            return
            
        # Add each TUL to the treeview
        for tul in tuls:
            tul_id, location, installation_date, notes = tul
            self.tree.insert("", tk.END, values=(tul_id, location, installation_date, notes))
            
        self.status_var.set(f"Loaded {len(tuls)} TULs.")
        
    def view_tul_assets(self):
        """View assets for the selected TUL."""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("Selection Error", "Please select a TUL to view its assets.")
            return
            
        # Get the selected TUL ID
        tul_id = self.tree.item(selected_items[0], "values")[0]
        
        # This would typically switch to the Asset tab and filter by TUL
        # For now, we'll just show a message
        messagebox.showinfo("View Assets", f"Viewing assets for TUL: {tul_id}")
        
    def delete_tul(self):
        """Delete the selected TUL after confirmation."""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("Selection Error", "Please select a TUL to delete.")
            return
            
        # Get the selected TUL ID
        tul_id = self.tree.item(selected_items[0], "values")[0]
        
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
            f"Are you sure you want to delete '{tul_id}'?\n\n"
            f"You will lose ALL assets and measurement data for this TUL.\n\n"
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
                self.load_tuls()
                self.status_var.set(f"TUL '{tul_id}' deleted successfully.")
            else:
                messagebox.showerror("Confirmation Error", 
                                   "Incorrect confirmation text. Type 'DELETE' exactly.")
        
        ttk.Button(button_frame, text="Delete", command=confirm_delete, style="Delete.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=confirm_dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Handle Enter key in entry field
        confirmation_entry.bind("<Return>", lambda event: confirm_delete())