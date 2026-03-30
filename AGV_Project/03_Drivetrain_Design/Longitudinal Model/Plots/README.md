# 📊 Longitudinal Model – Plots Overview

This folder contains the key plots generated from the longitudinal vehicle model. These visualizations support drivetrain sizing, performance evaluation, and thermal feasibility analysis.

---

## 📁 Plot List

### 1. Force vs Speed

![Force vs Speed](https://github.com/RicoTk/mechatronics-portfolio/blob/main/AGV_Project/03_Drivetrain_Design/Longitudinal%20Model/Plots/force_vs_speed.png)

**Description:** 
- Shows tractive force, resistive force, and net force vs vehicle speed
- Used to determine:
  - Whether the vehicle can accelerate
  - Theoretical top speed (where net force = 0)

**Key Insight:**
- Confirms the vehicle is mechanically capable of overcoming resistive forces

---

### 2. Current vs Time

![Current vs Time](https://github.com/RicoTk/mechatronics-portfolio/blob/main/AGV_Project/03_Drivetrain_Design/Longitudinal%20Model/Plots/current_vs_time.png)

**Description:**
- Shows motor current during acceleration for multiple grades
- Includes rated current reference line

**Key Insight:**
- High current at launch (~stall region)
- System settles into steady-state current
- Used to evaluate transient vs continuous loading

---

### 3. Required vs Available Current

![Required vs Available Current](https://github.com/RicoTk/mechatronics-portfolio/blob/main/AGV_Project/03_Drivetrain_Design/Longitudinal%20Model/Plots/required_vs_available.png)

**Description:**
- Compares:
  - Required current (from vehicle load)
  - Available current (from motor torque-speed curve)
- Includes rated current limit

**Key Insight:**
- System is mechanically feasible (required < available)
- Thermal limits identified where required > rated current

---

### 4. Steady-State Current vs Gear Ratio

![Steady State Current vs Gear Ratio](https://github.com/RicoTk/mechatronics-portfolio/blob/main/AGV_Project/03_Drivetrain_Design/Longitudinal%20Model/Plots/gear_ratio_current.png)

**Description:**
- Shows how required steady-state current changes with gear ratio
- Evaluated for multiple grades (0%, 5%, 10%)

**Key Insight:**
- Increasing gear ratio reduces motor current
- Identifies minimum gear ratio required to stay within rated current

---

### 5. Top Speed vs Gear Ratio

![Top Speed vs Gear Ratio](https://github.com/RicoTk/mechatronics-portfolio/blob/main/AGV_Project/03_Drivetrain_Design/Longitudinal%20Model/Plots/gear_ratio_speed.png)

**Description:**
- Shows how top speed varies with gear ratio for different grades

**Key Insight:**
- Increasing gear ratio reduces top speed
- Reveals tradeoff between:
  - Thermal safety (current)
  - Performance (speed)

---

## ⚖️ Design Tradeoff Summary

The plots in this folder collectively show:

- The system is **not torque-limited**, but **thermally limited**
- Gear ratio is the dominant design variable
- An optimal gear ratio exists that balances:
  - Current limits
  - Speed requirements

---

## 🏆 Final Outcome

Based on these plots:

> A gear ratio of approximately **4:1** provides the best balance between motor current limits and vehicle performance across all grades.

---

## 🧠 Notes

- All plots are generated using a physics-based longitudinal model
- Motor current is computed using:
  - Load-based torque demand (required current)
  - Motor torque-speed curve (available current)
- Plots are intended to support engineering decisions, not just visualization

---

## 🔜 Next Steps

Future plots may include:
- Traction limits (μ-slip)
- Lateral dynamics (turning radius, bicycle model)
- Motor thermal modeling

---
