# Control Systems & Motor Control Cheat Sheet

This document summarizes key formulas, concepts, and engineering intuition related to motor control, system dynamics, and industrial communication.

The concepts here were learned while developing and characterizing a Modbus-controlled BLDC motor system.

---

# 1. Motor Physics

## Torque–Current Relationship

Motor torque is proportional to current.

T = Kt * I

Where:

T = torque (Nm)  
Kt = torque constant (Nm/A)  
I = motor current (A)

Engineering intuition:

- More current → more torque
- Acceleration requires torque
- Torque increases when load increases

Observed experimentally:


acceleration → current spike
steady state → low current
load applied → current increases


---

# 2. Speed–Voltage Relationship

For many motors:

ω ≈ Kv * V

Where:

ω = speed  
Kv = speed constant  
V = applied voltage

Motor drivers control voltage internally to regulate speed.

---

# 3. Power Relationships

Electrical power:

P = V * I

Mechanical power:

P = T * ω

Where:

T = torque  
ω = angular velocity

---

# 4. First-Order System Model

Many physical systems behave approximately like a **first-order system**.

General equation:

τ (dy/dt) + y = K * u

Where:

τ = time constant  
y = output  
u = input  
K = gain

Example in motor control:


input = commanded speed
output = actual speed


---

# 5. Time Constant (τ)

The **time constant** describes how quickly a system responds.

For a step input:

| Time | % of final value |
|-----|------------------|
| 1τ | 63% |
| 2τ | 86% |
| 3τ | 95% |
| 4τ | 98% |

Engineering rule:


Settling time ≈ 4τ


Example from experiments:


τ ≈ 0.25–0.35 seconds


---

# 6. Step Response

A step input changes the command instantly.

Example:


1500 RPM → 2500 RPM


Step response reveals:

- system speed
- stability
- controller tuning
- overshoot
- damping

Typical shape for a well-tuned motor controller:


smooth rise
minimal overshoot
quick settling


---

# 7. System Identification

Experimental testing allows estimation of system parameters.

From step response:

You can estimate:

- time constant
- steady-state gain
- delay
- settling time

This helps create mathematical models for simulation.

---

# 8. Cascaded Control Architecture

Most motor controllers use nested loops.

Typical structure:


Position Loop (optional)
↓
Speed Loop
↓
Current Loop
↓
Motor Torque


Why cascaded control is used:

- faster inner loops stabilize slower outer loops
- improves stability
- improves disturbance rejection

Example in this project:


Arduino → speed command
Motor driver → internal speed controller
Driver firmware → current controller
Motor → torque output


---

# 9. Disturbance Rejection

A disturbance is any external force affecting the system.

Examples:

- mechanical load
- friction
- slope (robotics)
- collisions

Observed behavior:


load applied → current increases → speed maintained


The controller compensates automatically.

Good disturbance rejection indicates:

- strong controller tuning
- sufficient torque capability

---

# 10. Current Limiting

Motor drivers often enforce a current limit.

Purpose:

- protect driver electronics
- protect motor windings
- prevent overheating

Effect:


max torque = Kt * Imax


If current limit is reached:

- torque saturates
- acceleration decreases
- speed regulation weakens under heavy load

---

# 11. RS485 Communication

RS485 uses **differential signaling**.

Advantages:

- high noise immunity
- long cable distances
- multi-device bus

Signals:


A
B


The receiver measures the **difference** between them.

---

# 12. RS485 Direction Control

RS485 transceivers require switching between transmit and receive.

Typical pins:


DE (Driver Enable)
RE (Receiver Enable)


Typical sequence:


Enable transmit
Send frame
Flush serial buffer
Disable transmit
Enable receive
Wait for response


Incorrect timing can cause:

- lost responses
- bus collisions
- incomplete frames

---

# 13. Modbus RTU Frame Structure

Basic frame:


[Slave ID]
[Function Code]
[Register Address]
[Data]
[CRC]


Example:


01 03 00 B6 00 01 CRC


Meaning:


Device 1
Read register 0x00B6
Read 1 register


---

# 14. Common Modbus Function Codes

| Code | Meaning |
|-----|--------|
| 03 | Read holding register |
| 04 | Read input register |
| 06 | Write single register |
| 16 | Write multiple registers |

---

# 15. CRC Error Checking

Modbus uses **CRC-16**.

Purpose:

- detect corrupted packets
- ensure communication reliability

If CRC fails:


message is discarded


---

# 16. Echo Behavior

Some RS485 setups return the transmitted frame.

Sequence may look like:


TX request
RX echo
RX slave response


Software must discard the echo.

---

# 17. Debugging Industrial Communication

Typical troubleshooting steps:

1. Verify wiring
2. Verify baud rate
3. Verify frame format
4. Check CRC
5. Check timing between messages
6. Inspect raw frames
7. Verify device address
8. Confirm register addresses

---

# 18. Useful Experimental Tests

For motor systems:

### Step Response Test

Characterizes system dynamics.

### Loaded Step Test

Reveals torque demand behavior.

### Disturbance Test

Measures controller robustness.

---

# 19. Engineering Intuition

Key patterns to remember:


acceleration → high current
steady speed → low current
disturbance → current spike


Speed changes slowly because:


inertia resists acceleration


---

# 20. Future Topics to Explore

- PID control
- field-oriented control (FOC)
- trajectory planning
- motion profiles
- system identification
- motor modeling

---

# Summary

This cheat sheet condenses key ideas related to:

- motor physics
- control systems
- industrial communication
- system characterization

These concepts form the foundation for robotics, automation, and electric vehicle systems
