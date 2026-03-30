import Variables_Lateral as lv
import numpy as np
import matplotlib.pyplot as plt

# ============================================
# 1. Turning Radius vs Steering Angle
# ============================================

plt.figure(figsize=(9, 6))
plt.plot(lv.steering_deg, lv.turn_radius, linewidth=2)
plt.xlabel("Steering Angle (deg)")
plt.ylabel("Turning Radius (m)")
plt.title("Turning Radius vs Steering Angle")
plt.grid(True)
plt.show()


# ============================================
# 2. Ackermann Inside / Outside Wheel Angles
# ============================================

plt.figure(figsize=(9, 6))
plt.plot(lv.turn_radius, lv.SAI_deg, linewidth=2, label="Inside Wheel Angle")
plt.plot(lv.turn_radius, lv.SAO_deg, linewidth=2, label="Outside Wheel Angle")
plt.xlabel("Turning Radius (m)")
plt.ylabel("Steering Angle (deg)")
plt.title("Ackermann Steering Angles vs Turning Radius")
plt.grid(True)
plt.legend()
plt.show()


# ============================================
# 3. Lateral Acceleration vs Speed
#    for selected steering angles
# ============================================

selected_angles = [5, 10, 15, 20, 25]

plt.figure(figsize=(9, 6))

for angle_deg in selected_angles:
    angle_rad = np.radians(angle_deg)
    R = lv.wheelbase / np.tan(angle_rad)
    a_lat = (lv.Vspeed ** 2) / R
    plt.plot(lv.Vspeed, a_lat, linewidth=2, label=f"{angle_deg} deg")

plt.axhline(lv.mu * lv.g, color="red", linestyle="--", linewidth=2, label="Grip Limit")
plt.xlabel("Vehicle Speed (m/s)")
plt.ylabel("Lateral Acceleration (m/s²)")
plt.title("Lateral Acceleration vs Speed")
plt.grid(True)
plt.legend()
plt.show()


# ============================================
# 4. Max Safe Speed vs Steering Angle
# ============================================

plt.figure(figsize=(9, 6))
plt.plot(lv.steering_deg, lv.Vsafe, linewidth=2)
plt.xlabel("Steering Angle (deg)")
plt.ylabel("Max Safe Speed (m/s)")
plt.title("Max Safe Speed vs Steering Angle")
plt.grid(True)
plt.show()