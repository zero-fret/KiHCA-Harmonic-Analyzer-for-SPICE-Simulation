import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ========== GLOBAL FONT SETTINGS ==========
GUI_FONT_SIZE = 20     
CHART_FONT_SIZE = 20    

# Global font size
plt.rcParams['font.size'] = CHART_FONT_SIZE
plt.rcParams['axes.labelsize'] = CHART_FONT_SIZE
plt.rcParams['axes.titlesize'] = CHART_FONT_SIZE + 2
plt.rcParams['xtick.labelsize'] = CHART_FONT_SIZE - 1
plt.rcParams['ytick.labelsize'] = CHART_FONT_SIZE - 1
plt.rcParams['legend.fontsize'] = CHART_FONT_SIZE - 1


TITLE_FONT_SIZE = GUI_FONT_SIZE + 2
HEADING_FONT_SIZE = GUI_FONT_SIZE + 1
NORMAL_FONT_SIZE = GUI_FONT_SIZE
SMALL_FONT_SIZE = GUI_FONT_SIZE - 1

class HarmonicAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Harmonic Analysis Software")
        self.root.geometry("950x750")
        
        # Apply global fonts for GUI
        self.configure_fonts()

        # Data storage
        self.time = None
        self.signals = {}          # column name -> data array
        self.variable_names = []   # signal column names (excluding time)
        self.current_var = None
        self.f0 = None

        # Create interface
        self.create_widgets()

    def configure_fonts(self):

        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=GUI_FONT_SIZE)
        
 
        text_font = font.nametofont("TkTextFont")
        text_font.configure(size=GUI_FONT_SIZE)
        
 
        self.title_font = ('Segoe UI', TITLE_FONT_SIZE, 'bold')
        self.heading_font = ('Segoe UI', HEADING_FONT_SIZE, 'bold')
        self.normal_font = ('Segoe UI', NORMAL_FONT_SIZE)
        self.small_font = ('Segoe UI', SMALL_FONT_SIZE)
        self.mono_font = ('Consolas', NORMAL_FONT_SIZE) 

    def create_widgets(self):
        # File selection area
        file_frame = ttk.LabelFrame(self.root, text="Data File", padding=5)
        file_frame.pack(fill=tk.X, padx=10, pady=5)

        self.configure_labelframe_font(file_frame)

        self.file_path = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path, width=70)
        file_entry.pack(side=tk.LEFT, padx=5)
        
        browse_btn = ttk.Button(file_frame, text="Browse", command=self.select_file)
        browse_btn.pack(side=tk.LEFT, padx=5)
        
        load_btn = ttk.Button(file_frame, text="Load Data", command=self.load_data)
        load_btn.pack(side=tk.LEFT, padx=5)

        # Parameter setting area
        param_frame = ttk.LabelFrame(self.root, text="Analysis Parameters", padding=5)
        param_frame.pack(fill=tk.X, padx=10, pady=5)
        self.configure_labelframe_font(param_frame)

        f0_label = ttk.Label(param_frame, text="Fundamental Frequency (Hz):", font=self.normal_font)
        f0_label.pack(side=tk.LEFT, padx=5)
        
        self.f0_entry = ttk.Entry(param_frame, width=10, font=self.normal_font)
        self.f0_entry.pack(side=tk.LEFT, padx=5)
        self.f0_entry.insert(0, "50.0")

        harmonic_label = ttk.Label(param_frame, text="Max Harmonic Order:", font=self.normal_font)
        harmonic_label.pack(side=tk.LEFT, padx=(20,5))
        
        self.max_harmonic = ttk.Entry(param_frame, width=5, font=self.normal_font)
        self.max_harmonic.pack(side=tk.LEFT, padx=5)
        self.max_harmonic.insert(0, "20")

        # Variable selection area
        var_frame = ttk.LabelFrame(self.root, text="Select Signal", padding=5)
        var_frame.pack(fill=tk.X, padx=10, pady=5)
        self.configure_labelframe_font(var_frame)

        self.var_combo = ttk.Combobox(var_frame, state="readonly", width=30, font=self.normal_font)
        self.var_combo.pack(side=tk.LEFT, padx=5)
        
        analyze_btn = ttk.Button(var_frame, text="Analyze & Plot", command=self.analyze_and_plot)
        analyze_btn.pack(side=tk.LEFT, padx=5)

        # Results display area
        result_frame = ttk.LabelFrame(self.root, text="Analysis Results", padding=5)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.configure_labelframe_font(result_frame)

        self.result_text = tk.Text(result_frame, wrap=tk.WORD, height=12, 
                                   font=self.mono_font, bg='#f5f5f5')
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Plot area
        plot_frame = ttk.LabelFrame(self.root, text="Harmonic Spectrum (dB Scale)", padding=5)
        plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.configure_labelframe_font(plot_frame)

        self.fig, self.ax = plt.subplots(figsize=(9, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def configure_labelframe_font(self, frame):
        style = ttk.Style()
        style.configure("TLabelframe.Label", font=self.heading_font)


    def select_file(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if filename:
            self.file_path.set(filename)

    def load_data(self):
        """Read CSV file (semicolon separated), first row contains variable names"""
        path = self.file_path.get()
        if not path:
            messagebox.showerror("Error", "Please select a file first")
            return

        try:
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=';')
                header = next(reader)
                # Clean column names: remove whitespace and empty strings
                col_names = [name.strip() for name in header if name.strip() != '']
                if not col_names:
                    raise ValueError("No valid column names in CSV header")

                # Read data rows
                data_rows = []
                for row in reader:
                    if not row:
                        continue
                    clean_row = [val.strip() for val in row if val.strip() != '']
                    if len(clean_row) < len(col_names):
                        continue
                    clean_row = clean_row[:len(col_names)]
                    data_rows.append(clean_row)

                if not data_rows:
                    raise ValueError("No valid data rows in file")

                # Convert to float
                data = np.array(data_rows, dtype=float)

                # Build signal dictionary
                self.signals = {}
                for i, name in enumerate(col_names):
                    self.signals[name] = data[:, i]

                # Identify time column
                time_col = None
                for name in col_names:
                    if name.lower() == 'time':
                        time_col = name
                        break
                if time_col is None:
                    time_col = col_names[0]
                    print(f"Column '{time_col}' used as time column")

                self.time = self.signals[time_col]
                self.variable_names = [name for name in col_names if name != time_col]

                # Update dropdown menu
                self.var_combo['values'] = self.variable_names
                if self.variable_names:
                    self.var_combo.current(0)
                    self.current_var = self.variable_names[0]

                messagebox.showinfo("Success", 
                    f"Data loaded!\nTime range: {self.time[0]:.4f} ~ {self.time[-1]:.4f} s\n"
                    f"Signals: {', '.join(self.variable_names)}")

        except Exception as e:
            messagebox.showerror("Load Error", str(e))

    def harmonic_fit(self, t, y, f0, max_harmonic):
        """
        Least squares fit for DC + harmonics 1..max_harmonic with known fundamental frequency f0.
        Returns:
            harmonics_amp: array length max_harmonic+1, index 0 = DC amplitude, index k = peak amplitude of k-th harmonic
            harmonics_phase: phase in radians
        """
        N = len(t)
        # Construct matrix M: columns for [1, cos(2πf0 t), sin(2πf0 t), cos(4πf0 t), sin(4πf0 t), ...]
        M = np.ones((N, 1))  # DC component
        for k in range(1, max_harmonic+1):
            omega = 2 * np.pi * k * f0
            M = np.column_stack((M, np.cos(omega * t), np.sin(omega * t)))

        # Solve coefficients
        try:
            coeffs, _, _, _ = np.linalg.lstsq(M, y, rcond=None)
        except np.linalg.LinAlgError:
            raise RuntimeError("Singular matrix in least squares. Check data or fundamental frequency.")

        # Parse coefficients
        dc = coeffs[0]
        harmonics_amp = np.zeros(max_harmonic+1)
        harmonics_phase = np.zeros(max_harmonic+1)
        harmonics_amp[0] = dc

        idx = 1
        for k in range(1, max_harmonic+1):
            cos_coef = coeffs[idx]
            sin_coef = coeffs[idx+1]
            amp = np.sqrt(cos_coef**2 + sin_coef**2)
            phase = np.arctan2(sin_coef, cos_coef)
            harmonics_amp[k] = amp
            harmonics_phase[k] = phase
            idx += 2

        return harmonics_amp, harmonics_phase

    def compute_metrics(self, amps, fundamental_amp):
        """Calculate relative dB values, THD, and total RMS"""
        max_harmonic = len(amps)-1
        if fundamental_amp <= 1e-12:
            raise ValueError("Fundamental amplitude too small for relative calculations")

        # Relative dB values: 20*log10(amp_k / amp_fund)
        rel_db = np.zeros(max_harmonic+1)
        rel_db[0] = 20 * np.log10(np.abs(amps[0]) / fundamental_amp + 1e-12)
        for k in range(1, max_harmonic+1):
            rel_db[k] = 20 * np.log10(amps[k] / fundamental_amp + 1e-12)

        # Total Harmonic Distortion (THD)
        harmonic_power_sum = np.sum(amps[2:]**2)
        thd = np.sqrt(harmonic_power_sum) / fundamental_amp
        thd_db = 20 * np.log10(thd + 1e-12)

        # Total RMS (equivalent amplitude)
        rms_dc = np.abs(amps[0])
        rms_fund = fundamental_amp / np.sqrt(2)
        rms_harmonics = np.sqrt(np.sum((amps[2:]**2) / 2))
        total_rms = np.sqrt(rms_dc**2 + rms_fund**2 + rms_harmonics**2)

        return rel_db, thd, thd_db, total_rms

    def analyze_and_plot(self):
        """Main analysis: get parameters, fit, display results, and plot dB spectrum with points"""
        if self.time is None or not self.signals:
            messagebox.showerror("Error", "Please load data file first")
            return

        # Get fundamental frequency
        try:
            f0 = float(self.f0_entry.get())
            if f0 <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Fundamental frequency must be a positive number")
            return

        # Get max harmonic order
        try:
            max_harmonic = int(self.max_harmonic.get())
            if max_harmonic < 1:
                max_harmonic = 1
        except:
            max_harmonic = 20

        # Get selected variable
        selected_var = self.var_combo.get()
        if not selected_var:
            messagebox.showerror("Error", "Please select a signal to analyze")
            return
        y = self.signals[selected_var]

        t = self.time
        # Remove NaN or Inf
        mask = np.isfinite(t) & np.isfinite(y)
        t = t[mask]
        y = y[mask]
        if len(t) < 2:
            messagebox.showerror("Error", "Insufficient valid data points")
            return

        # Fit harmonics
        try:
            amps, phases = self.harmonic_fit(t, y, f0, max_harmonic)
        except Exception as e:
            messagebox.showerror("Fit Failed", str(e))
            return

        fundamental_amp = amps[1]
        # Calculate metrics
        try:
            rel_db, thd, thd_db, total_rms = self.compute_metrics(amps, fundamental_amp)
        except Exception as e:
            messagebox.showerror("Calculation Error", str(e))
            return

        # Build result text
        result_str = f"Signal: {selected_var}\n"
        result_str += f"Fundamental Frequency: {f0} Hz\n"
        result_str += f"Fundamental Amplitude (peak): {fundamental_amp:.6f}\n"
        result_str += f"DC Component: {amps[0]:.6f}\n"
        result_str += "-" * 85 + "\n"
        result_str += f"{'Order':<8}{'Amplitude(peak)':<20}{'Relative to Fundamental (dB)':<28}{'Phase (rad)':<12}\n"
        result_str += "-" * 85 + "\n"
        for k in range(1, max_harmonic+1):
            result_str += f"{k:<8}{amps[k]:<20.6e}{rel_db[k]:<28.2f}{phases[k]:<12.4f}\n"

        result_str += "-" * 85 + "\n"
        result_str += f"Total Harmonic Distortion (THD): {thd*100:.4f}%  (linear: {thd:.6f})\n"
        result_str += f"THD in dB: {thd_db:.2f} dB\n"
        result_str += f"Total RMS (equivalent amplitude): {total_rms:.6f}\n"
        result_str += f"DC relative to fundamental: {rel_db[0]:.2f} dB\n"

        # Display results
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_str)

        # Plot dB spectrum with points (not bars)
        self.ax.clear()
        harmonics = np.arange(1, max_harmonic+1)
        rel_db_values = rel_db[1:]  # exclude DC for main plot
        
        # Create point plot with markers
        self.ax.plot(harmonics, rel_db_values, 'o-', color='steelblue', 
                    markersize=8, markerfacecolor='steelblue', 
                    markeredgecolor='navy', markeredgewidth=1.5,
                    linewidth=1.5, alpha=0.8, label='Harmonics')
        
        # Add value labels on top of points (except very low values)
        label_fontsize = max(8, CHART_FONT_SIZE - 2)
        for i, (harmonic, db_val) in enumerate(zip(harmonics, rel_db_values)):
            if db_val > -100:  # Only label points that are not too low
                # Offset label position based on dB value
                y_offset = 3 if db_val >= 0 else -5
                self.ax.text(harmonic, db_val + y_offset, 
                           f'{db_val:.1f}', ha='center', va='bottom' if db_val >= 0 else 'top', 
                           fontsize=label_fontsize, color='darkblue', fontweight='bold')
        
        # Set axis labels and title
        self.ax.set_xlabel("Harmonic Order", fontsize=CHART_FONT_SIZE, fontweight='bold')
        self.ax.set_ylabel("Relative Amplitude (dB)", fontsize=CHART_FONT_SIZE, fontweight='bold')
        self.ax.set_title(f"Harmonic Spectrum - {selected_var} (f0 = {f0} Hz, 0 dB = Fundamental)", 
                         fontsize=CHART_FONT_SIZE + 2, fontweight='bold')
        
        # Set y-axis limits with some margin
        y_min = min(-60, np.min(rel_db_values) - 10)
        y_max = max(5, np.max(rel_db_values) + 10)
        self.ax.set_ylim(y_min, y_max)
        
        # Set x-axis limits with some padding
        self.ax.set_xlim(0.5, max_harmonic + 0.5)
        
        # Add grid
        self.ax.grid(True, linestyle='--', alpha=0.3, axis='both')
        self.ax.set_axisbelow(True)
        
        # Set x-ticks for all harmonics
        self.ax.set_xticks(harmonics)
        self.ax.set_xticklabels([str(k) for k in harmonics], fontsize=CHART_FONT_SIZE - 2)
        
        # Add horizontal line at 0 dB
        self.ax.axhline(y=0, color='red', linestyle='-', linewidth=1.5, alpha=0.7, label='0 dB (Fundamental)')
        
        # Add legend
        self.ax.legend(loc='lower right', framealpha=0.9, fontsize=CHART_FONT_SIZE - 2)
        
        # Add light vertical lines at each harmonic for better readability
        for harmonic in harmonics:
            self.ax.axvline(x=harmonic, color='gray', linestyle=':', linewidth=0.5, alpha=0.3)
        
        # Adjust layout
        self.fig.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = HarmonicAnalyzer(root)
    root.mainloop()
