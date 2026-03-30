# Kinematic Bicycle Model

## 🎯 Objective

Implement a first-order lateral dynamics model to analyze vehicle turning behavior and stability limits.

---

## ⚙️ Model Description

The vehicle is approximated as a bicycle model:

\[
R = \frac{L}{\tan(\delta)}
\]

Where:
- \(R\) = turning radius
- \(L\) = wheelbase
- \(\delta\) = steering angle

---

## 📊 Plots

### Turning Radius vs Steering Angle
![Turning Radius](plots/turning_radius.png)

---

### Ackermann Steering Angles
![Ackermann](plots/ackermann_angles.png)

---

### Lateral Acceleration vs Speed
![Lateral Acceleration](plots/lateral_acceleration.png)

---

### Max Safe Speed vs Steering Angle
![Safe Speed](plots/safe_speed.png)

---

## 🧠 Key Findings

- Turning radius decreases rapidly at low steering angles
- Ackermann geometry is necessary for realistic steering behavior
- Lateral acceleration increases quadratically with speed
- Tire grip limits impose strict constraints on turning speed

---

## ⚠️ Engineering Insight

At high steering angles, the maximum safe speed decreases significantly:

- 5° → ~6 m/s safe
- 20° → ~3 m/s safe

This indicates the need for **speed control based on steering input**.

---
