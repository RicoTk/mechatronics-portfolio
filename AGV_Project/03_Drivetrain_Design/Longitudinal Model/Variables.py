import math as m
import numpy as np

# ============================================
# CONSTANTS
# ============================================

g = 9.81                         # m/s^2

# ============================================
# INPUT VARIABLES
# ============================================

# Vehicle / geometry
WV = 100                          # N, total vehicle weight
mass = WV / g                    # kg
wheelbase = 0.5                  # m
wheel_R = 0.075                  # m

# Terrain / operating condition
grade = 0                        # %, maximum expected 5 to 10
angle = m.atan(grade / 100)      # rad

# Motor / drivetrain
Tstall = 0.94                    # Nm, stall torque per motor
w_noLoad = 4400                  # RPM, no-load speed per motor
motor_w = np.arange(200, 3000, 200)   # RPM, motor speed sweep
motor_eff = 0.7                  # drivetrain/motor efficiency
motorTconst = 0.0555             # Nm/A, torque constant
G = 3                           # gear ratio

# Vehicle drag / rolling resistance
Crr = 0.1                        # rolling resistance coefficient
drag_Coeff = 0.5
SAV = 0.0625                       # m^2, frontal/surface area
Air_density = 1.225              # kg/m^3

# ============================================
# DERIVED MOTOR / SPEED VARIABLES
# ============================================

# Geared drive assumption:
# wheel speed = motor speed / G

motor_w_rad = motor_w * (2 * np.pi / (60 * G))     # rad/s
#Vspeed = motor_w_rad * wheel_R                   # m/s, vehicle speed array
Vspeed = np.arange(0.4, 6, 0.4)                 # m/s, vehicle speed array


# Linear motor torque-speed model
motor_T = Tstall * (1 - (motor_w / w_noLoad))   # Nm per motor
motor_T = np.maximum(motor_T, 0)                # prevent negative torque

# Current estimate
current_per_motor = motor_T / motorTconst       # A
current_total = 2 * current_per_motor           # A, two rear motors

# ============================================
# FORCE CALCULATIONS
# ============================================

# Weight components
Wx = WV * m.sin(angle)                     # x component of weight
Wy = WV * m.cos(angle)                     # y component of weight

# Rolling resistance
F_rolling = Crr * Wy                #rolling resistance force

# Aerodynamic drag (depends on vehicle speed)
F_drag = 0.5 * Air_density * drag_Coeff * SAV * (Vspeed ** 2)   #drag force

# Tractive force from 2 rear motors, direct drive
TractiveF = (2 * motor_eff * motor_T * G) / wheel_R             # N

# Total resistive force
F_resist = Wx + F_rolling + F_drag                     # N

# Net force
Fnet = TractiveF - F_resist                                 # N

# Vehicle acceleration
VA = Fnet / mass                                            # m/s^2

# ============================================
# OPTIONAL AXLE LOADS (STATIC, ON SLOPE)
# ============================================

# If you want rough static axle loads for a 45/55 distribution:
NormalFF = 0.45 * Wy     # N, front axle normal load
NormalFR = 0.55 * Wy     # N, rear axle normal load

# Rear traction limit estimate (optional, if you later include tire friction)
# mu = 0.6
# F_traction_limit = mu * NormalFR
