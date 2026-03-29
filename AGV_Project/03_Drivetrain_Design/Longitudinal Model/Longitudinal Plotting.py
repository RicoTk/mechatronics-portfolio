import Variables as vp
import numpy as np
import math as m
import matplotlib.pyplot as plt

g = 9.81

# ============================================
# CORE MODEL FUNCTION
# Uses motor speed as the independent variable
# Current is computed from required motor load
# ============================================

def compute_load_based_model(motor_w_rpm, grade_percent, G, accel=0.0):
    angle = m.atan(grade_percent / 100.0)

    # Vehicle speed derived from motor speed
    motor_w_rad = motor_w_rpm * (2 * np.pi / 60.0)   # rad/s
    wheel_w_rad = motor_w_rad / G                    # rad/s
    Vspeed = wheel_w_rad * vp.wheel_R                # m/s

    # Available motor torque from torque-speed relation
    T_motor_available = vp.Tstall * (1 - motor_w_rpm / vp.w_noLoad)
    T_motor_available = np.maximum(T_motor_available, 0)

    # Available tractive force
    F_tractive_available = (2 * vp.motor_eff * T_motor_available * G) / vp.wheel_R

    # Resistive forces
    F_grade = vp.WV * np.sin(angle)
    F_normal = vp.WV * np.cos(angle)

    F_rolling = vp.Crr * F_normal
    F_drag = 0.5 * vp.Air_density * vp.drag_Coeff * vp.SAV * (Vspeed ** 2)
    F_resist = F_grade + F_rolling + F_drag

    # Net force using available tractive force
    Fnet_available = F_tractive_available - F_resist

    # Acceleration using available tractive force
    mass = vp.WV / g
    accel_available = Fnet_available / mass

    # ============================================
    # Load-based required torque/current
    # ============================================

    # Total longitudinal force demand
    # For steady-state accel=0, this is just the road load
    F_required = F_resist + mass * accel

    # Wheel torque required per motor (2 driven rear wheels / 2 motors)
    T_wheel_required_per_motor = (F_required * vp.wheel_R) / 2.0

    # Required motor torque per motor
    T_motor_required = T_wheel_required_per_motor / (G * vp.motor_eff)

    # Required current per motor
    current_required_per_motor = T_motor_required / vp.motorTconst
    current_required_total = 2 * current_required_per_motor

    # Available current from available torque-speed curve
    current_available_per_motor = T_motor_available / vp.motorTconst
    current_available_total = 2 * current_available_per_motor

    feasible = T_motor_required <= T_motor_available
    torque_margin = T_motor_available - T_motor_required

    return {
        "Vspeed": Vspeed,
        "T_motor_available": T_motor_available,
        "T_motor_required": T_motor_required,
        "F_tractive": F_tractive_available,
        "F_resist": F_resist,
        "Fnet": Fnet_available,
        "accel": accel_available,
        "current_required_per_motor": current_required_per_motor,
        "current_required_total": current_required_total,
        "current_available_per_motor": current_available_per_motor,
        "current_available_total": current_available_total,
        "F_drag": F_drag,
        "F_rolling": F_rolling,
        "F_grade": F_grade,
        "F_required": F_required,
        "feasible": feasible,
        "torque_margin": torque_margin
    }


# ============================================
# SETTINGS
# ============================================

grades = [0, 2, 5, 8, 10]
rated_current = 5.40   # A per motor
motor_w = vp.motor_w
G_nominal = vp.G


# ============================================
# 1. RESISTIVE + TRACTIVE FORCE vs SPEED
# ============================================

plt.figure(figsize=(9, 6))

for grade in grades:
    result = compute_load_based_model(motor_w, grade, G_nominal)
    plt.plot(result["Vspeed"], result["F_resist"], linewidth=2, label=f"Resistive {grade}%")

result0 = compute_load_based_model(motor_w, grades[0], G_nominal)
plt.plot(result0["Vspeed"], result0["F_tractive"], "k--", linewidth=2.5, label="Tractive Force")

plt.xlabel("Vehicle Speed (m/s)")
plt.ylabel("Force (N)")
plt.title("Resistive vs Tractive Force for Different Grades")
plt.grid(True)
plt.legend()
plt.show()


# ============================================
# 2. NET FORCE + TRACTIVE FORCE vs SPEED
# ============================================

plt.figure(figsize=(9, 6))

for grade in grades:
    result = compute_load_based_model(motor_w, grade, G_nominal)
    plt.plot(result["Vspeed"], result["Fnet"], linewidth=2, label=f"Net {grade}%")

plt.plot(result0["Vspeed"], result0["F_tractive"], "k--", linewidth=2.5, label="Tractive Force")
plt.axhline(0, linestyle="--", linewidth=1)

plt.xlabel("Vehicle Speed (m/s)")
plt.ylabel("Force (N)")
plt.title("Net Force vs Vehicle Speed for Different Grades")
plt.grid(True)
plt.legend()
plt.show()


# ============================================
# 3. ACCELERATION vs SPEED for several grades
# ============================================

plt.figure(figsize=(9, 6))

for grade in grades:
    result = compute_load_based_model(motor_w, grade, G_nominal)
    plt.plot(result["Vspeed"], result["accel"], linewidth=2, label=f"{grade}% grade")

plt.axhline(0, linestyle="--", linewidth=1)
plt.xlabel("Vehicle Speed (m/s)")
plt.ylabel("Acceleration (m/s²)")
plt.title("Acceleration vs Vehicle Speed for Different Grades")
plt.grid(True)
plt.legend()
plt.show()


# ============================================
# 4. SPEED vs TIME for several grades
# Uses available force model
# ============================================

plt.figure(figsize=(9, 6))

dt = 0.05
t_end = 10.0
time = np.arange(0, t_end, dt)

for grade in grades:
    result = compute_load_based_model(motor_w, grade, G_nominal)

    V_lookup = result["Vspeed"]
    Fnet_lookup = result["Fnet"]

    v = 0.0
    v_hist = []

    for t in time:
        v_clamped = np.clip(v, V_lookup.min(), V_lookup.max())
        Fnet_now = np.interp(v_clamped, V_lookup, Fnet_lookup)
        a_now = Fnet_now / (vp.WV / g)

        v = max(v + a_now * dt, 0.0)
        v_hist.append(v)

    plt.plot(time, v_hist, linewidth=2, label=f"{grade}% grade")

plt.xlabel("Time (s)")
plt.ylabel("Vehicle Speed (m/s)")
plt.title("Vehicle Speed vs Time for Different Grades")
plt.grid(True)
plt.legend()
plt.show()


# ============================================
# 5. TOP SPEED vs GRADE
# ============================================

top_speeds = []

for grade in grades:
    result = compute_load_based_model(motor_w, grade, G_nominal)
    idx = np.argmin(np.abs(result["Fnet"]))
    top_speeds.append(result["Vspeed"][idx])

plt.figure(figsize=(9, 6))
plt.plot(grades, top_speeds, marker="o", linewidth=2)
plt.xlabel("Grade (%)")
plt.ylabel("Top Speed (m/s)")
plt.title("Top Speed vs Grade")
plt.grid(True)
plt.show()


# ============================================
# 6. TOP SPEED vs GEAR RATIO
# ============================================

gear_ratios = np.arange(1, 7, 0.5)
top_speeds_G = []

for G in gear_ratios:
    result = compute_load_based_model(motor_w, 0, G)
    idx = np.argmin(np.abs(result["Fnet"]))
    top_speeds_G.append(result["Vspeed"][idx])

plt.figure(figsize=(9, 6))
plt.plot(gear_ratios, top_speeds_G, marker="o", linewidth=2)
plt.xlabel("Gear Ratio")
plt.ylabel("Top Speed (m/s)")
plt.title("Top Speed vs Gear Ratio (0% Grade)")
plt.grid(True)
plt.show()


# ============================================
# 7. REQUIRED vs AVAILABLE CURRENT vs SPEED
# ============================================

plt.figure(figsize=(9, 6))

for grade in grades:
    result = compute_load_based_model(motor_w, grade, G_nominal)
    plt.plot(
        result["Vspeed"],
        result["current_required_per_motor"],
        linewidth=2,
        label=f"Required {grade}%"
    )

plt.plot(
    result0["Vspeed"],
    result0["current_available_per_motor"],
    "k--",
    linewidth=2.5,
    label="Available Current"
)

plt.axhline(
    rated_current,
    color="red",
    linestyle="--",
    linewidth=2,
    label=f"Rated Current = {rated_current:.2f} A"
)

plt.xlabel("Vehicle Speed (m/s)")
plt.ylabel("Current per Motor (A)")
plt.title("Required vs Available Motor Current")
plt.grid(True)
plt.legend()
plt.show()


# ============================================
# 8. LOAD-BASED CURRENT vs TIME for several grades
# ============================================

plt.figure(figsize=(9, 6))

for grade in grades:
    result = compute_load_based_model(motor_w, grade, G_nominal)

    V_lookup = result["Vspeed"]
    Fnet_lookup = result["Fnet"]

    v = 0.0
    current_hist = []

    for t in time:
        v_clamped = np.clip(v, V_lookup.min(), V_lookup.max())

        # Use available force to update motion
        Fnet_now = np.interp(v_clamped, V_lookup, Fnet_lookup)
        a_now = Fnet_now / (vp.WV / g)

        # Recompute required current at the instantaneous speed and acceleration
        # Convert current vehicle speed back to motor speed
        wheel_w_now = v_clamped / vp.wheel_R
        motor_w_now_rad = wheel_w_now * G_nominal
        motor_w_now_rpm = motor_w_now_rad * (60 / (2 * np.pi))

        instant_result = compute_load_based_model(
            np.array([motor_w_now_rpm]),
            grade,
            G_nominal,
            accel=a_now
        )

        current_now = instant_result["current_required_per_motor"][0]

        v = max(v + a_now * dt, 0.0)
        current_hist.append(current_now)

    plt.plot(time, current_hist, linewidth=2, label=f"{grade}% grade")

plt.axhline(
    rated_current,
    color="red",
    linestyle="--",
    linewidth=2,
    label=f"Rated Current = {rated_current:.2f} A"
)

plt.xlabel("Time (s)")
plt.ylabel("Required Current per Motor (A)")
plt.title("Load-Based Motor Current vs Time for Different Grades")
plt.grid(True)
plt.legend()
plt.show()


# ============================================
# 9. OPTIONAL: REQUIRED vs AVAILABLE TOTAL CURRENT
# ============================================

plt.figure(figsize=(9, 6))

for grade in grades:
    result = compute_load_based_model(motor_w, grade, G_nominal)
    plt.plot(
        result["Vspeed"],
        result["current_required_total"],
        linewidth=2,
        label=f"Required Total {grade}%"
    )

plt.plot(
    result0["Vspeed"],
    result0["current_available_total"],
    "k--",
    linewidth=2.5,
    label="Available Total Current"
)

plt.axhline(
    2 * rated_current,
    color="red",
    linestyle="--",
    linewidth=2,
    label=f"2-Motor Rated Total = {2 * rated_current:.2f} A"
)

plt.xlabel("Vehicle Speed (m/s)")
plt.ylabel("Total Current (A)")
plt.title("Required vs Available Total Motor Current")
plt.grid(True)
plt.legend()
plt.show()

# ============================================
# 10. GEAR RATIO STUDY:
#     steady-state current vs gear ratio
#     and top speed vs gear ratio
# ============================================

gear_ratios = np.arange(1.0, 8.5, 0.5)
grades_for_study = [0, 5, 10]

plt.figure(figsize=(9, 6))

for grade in grades_for_study:
    steady_currents = []

    for G in gear_ratios:
        result = compute_load_based_model(motor_w, grade, G)

        # steady-state point = where |Fnet| is minimum
        idx_ss = np.argmin(np.abs(result["Fnet"]))
        steady_currents.append(result["current_required_per_motor"][idx_ss])

    plt.plot(gear_ratios, steady_currents, marker="o", linewidth=2, label=f"{grade}% grade")

plt.axhline(
    rated_current,
    color="red",
    linestyle="--",
    linewidth=2,
    label=f"Rated Current = {rated_current:.2f} A"
)

plt.xlabel("Gear Ratio")
plt.ylabel("Steady-State Required Current per Motor (A)")
plt.title("Steady-State Current vs Gear Ratio")
plt.grid(True)
plt.legend()
plt.show()


# Top speed vs gear ratio for same grades
plt.figure(figsize=(9, 6))

for grade in grades_for_study:
    top_speeds = []

    for G in gear_ratios:
        result = compute_load_based_model(motor_w, grade, G)

        idx_ss = np.argmin(np.abs(result["Fnet"]))
        top_speeds.append(result["Vspeed"][idx_ss])

    plt.plot(gear_ratios, top_speeds, marker="o", linewidth=2, label=f"{grade}% grade")

plt.xlabel("Gear Ratio")
plt.ylabel("Top Speed (m/s)")
plt.title("Top Speed vs Gear Ratio")
plt.grid(True)
plt.legend()
plt.show()

# ============================================
# 11. STEADY-STATE OPERATING POINT SUMMARY
# ============================================

print("\nSTEADY-STATE OPERATING POINTS")
print("-" * 90)
print(f"{'Grade (%)':>10} | {'G':>4} | {'V_ss (m/s)':>10} | {'Motor RPM':>10} | {'I_req (A)':>10} | {'I_avail (A)':>12} | {'Fnet (N)':>10}")
print("-" * 90)

for grade in grades:
    result = compute_load_based_model(motor_w, grade, G_nominal)

    idx_ss = np.argmin(np.abs(result["Fnet"]))

    v_ss = result["Vspeed"][idx_ss]
    motor_rpm_ss = motor_w[idx_ss]
    i_req_ss = result["current_required_per_motor"][idx_ss]
    i_avail_ss = result["current_available_per_motor"][idx_ss]
    fnet_ss = result["Fnet"][idx_ss]

    print(f"{grade:10.1f} | {G_nominal:4.1f} | {v_ss:10.3f} | {motor_rpm_ss:10.1f} | {i_req_ss:10.3f} | {i_avail_ss:12.3f} | {fnet_ss:10.3f}")

print("-" * 90)


# ============================================
# 12. STEADY-STATE SUMMARY FOR MULTIPLE GEAR RATIOS
# ============================================

candidate_gears = [3, 4, 5, 6]
grades_for_summary = [0, 5, 10]

print("\nSTEADY-STATE SUMMARY FOR CANDIDATE GEAR RATIOS")
print("-" * 110)
print(f"{'Grade (%)':>10} | {'G':>4} | {'V_ss (m/s)':>10} | {'Motor RPM':>10} | {'I_req (A)':>10} | {'I_avail (A)':>12} | {'Feasible':>10}")
print("-" * 110)

for grade in grades_for_summary:
    for G in candidate_gears:
        result = compute_load_based_model(motor_w, grade, G)

        idx_ss = np.argmin(np.abs(result["Fnet"]))

        v_ss = result["Vspeed"][idx_ss]
        motor_rpm_ss = motor_w[idx_ss]
        i_req_ss = result["current_required_per_motor"][idx_ss]
        i_avail_ss = result["current_available_per_motor"][idx_ss]
        feasible_ss = result["feasible"][idx_ss]

        print(f"{grade:10.1f} | {G:4.1f} | {v_ss:10.3f} | {motor_rpm_ss:10.1f} | {i_req_ss:10.3f} | {i_avail_ss:12.3f} | {str(feasible_ss):>10}")

print("-" * 110)