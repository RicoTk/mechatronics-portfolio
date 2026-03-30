import numpy as np
import math as m

# ============================================
# INPUT VARIABLES
# ============================================

# Vehicle properties
Vmass = 10.0              # kg
g = 9.81                  # m/s^2
wheelbase = 0.5           # m
trackwidth = 0.3          # m
Lf = 0.275                # m
Lr = 0.225                # m

# Terrain / tire assumption
mu = 0.6                  # friction coefficient
bankAngle = 0.0           # rad

# Steering input range
steering_deg = np.linspace(1, 30, 100)     # deg
steering_rad = np.radians(steering_deg)    # rad

# Vehicle speed range
Vspeed = np.linspace(0.1, 6.0, 100)        # m/s

# ============================================
# DERIVED VARIABLES
# ============================================

# Bicycle-model turning radius
turn_radius = wheelbase / np.tan(steering_rad)   # m

# Ackermann steering angles for each turn radius
# inside and outside front wheel angles
SAI_rad = np.arctan(wheelbase / (turn_radius - trackwidth / 2))   # rad
SAO_rad = np.arctan(wheelbase / (turn_radius + trackwidth / 2))   # rad

SAI_deg = np.degrees(SAI_rad)
SAO_deg = np.degrees(SAO_rad)

# Maximum safe speed based on lateral grip
# ay_max = mu * g
Vsafe = np.sqrt(mu * g * turn_radius)      # m/s