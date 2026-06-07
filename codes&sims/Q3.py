import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# Q3 (i) Acceptance Angle Calculation
# ==========================================

n1 = 1.49  # PMMA fibre core RI
n2_range = np.linspace(1.0, 1.5, 500)

alpha_deg = []
for n2 in n2_range:
    if n2 < n1:
        val = np.sqrt(n1**2 - n2**2)
        # enforce physical saturation limit
        val = min(val, 1.0)
        angle = np.degrees(np.arcsin(val))
    else:
        angle = 0
    alpha_deg.append(angle)

alpha_deg = np.array(alpha_deg)

# reference materials
ref_materials = {
    "Air": 1.00,
    "Silicone Rubber": 1.42,
    "Fused Silica": 1.46,
}

plt.figure(figsize=(10, 6))
plt.plot(n2_range, alpha_deg, label=r'Acceptance Angle $\alpha$', 
         color='blue', linewidth=2)

for name, n_val in ref_materials.items():
    if n_val < n1:
        # compute correct saturated angle
        val = min(np.sqrt(n1**2 - n_val**2), 1.0)
        a_val = np.degrees(np.arcsin(val))
        plt.scatter(n_val, a_val, color='red')
        plt.text(n_val, a_val + 5,
                 f"{name}\n(n={n_val})\n{a_val:.1f}$^\circ$",
                 ha='center', color='darkred')
    else:
        plt.scatter(n_val, 0, color='gray')
        plt.text(n_val, 5, f"{name}\n(n={n_val})\nNo TIR",
                 ha='center', color='gray')

plt.axhline(30, color='green', linestyle=':', 
            label='Light Source Angle (30$^\circ$)')
plt.axvline(n1, color='gray', linestyle='--', 
            label='Fibre Core RI (1.49)')

plt.title(r'Q3: Acceptance Angle $\alpha$ vs. Surrounding Medium RI $n_2$')
plt.xlabel(r'Refractive Index of Surrounding Medium ($n_2$)')
plt.ylabel(r'Acceptance Angle $\alpha$ (degrees)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.xlim(1.0, 1.52)
plt.ylim(0, 90)

plt.savefig("Q3_fiber_acceptance_angle.jpg", dpi=300)
plt.show()

# ==========================================
# Q3 (ii) Threshold Calculation
# ==========================================

target_angle = 30 # degrees
sin_alpha = np.sin(np.radians(target_angle))
n2_critical = np.sqrt(n1**2 - sin_alpha**2)

print("Critical refractive-index threshold:", n2_critical)
