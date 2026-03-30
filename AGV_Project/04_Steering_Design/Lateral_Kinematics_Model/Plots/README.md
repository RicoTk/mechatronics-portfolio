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
![Turning Radius](mechatronics-portfolio/AGV_Project/04_Steering_Design/Lateral_Kinematics_Model/plots/turning_radius_vs_steering_angle.png)

---

### Ackermann Steering Angles
![Ackermann](mechatronics-portfolio/AGV_Project/04_Steering_Design/Lateral_Kinematics_Model/plots/ackermann_steering_angles_vs_turning_radius.png)

---

### Lateral Acceleration vs Speed
![Lateral Acceleration](mechatronics-portfolio/AGV_Project/04_Steering_Design/Lateral_Kinematics_Model/plots/lateral_acceleration_vs_speed.png)

---

### Max Safe Speed vs Steering Angle
![Safe Speed](mechatronics-portfolio/AGV_Project/04_Steering_Design/Lateral_Kinematics_Model/plots/max_safe_speed_vs_steering_angle.png)

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
