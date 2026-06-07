import numpy as np

# 传感器参数 [R0 (kOhm), L0 (mm), GF, Rcp (kOhm)]
sensors = {
    'A': {'R0': 2.0, 'L0': 50, 'GF': 2.4, 'Rcp': 0.1},
    'B': {'R0': 3.5, 'L0': 40, 'GF': 1.6, 'Rcp': 0.1},
    'C': {'R0': 3.0, 'L0': 40, 'GF': 0.6, 'Rcp': 0.2}
}

# 电路参数
dL_target = 10.0  # 目标伸长量 (mm)
Vin = 5.0         # 输入电压 (V)
Rk = 10.0         # 分压电阻 (kOhm)

print(f"{'Sensor':<8} | {'Rm (kOhm)':<10} | {'Vout (V)':<10} | {'M (0-31)':<10} | {'Sensitivity':<12}")
print("-" * 60)

best_sensor = None
max_sensitivity = -1

for name, params in sensors.items():
    R0 = params['R0']
    L0 = params['L0']
    GF = params['GF']
    Rcp = params['Rcp']

    # 1. 计算 10mm 处的实际电阻 Rm
    # 理想电阻 + 接触电阻
    R_ideal = R0 * (1 + GF * (dL_target / L0))
    Rm = R_ideal + 2 * Rcp

    # 2. 计算分压输出 Vout
    Vout = (Rk / (Rk + Rm)) * Vin

    # 3. 计算量化值 M
    M = round(31 * Vout / Vin)

    # 4. 计算灵敏度 S = |dM/dL|
    # 链式法则: dM/dL = (dM/dVout) * (dVout/dRm) * (dRm/dL)
    
    # dRm/dL = R0 * GF / L0
    dRm_dL = R0 * GF / L0
    
    # dVout/dRm = - Vin * Rk / (Rk + Rm)^2
    dVout_dRm = - Vin * Rk / ((Rk + Rm)**2)
    
    # dM/dVout = 31 / Vin (近似)
    dM_dVout = 31 / Vin
    
    # 总灵敏度 (绝对值)
    Sensitivity = abs(dM_dVout * dVout_dRm * dRm_dL)
    
    print(f"{name:<8} | {Rm:<10.4f} | {Vout:<10.4f} | {M:<10} | {Sensitivity:<12.4f}")

    if Sensitivity > max_sensitivity:
        max_sensitivity = Sensitivity
        best_sensor = name

print("-" * 60)
print(f"结论: Sensor {best_sensor} 最准确 (灵敏度最高)。")