import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

V_data = np.array([0.0, 3.9, 9.8, 17.1, 22.3, 25.0, 26.7, 27.4, 27.6])

t_data = np.array([0.300, 0.298, 0.295, 0.276, 0.253, 0.225, 0.184, 0.149, 0.053])

t0 = 0.300

def thickness_model(V, K):
    """
    DEA thickness model:
        t(V) = t0 * (1 - K * V^2)^(1/6)
    V in kV, K in kV^{-2}, t in mm.
    """
    inside = 1.0 - K * V**2
    inside = np.clip(inside, 1e-12, None)
    return t0 * inside**(1.0 / 6.0)

K0 = 1.0e-3

popt, pcov = curve_fit(thickness_model, V_data, t_data, p0=[K0])
K_fit = popt[0]
print(f"Best-fit K = {K_fit:.5f} kV^(-2)")

V_plot = np.linspace(-30.0, 30.0, 400)  # kV
t_plot = thickness_model(V_plot, K_fit)

# plot

plt.figure(figsize=(6, 4))

plt.plot(V_plot, t_plot, label=rf"Model: $K = {K_fit:.4f}\,\mathrm{{kV^{{-2}}}}$")

plt.scatter(V_data, t_data, color="red", label="Experimental data")

plt.xlabel(r"Voltage $V$ (kV)")
plt.ylabel(r"Thickness $t$ (mm)")
plt.title("DEA thickness–voltage behaviour")
plt.xlim(-30, 30)
plt.grid(True, linestyle="--", alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig("dea_thickness_voltage.png", dpi=300)
plt.show()
