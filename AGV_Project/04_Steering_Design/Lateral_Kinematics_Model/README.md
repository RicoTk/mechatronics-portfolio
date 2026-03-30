# Lateral Vehicle Dynamics Modeling

## 🎯 Objective

Develop a lateral dynamics model to evaluate vehicle turning behavior, maneuverability, and stability limits.

This model complements the longitudinal drivetrain analysis by determining:

- Turning radius
- Steering geometry (Ackermann)
- Lateral acceleration
- Maximum safe speed during turns

---

## 🧠 Modeling Approach

A **kinematic bicycle model** was used as a first-order approximation.

Key assumptions:
- Front and rear wheels are lumped into single equivalent wheels
- No tire slip (pure rolling)
- Flat road (no banking effects)

---

## 📊 Key Results

### Turning Radius vs Steering Angle
- Demonstrates nonlinear relationship between steering input and turning capability

### Ackermann Steering Geometry
- Shows required inside/outside wheel angle difference
- Highlights need for proper steering linkage design

### Lateral Acceleration vs Speed
- Reveals how lateral forces increase with speed
- Identifies grip limits

### Max Safe Speed vs Steering Angle
- Defines safe operating envelope
- Shows how steering constrains speed

---

## 🔥 Key Insight

> The vehicle is not limited by drivetrain capability, but by lateral stability constraints. At higher steering angles, safe operating speed must be reduced to avoid exceeding tire grip limits.

---

## 🔗 Relationship to Longitudinal Model

- Longitudinal model determines **maximum achievable speed**
- Lateral model determines **maximum safe speed during turning**

Together, they define the full vehicle operating envelope.

---

## 🔜 Future Work

- Dynamic bicycle model (with slip angles)
- Tire force modeling
- Combined longitudinal + lateral traction (friction circle)
- Control system integration

---
