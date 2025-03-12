import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import statistics

class ComparisonTab:
    """Implements the Comparison Analysis tab functionality."""
    
    def __init__(self, parent, db_manager, prediction_model, status_var):
        self.parent = parent
        self.db_manager = db_manager
        self.prediction_model = prediction_model
        self.status_var = status_var
        
        # Variables for comparison controls
        self.comparison_mode_var = tk.StringVar(value="By Asset Type")
        self.tul_var = tk.StringVar()
        self.asset_type_var = tk.StringVar()
        self.time_range_var = tk.StringVar(value="All Time")
        self.invert_y_var = tk.BooleanVar(value=True)  # Default to inverted Y-axis
        self.highlight_outliers_var = tk.BooleanVar(value=True)
        
        # UI components
        self.canvas = None
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface for the comparison tab."""
        # Create main layout with control panel at top, graph below
        control_frame = ttk.Frame(self.parent, padding="10")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        graph_frame = ttk.Frame(self.parent, padding="10")
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Control panel
        ttk.Label(control_frame, text="Comparison Analysis", style="Title.TLabel").grid(row=0, column=0, columnspan=6, sticky=tk.W, pady=5)
        
        # Comparison mode (radio buttons)
        mode_frame = ttk.LabelFrame(control_frame, text="Comparison Mode")
        mode_frame.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        
        ttk.Radiobutton(mode_frame, text="By Asset Type", variable=self.comparison_mode_var, 
                        value="By Asset Type", command=self.update_filters).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Radiobutton(mode_frame, text="By TUL", variable=self.comparison_mode_var, 
                        value="By TUL", command=self.update_filters).pack(anchor=tk.W, padx=5, pady=2)
        
        # Filters
        filter_frame = ttk.LabelFrame(control_frame, text="Filters")
        filter_frame.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(filter_frame, text="TUL:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.tul_combo = ttk.Combobox(filter_frame, textvariable=self.tul_var, width=15, state="readonly")
        self.tul_combo.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(filter_frame, text="Asset Type:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.asset_type_combo = ttk.Combobox(filter_frame, textvariable=self.asset_type_var, width=15, state="readonly")
        self.asset_type_combo.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(filter_frame, text="Time Range:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        time_range_combo = ttk.Combobox(filter_frame, textvariable=self.time_range_var, width=15, state="readonly")
        time_range_combo.grid(row=2, column=1, padx=5, pady=2)
        time_range_combo['values'] = ["All Time", "Last Year", "Last 6 Months", "Last 3 Months", "Last Month"]
        
        # Options
        options_frame = ttk.LabelFrame(control_frame, text="Display Options")
        options_frame.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        
        ttk.Checkbutton(options_frame, text="Invert Y-Axis (Show Wear Downward)", 
                        variable=self.invert_y_var).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Checkbutton(options_frame, text="Highlight Outliers", 
                        variable=self.highlight_outliers_var).pack(anchor=tk.W, padx=5, pady=2)
        
        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=1, column=3, padx=5, pady=5, sticky=tk.E)
        
        ttk.Button(button_frame, text="Generate Comparison", command=self.generate_comparison).pack(side=tk.TOP, pady=2)
        ttk.Button(button_frame, text="Export Graph", command=self.export_graph).pack(side=tk.TOP, pady=2)
        
        # Graph frame
        self.graph_container = ttk.Frame(graph_frame)
        self.graph_container.pack(fill=tk.BOTH, expand=True)
        
        # Add default message in graph container
        self.placeholder_label = ttk.Label(
            self.graph_container, 
            text="Select comparison options and click 'Generate Comparison' to visualize wear patterns",
            font=('Arial', 11),
            foreground='gray'
        )
        self.placeholder_label.pack(pady=100)
        
        # Load initial data
        self.load_tuls()
        self.load_asset_types()
        self.update_filters()
        
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
            
    def update_filters(self, event=None):
        """Update the filter options based on the comparison mode."""
        mode = self.comparison_mode_var.get()
        
        if mode == "By Asset Type":
            # When comparing by asset type, TUL can be optional
            self.tul_combo.config(state="readonly")
            self.asset_type_combo.config(state="readonly")
        else:  # By TUL
            # When comparing by TUL, asset type can be optional
            self.tul_combo.config(state="readonly")
            self.asset_type_combo.config(state="readonly")
            
    def generate_comparison(self):
        """Generate the comparison visualization based on selected options."""
        mode = self.comparison_mode_var.get()
        tul_id = self.tul_var.get()
        asset_type_id = self.asset_type_var.get()
        time_range = self.time_range_var.get()
        
        # Validate selections
        if mode == "By Asset Type" and not asset_type_id:
            messagebox.showerror("Selection Error", "Please select an Asset Type for comparison.")
            return
        
        if mode == "By TUL" and not tul_id:
            messagebox.showerror("Selection Error", "Please select a TUL for comparison.")
            return
        
        # Clear the graph container
        for widget in self.graph_container.winfo_children():
            widget.destroy()
            
        # Get the data based on comparison mode
        if mode == "By Asset Type":
            # Get assets of the selected type, optionally filtered by TUL
            assets = self.db_manager.get_assets(tul_id=tul_id if tul_id else None, asset_type_id=asset_type_id)
            
            if not assets:
                ttk.Label(self.graph_container, text="No assets found matching the selected criteria", 
                          font=('Arial', 11), foreground='gray').pack(pady=100)
                return
                
            title = f"{asset_type_id} Wear Comparison"
            if tul_id:
                title += f" in {tul_id}"
                
            # Get measurements for these assets
            all_measurements = []
            for asset in assets:
                asset_id = asset[0]
                measurements = self.db_manager.get_measurements(asset_id=asset_id)
                if measurements:
                    all_measurements.append((asset_id, measurements))
                    
            self.plot_comparison(all_measurements, title, time_range)
                
        else:  # By TUL
            # Get assets in the selected TUL, optionally filtered by type
            assets = self.db_manager.get_assets(tul_id=tul_id, asset_type_id=asset_type_id if asset_type_id else None)
            
            if not assets:
                ttk.Label(self.graph_container, text="No assets found matching the selected criteria", 
                          font=('Arial', 11), foreground='gray').pack(pady=100)
                return
                
            title = f"{tul_id} Wear Comparison"
            if asset_type_id:
                title += f" for {asset_type_id} Assets"
                
            # Get measurements for these assets
            all_measurements = []
            for asset in assets:
                asset_id = asset[0]
                measurements = self.db_manager.get_measurements(asset_id=asset_id)
                if measurements:
                    all_measurements.append((asset_id, measurements))
                    
            self.plot_comparison(all_measurements, title, time_range)
            
    def plot_comparison(self, all_measurements, title, time_range):
        """Plot the comparison chart based on measurement data."""
        if not all_measurements:
            ttk.Label(self.graph_container, text="No measurement data available for the selected assets", 
                      font=('Arial', 11), foreground='gray').pack(pady=100)
            return
            
        # Create figure and axis
        fig = plt.Figure(figsize=(10, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        # Filter by time range if needed
        cutoff_date = None
        if time_range != "All Time":
            today = datetime.now().date()
            if time_range == "Last Year":
                cutoff_date = today - timedelta(days=365)
            elif time_range == "Last 6 Months":
                cutoff_date = today - timedelta(days=180)
            elif time_range == "Last 3 Months":
                cutoff_date = today - timedelta(days=90)
            elif time_range == "Last Month":
                cutoff_date = today - timedelta(days=30)
        
        # Process and plot data for each asset
        colors = plt.cm.tab10.colors
        markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p', '*', 'h']
        
        # First pass: collect all wear rates for outlier detection
        all_wear_rates = []
        processed_data = []
        
        for i, (asset_id, measurements) in enumerate(all_measurements):
            # Sort by date
            measurements.sort(key=lambda m: datetime.strptime(m[2], '%Y-%m-%d'))
            
            # Filter by time range if needed
            if cutoff_date:
                filtered_measurements = [m for m in measurements if datetime.strptime(m[2], '%Y-%m-%d').date() >= cutoff_date]
                if filtered_measurements:
                    measurements = filtered_measurements
                    
            # Skip if no measurements
            if len(measurements) < 2:
                continue
                
            # Extract dates and wear values
            dates = [datetime.strptime(m[2], '%Y-%m-%d').date() for m in measurements]
            wear_values = [float(m[3]) for m in measurements]
            
            # Calculate days since first measurement for each asset
            start_date = dates[0]
            days = [(date - start_date).days for date in dates]
            
            # Calculate wear rate (mm per day)
            total_days = days[-1]
            if total_days > 0:  # Avoid division by zero
                wear_rate = (wear_values[-1] - wear_values[0]) / total_days
                all_wear_rates.append(wear_rate)
                
                # Store processed data for plotting
                processed_data.append({
                    'asset_id': asset_id,
                    'dates': dates,
                    'days': days,
                    'wear_values': wear_values,
                    'wear_rate': wear_rate
                })
        
        # Skip plotting if no valid data
        if not processed_data:
            ttk.Label(self.graph_container, text="No valid measurement data available for comparison", 
                      font=('Arial', 11), foreground='gray').pack(pady=100)
            return
        
        # Calculate outlier thresholds if needed
        outlier_threshold = None
        if self.highlight_outliers_var.get() and len(all_wear_rates) >= 3:
            median_rate = statistics.median(all_wear_rates)
            mad = statistics.median([abs(rate - median_rate) for rate in all_wear_rates])
            outlier_threshold = median_rate + (3 * mad)  # Using Median Absolute Deviation
            
        # Second pass: plot the data
        for i, data in enumerate(processed_data):
            color_idx = i % len(colors)
            marker_idx = i % len(markers)
            
            # Check if this asset's wear rate is an outlier
            is_outlier = outlier_threshold and data['wear_rate'] > outlier_threshold
            
            # Set line properties
            line_props = {
                'marker': markers[marker_idx],
                'linestyle': '-',
                'linewidth': 2 if is_outlier else 1.5,
                'markersize': 8 if is_outlier else 6,
                'alpha': 0.8
            }
            
            if is_outlier:
                line_props['color'] = 'red'
                line_props['markeredgecolor'] = 'red'
                line_props['markeredgewidth'] = 2
            else:
                line_props['color'] = colors[color_idx]
            
            # Plot the data
            line, = ax.plot(data['days'], data['wear_values'], **line_props, label=data['asset_id'])
            
            # Add annotation for outliers
            if is_outlier:
                ax.annotate(f"Outlier: {data['asset_id']}", 
                           xy=(data['days'][-1], data['wear_values'][-1]),
                           xytext=(10, 0), textcoords="offset points",
                           ha="left", va="center", fontsize=9,
                           bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.7))
        
        # Invert Y-axis if requested to show wear increasing downward
        if self.invert_y_var.get():
            ax.invert_yaxis()
        
        # Set chart properties
        ax.set_title(title)
        ax.set_xlabel("Days Since First Measurement")
        ax.set_ylabel("Wear (mm)")
        ax.grid(True, alpha=0.3)
        
        # Add legend
        if len(processed_data) <= 10:
            ax.legend(loc='best')
        else:
            # For many assets, move legend outside the plot
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            fig.subplots_adjust(right=0.8)
        
        # Create canvas for displaying the plot
        canvas = FigureCanvasTkAgg(fig, master=self.graph_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Save reference to canvas for export
        self.canvas = canvas
        self.fig = fig
        
        # Update status
        self.status_var.set(f"Comparison generated with {len(processed_data)} assets")
        
    def export_graph(self):
        """Export the current graph as an image file."""
        if not hasattr(self, 'fig') or not self.fig:
            messagebox.showinfo("Export Error", "No graph available to export. Please generate a comparison first.")
            return
            
        try:
            # TODO: Add file dialog to choose save location
            filename = "tul_comparison.png"
            self.fig.savefig(filename, dpi=300, bbox_inches='tight')
            messagebox.showinfo("Export Successful", f"Graph exported to {filename}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export graph: {str(e)}")