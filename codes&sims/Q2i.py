import numpy as np
import matplotlib.pyplot as plt

# Data from Figure 2 [cite: 2086]
# Format: [R0 (kOhm), L0 (mm), GF, Rcp (kOhm)]
sensors = {
    'A': {'R0': 2.0, 'L0': 50, 'GF': 2.4, 'Rcp': 0.1},
    'B': {'R0': 3.5, 'L0': 40, 'GF': 1.6, 'Rcp': 0.1},
    'C': {'R0': 3.0, 'L0': 40, 'GF': 0.6, 'Rcp': 0.2}
}

dL = np.linspace(0, 20, 100)  # Delta L from 0 to 20mm

plt.figure(figsize=(10, 6))

for name, params in sensors.items():
    R0 = params['R0']
    L0 = params['L0']
    GF = params['GF']
    Rcp = params['Rcp']
    
    # 1. Ideal Resistance (R_cp = 0)
    R_ideal = R0 * (1 + GF * (dL / L0))
    
    # 2. Measured Resistance (Real case)
    R_measured = R_ideal + 2 * Rcp
    
    # Plotting
    plt.plot(dL, R_ideal, linestyle='--', label=f'Sensor {name} (Ideal)')
    plt.plot(dL, R_measured, linestyle='-', label=f'Sensor {name} (Measured)')
    
    # 3. Calculate Prediction Error
    # Error formula derived: Error = (2 * Rcp * L0) / (R0 * GF)
    error_val = (2 * Rcp * L0) / (R0 * GF)
    print(f"Sensor {name} Prediction Error: {error_val:.4f} mm")

plt.xlabel('Extension $\Delta L$ (mm)')
plt.ylabel('Resistance ($k\Omega$)')
plt.title('Resistance vs. Extension for Soft Sensors')
plt.grid(True, alpha=0.5)
plt.legend()
plt.savefig('sensor_resistance_plot.png', dpi=300)
plt.show()