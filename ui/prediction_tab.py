import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PredictionTab:
    """Implements the Prediction tab functionality for the expanded asset system."""
    
    def __init__(self, parent, db_manager, prediction_model, status_var):
        self.parent = parent
        self.db_manager = db_manager
        self.status_var = status_var
        self.prediction_model = prediction_model
        
        # Variables for prediction controls
        self.tul_var = tk.StringVar()
        self.asset_type_var = tk.StringVar()
        self.asset_var = tk.StringVar()
        self.days_ahead_var = tk.IntVar(value=90)
        self.threshold_var = tk.DoubleVar(value=60.0)
        self.invert_y_var = tk.BooleanVar(value=True)  # Default to inverted Y-axis
        
        # Create the UI
        self.setup_ui()
        
    def setup_ui(self):
        """Set up a simplified user interface for the prediction tab."""
        # Create main layout with control panel on left, results on right
        left_frame = ttk.Frame(self.parent, padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        right_frame = ttk.Frame(self.parent, padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left frame - Prediction Controls
        ttk.Label(left_frame, text="Wear Prediction", style="Title.TLabel").pack(anchor=tk.W, pady=5)
        ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        
        # Control section
        control_frame = ttk.LabelFrame(left_frame, text="Prediction Controls")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Asset selection
        ttk.Label(control_frame, text="TUL:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.tul_combo = ttk.Combobox(control_frame, textvariable=self.tul_var, width=15, state="readonly")
        self.tul_combo.grid(row=0, column=1, padx=5, pady=5)
        self.tul_combo.bind("<<ComboboxSelected>>", self.on_tul_selected)
        
        ttk.Label(control_frame, text="Asset Type:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.asset_type_combo = ttk.Combobox(control_frame, textvariable=self.asset_type_var, width=15, state="readonly")
        self.asset_type_combo.grid(row=1, column=1, padx=5, pady=5)
        self.asset_type_combo.bind("<<ComboboxSelected>>", self.on_asset_type_selected)
        
        ttk.Label(control_frame, text="Asset:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.asset_combo = ttk.Combobox(control_frame, textvariable=self.asset_var, width=15, state="readonly")
        self.asset_combo.grid(row=2, column=1, padx=5, pady=5)
        
# Prediction parameters
        ttk.Label(control_frame, text="Predict Days Ahead:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Spinbox(control_frame, from_=30, to=365, increment=30, textvariable=self.days_ahead_var, width=10).grid(row=3, column=1, padx=5, pady=5)
        
        # Get threshold for the selected asset type or use default
        ttk.Label(control_frame, text="Wear Threshold (mm):").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        threshold_spinbox = ttk.Spinbox(control_frame, from_=0.1, to=100.0, increment=0.5, textvariable=self.threshold_var, width=10)
        threshold_spinbox.grid(row=4, column=1, padx=5, pady=5)
        
        # Display options
        ttk.Checkbutton(control_frame, text="Invert Y-Axis (Show Wear Downward)", 
                       variable=self.invert_y_var).grid(row=5, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        
        # Action buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Generate Prediction", command=self.generate_prediction).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Show Maintenance Date", command=self.show_maintenance_date).pack(side=tk.LEFT, padx=5)
        
        # Right frame - Results display with tabs
        results_notebook = ttk.Notebook(right_frame)
        results_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Text Results Tab
        self.text_tab = ttk.Frame(results_notebook)
        results_notebook.add(self.text_tab, text="Results")
        
        self.result_text = tk.Text(self.text_tab, wrap=tk.WORD, width=50, height=15)
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=5, padx=5)
        
        # Graph Tab
        self.graph_tab = ttk.Frame(results_notebook)
        results_notebook.add(self.graph_tab, text="Graph")
        
        self.graph_frame = ttk.Frame(self.graph_tab)
        self.graph_frame.pack(fill=tk.BOTH, expand=True)
        
        # Default message in graph frame
        ttk.Label(self.graph_frame, text="Select an asset and click 'Generate Prediction'\nto display the wear chart.", 
                  font=('Arial', 11), foreground='gray').pack(pady=50)
        
        # Load the initial data
        self.load_tuls()
        self.load_asset_types()
        
    def load_tuls(self):
        """Load TUL data for dropdowns."""
        tuls = self.db_manager.get_tuls()
        tul_ids = [row[0] for row in tuls]
        
        self.tul_combo['values'] = tul_ids
        if tul_ids and not self.tul_var.get():
            self.tul_combo.current(0)
            
    def load_asset_types(self):
        """Load asset type data for dropdowns."""
        asset_types = self.db_manager.get_asset_types()
        asset_type_ids = [row[0] for row in asset_types]
        
        self.asset_type_combo['values'] = asset_type_ids
        if asset_type_ids and not self.asset_type_var.get():
            self.asset_type_combo.current(0)
            self.update_threshold()
    
    def update_threshold(self):
        """Update the threshold value based on the selected asset type."""
        asset_type_id = self.asset_type_var.get()
        if not asset_type_id:
            return
            
        # Get asset type details to find the default threshold
        asset_types = self.db_manager.get_asset_types()
        for asset_type in asset_types:
            if asset_type[0] == asset_type_id:
                self.threshold_var.set(asset_type[3])  # Set to WearThreshold value
                break
                
    def on_tul_selected(self, event=None):
        """Handle TUL selection to update asset list."""
        tul_id = self.tul_var.get()
        asset_type_id = self.asset_type_var.get()
        
        if tul_id:
            self.update_asset_list(tul_id, asset_type_id)
    
    def on_asset_type_selected(self, event=None):
        """Handle asset type selection to update asset list and threshold."""
        tul_id = self.tul_var.get()
        asset_type_id = self.asset_type_var.get()
        
        if asset_type_id:
            self.update_asset_list(tul_id, asset_type_id)
            self.update_threshold()
    
    def update_asset_list(self, tul_id=None, asset_type_id=None):
        """Update the asset dropdown based on selected TUL and/or asset type."""
        assets = self.db_manager.get_assets(tul_id=tul_id, asset_type_id=asset_type_id)
        asset_ids = [asset[0] for asset in assets]
        
        self.asset_combo['values'] = asset_ids
        if asset_ids:
            self.asset_combo.current(0)
        else:
            self.asset_var.set("")
    
    def generate_prediction(self):
        """Generate wear prediction for the selected asset."""
        asset_id = self.asset_var.get()
        if not asset_id:
            messagebox.showerror("Selection Error", "Please select an asset.")
            return
            
        # Get the measurement data
        measurements = self.db_manager.get_measurements(asset_id=asset_id)
        if len(measurements) < 3:
            messagebox.showerror("Data Error", 
                f"Not enough measurements for asset {asset_id}. Need at least 3 data points.")
            return
            
        # Get asset and type details for display
        assets = self.db_manager.get_assets()
        asset_details = None
        for asset in assets:
            if asset[0] == asset_id:
                asset_details = asset
                break
                
        if not asset_details:
            messagebox.showerror("Data Error", f"Could not find details for asset {asset_id}.")
            return
            
        tul_id = asset_details[1]
        asset_type_id = asset_details[2]
        instance_num = asset_details[3]
        
        # Process measurement data for modeling
        dates = []
        wear_values = []
        
        # Convert to datetime and prepare for model
        for m in measurements:
            date_str = m[2]
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                dates.append(date)
                wear_values.append(float(m[3]))  # Wear value
            except ValueError:
                continue
        
        if len(dates) < 3:
            messagebox.showerror("Data Error", 
                f"Not enough valid measurements for asset {asset_id}. Need at least 3 data points.")
            return
            
        # Convert dates to days since start
        start_date = min(dates)
        days_since_start = [(date - start_date).days for date in dates]
        
        # Remove duplicates and handle maintenance events
        unique_days_dict = {}
        for i, day in enumerate(days_since_start):
            # Keep the latest measurement for each day
            unique_days_dict[day] = wear_values[i]
        
        clean_days = list(unique_days_dict.keys())
        clean_wear = list(unique_days_dict.values())
        
        # Sort by days
        sorted_indices = sorted(range(len(clean_days)), key=lambda i: clean_days[i])
        clean_days = [clean_days[i] for i in sorted_indices]
        clean_wear = [clean_wear[i] for i in sorted_indices]
        
        # Look for maintenance events (significant drops in wear)
        segments = [[]]
        segment_days = [[]]
        current_segment = 0
        
        for i in range(len(clean_days)):
            # If this is not the first point and there's a significant drop in wear
            if i > 0 and clean_wear[i] < clean_wear[i-1] * 0.5:  # Drop of more than 50%
                # Start a new segment
                current_segment += 1
                segments.append([])
                segment_days.append([])
            
            segments[current_segment].append(clean_wear[i])
            segment_days[current_segment].append(clean_days[i])
        
        # Use the last segment for prediction
        if segments and len(segment_days[-1]) >= 3:
            prediction_days = segment_days[-1]
            prediction_wear = segments[-1]
            
            # Try different polynomial degrees
            best_degree = 1
            best_r2 = -float('inf')
            
            for degree in range(1, min(4, len(prediction_days))):
                temp_model = type(self.prediction_model)(degree=degree)
                success, _ = temp_model.fit(prediction_days, prediction_wear)
                
                if success:
                    # Predict using the model
                    pred, _ = temp_model.predict(prediction_days)
                    
                    # Calculate R²
                    mean_wear = sum(prediction_wear) / len(prediction_wear)
                    ss_total = sum((y - mean_wear) ** 2 for y in prediction_wear)
                    ss_residual = sum((y - p) ** 2 for y, p in zip(prediction_wear, pred))
                    r2 = 1 - (ss_residual / ss_total if ss_total > 0 else 0)
                    
                    if r2 > best_r2:
                        best_r2 = r2
                        best_degree = degree
            
            # Train with best degree
            self.prediction_model = type(self.prediction_model)(degree=best_degree)
            success, message = self.prediction_model.fit(prediction_days, prediction_wear)
            
            if not success:
                messagebox.showerror("Model Error", f"Failed to train model: {message}")
                return
        else:
            # Fall back to all data if no valid segments
            success, message = self.prediction_model.fit(days_since_start, wear_values)
            
            if not success:
                messagebox.showerror("Model Error", f"Failed to train model: {message}")
                return
        
        # Get the threshold value
        threshold = self.threshold_var.get()
        
        # Generate prediction
        days_ahead = self.days_ahead_var.get()
        last_day = max(days_since_start)
        future_days = list(range(last_day + 1, last_day + days_ahead + 1))
        predictions, _ = self.prediction_model.predict(future_days)
        
        # Calculate threshold crossing
        crossing_date, days_until = self.prediction_model.calculate_threshold_crossing(
            start_day=last_day,
            days_ahead=days_ahead,
            start_date=dates[-1],
            threshold=threshold
        )
        
        # Clear previous results
        self.result_text.delete(1.0, tk.END)
        
        # Update result text
        result_text = f"Prediction for {asset_id}:\n\n"
        result_text += f"TUL: {tul_id}\n"
        result_text += f"Asset Type: {asset_type_id}\n"
        result_text += f"Number of measurements: {len(dates)}\n"
        result_text += f"Date range: {min(dates)} to {max(dates)}\n"
        result_text += f"Current wear: {wear_values[-1]:.2f} mm\n\n"
        result_text += f"Predicted wear in {days_ahead} days:\n"
        
        # Show a few prediction points
        for i, day in enumerate(future_days):
            if i % 10 == 0 or i == len(future_days) - 1:  # Show every 10th day and the last day
                future_date = dates[-1] + timedelta(days=day - last_day)
                result_text += f"{future_date}: {predictions[i]:.2f} mm\n"
        
        result_text += f"\nMaintenance threshold: {threshold:.1f} mm\n"
        
        if crossing_date:
            days_text = "day" if days_until == 1 else "days"
            result_text += f"Will be reached in {days_until} {days_text}\n"
            result_text += f"Estimated date: {crossing_date.strftime('%Y-%m-%d')}"
        else:
            result_text += f"Will not be reached within {days_ahead} days"
        
        self.result_text.insert(tk.END, result_text)
        
        # Generate and display the plot
        self.generate_plot(asset_id, tul_id, asset_type_id, dates, wear_values, future_days, predictions, threshold, crossing_date)
        
        self.status_var.set(f"Prediction generated for {asset_id}")
        
    def show_maintenance_date(self):
        """Calculate and display the estimated maintenance date."""
        asset_id = self.asset_var.get()
        if not asset_id:
            messagebox.showerror("Selection Error", "Please select an asset.")
            return
            
        # Check if model has been trained
        if self.prediction_model.model is None:
            # Generate prediction first
            self.generate_prediction()
            return
            
        # Get threshold value
        threshold = self.threshold_var.get()
        
        # Get the last measurement date and wear value
        measurements = self.db_manager.get_measurements(asset_id=asset_id)
        if not measurements:
            messagebox.showerror("Data Error", f"No data found for asset {asset_id}.")
            return
            
        # Sort measurements by date
        sorted_measurements = sorted(measurements, key=lambda m: datetime.strptime(m[2], '%Y-%m-%d'))
        
        # Get first and last measurement
        first_date = datetime.strptime(sorted_measurements[0][2], '%Y-%m-%d').date()
        last_date = datetime.strptime(sorted_measurements[-1][2], '%Y-%m-%d').date()
        last_wear = float(sorted_measurements[-1][3])
        
        # Calculate days since start
        last_day = (last_date - first_date).days
        
        # Calculate maintenance date using extended prediction horizon
        crossing_date, days_until = self.prediction_model.calculate_threshold_crossing(
            start_day=last_day,
            days_ahead=365,  # Look ahead a full year
            start_date=last_date,
            threshold=threshold
        )
        
        if crossing_date:
            # Show maintenance date dialog
            days_text = "day" if days_until == 1 else "days"
            maintenance_info = (
                f"Maintenance for {asset_id}\n\n"
                f"Current wear: {last_wear:.2f} mm\n"
                f"Threshold: {threshold:.1f} mm\n\n"
                f"Estimated maintenance date:\n{crossing_date.strftime('%Y-%m-%d')}\n"
                f"({days_until} {days_text} from last measurement)"
            )
            messagebox.showinfo("Maintenance Date", maintenance_info)
        else:
            messagebox.showinfo("Maintenance Date", 
                f"The maintenance threshold ({threshold:.1f} mm) will not be reached within the next 365 days.")

    def generate_plot(self, asset_id, tul_id, asset_type_id, dates, wear_values, future_days, predictions, threshold, crossing_date):
        """Generate and display a plot with actual measurements and predictions."""
        try:
            # Clear previous content
            for widget in self.graph_frame.winfo_children():
                widget.destroy()
            
            # Create figure and axis
            fig, ax = plt.subplots(figsize=(8, 5))
            
            # Convert future days to dates
            last_date = dates[-1]
            future_dates = [last_date + timedelta(days=day - (dates[-1] - dates[0]).days) for day in future_days]
            
            # Plot historical data
            ax.scatter(dates, wear_values, color='blue', label='Actual Measurements')
            ax.plot(dates, wear_values, 'b-', alpha=0.5)
            
            # Plot prediction
            ax.plot(future_dates, predictions, 'g--', label='Predicted Wear')
            
            # Add maintenance threshold line
            ax.axhline(y=threshold, color='red', linestyle='--', 
                      label=f'Maintenance Threshold ({threshold} mm)')
            
            # Mark crossing date if exists
            if crossing_date:
                ax.axvline(x=crossing_date, color='orange', linestyle='-.',
                          label=f'Threshold Reached ({crossing_date.strftime("%Y-%m-%d")})')
                
                # Add annotation
                ax.annotate(f"Maintenance\nNeeded", 
                           xy=(crossing_date, threshold),
                           xytext=(10, -20), textcoords="offset points",
                           arrowprops=dict(arrowstyle="->", color='orange'),
                           bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.7))
            
            # Invert Y-axis if requested (so wear increases downward)
            if self.invert_y_var.get():
                ax.invert_yaxis()
            
            # Set labels and title
            ax.set_title(f'Wear Prediction for {asset_id} ({tul_id}, {asset_type_id})')
            ax.set_xlabel('Date')
            ax.set_ylabel('Wear (mm)')
            
            # Add grid and legend
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            # Format dates on x-axis
            fig.autofmt_xdate()
            
            # Create canvas
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            ttk.Label(self.graph_frame, text=f"Error creating plot: {str(e)}").pack(pady=20)
            self.status_var.set(f"Error creating plot: {str(e)}")