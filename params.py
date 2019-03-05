"""
ME 112, Project 2
R Cohen, Feb 2019

Key parameters for jumping robot dynamic analysis.
"""

# Battery
V_b = 4.2  # [V] battery voltage

# Motor
R_m = 2.1  # [ohms] motor coil resistance
k_m = 0.0021  # motor torque constant
T_fric = 0.00099 # motor friction torque

# Gearbox
# N = 29.8  # gear ratio
eta_g = 0.803  # estimated gearbox efficiency, from gears lab

# Geometry
r_shaft = 0.002  # [m] spooling shaft radius
l = 0.109  # [m] leg length

# Assorted
t = 8.0  # [s] loading time