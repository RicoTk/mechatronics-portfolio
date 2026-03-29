# Longitudinal Vehicle Modeling and Drivetrain Sizing

## 🎯 Objective

Develop a physics-based longitudinal model to evaluate vehicle performance and size the drivetrain for a small autonomous ground vehicle (AGV).

The goal was to determine whether the selected motor and drivetrain could meet:
- Speed requirements
- Grade climbing capability (up to 10%)
- Continuous thermal limits (motor current)

---

## ⚙️ System Overview

- **Configuration:** 2WD rear-drive
- **Motors:** 2 BLDC motors (1 per rear wheel)
- **Drivetrain:** Gear reduction (variable ratio)
- **Wheel Radius:** 0.075 m
- **Vehicle Weight:** ~100 N
- **Target Terrain:** Up to 10% grade

---

## 🧠 Modeling Approach

### 1. Longitudinal Force Balance

The vehicle is modeled using:

\[
F_{net} = F_{tractive} - (F_{grade} + F_{rolling} + F_{drag})
\]

Where:

- \(F_{grade} = W \sin(\theta)\)
- \(F_{rolling} = C_{rr} W \cos(\theta)\)
- \(F_{drag} = \frac{1}{2} \rho C_d A v^2\)

---

### 2. Motor Model

#### Torque-Speed Relationship

\[
T_{motor} = T_{stall} \left(1 - \frac{\omega}{\omega_{no-load}}\right)
\]

#### Torque-Current Relationship

\[
T = K_t I
\]

---

### 3. Required vs Available Current

Two current models were used:

#### Required Current (Load-Based)

\[
I_{required} = \frac{T_{motor, required}}{K_t}
\]

Where required torque is derived from vehicle force demand.

---

#### Available Current (Motor Capability)

\[
I_{available} = \frac{T_{motor, available}}{K_t}
\]

Derived from the motor torque-speed curve.

---

## 📊 Key Results

### 🔹 Force vs Speed
- Verified system can generate sufficient tractive force

### 🔹 Current vs Time
- High current at launch (~16 A)
- Settles into steady-state current region

### 🔹 Required vs Available Current
- System is **mechanically feasible**
- Required current remains below available torque capacity

### 🔹 Thermal Constraint Identified
- Required current exceeds **5.40 A rated current**
- Indicates **thermal limitation**, not torque limitation

---

## ⚖️ Gear Ratio Trade Study

A gear ratio sweep was performed to balance:

- Motor current (thermal constraint)
- Vehicle speed (performance constraint)

### Result:

- Increasing gear ratio reduces required current
- Increasing gear ratio reduces top speed

---

## 🏆 Final Design Decision

> A gear ratio of approximately **4:1** provides the optimal tradeoff.

At this ratio:

- Required current ≤ rated current (5.40 A)
- Vehicle remains capable of:
  - Flat operation
  - 5% and 10% grade climbing
- Acceptable top speeds are maintained

---

## 🧠 Key Engineering Insights

- The system is **thermally limited**, not torque limited
- Load-based current modeling is essential for realistic evaluation
- Gear ratio is the dominant design parameter
- Small changes in gear ratio significantly impact current demand

---

## 🔜 Future Work

- Lateral vehicle modeling (bicycle model)
- Traction limits and tire modeling
- Motor thermal modeling
- Closed-loop control implementation

---

## 📁 Project Structure

01_Longitudinal_Model/
├── Variables.py
├── longitudinal_analysis.py
├── plots/
│ ├── force_vs_speed.png
│ ├── current_vs_time.png
│ ├── required_vs_available.png
│ ├── gear_ratio_current.png
│ ├── gear_ratio_speed.png
├── README.md

---

## 🚀 Key Takeaway

This study demonstrates a full **physics-based drivetrain design workflow**, including:

- System modeling
- Performance evaluation
- Constraint identification
- Trade study and optimization

---

## 📁 Project Structure
