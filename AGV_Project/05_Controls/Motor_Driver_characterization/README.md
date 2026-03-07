# BLDC Motor Driver Characterization (Modbus Control)

## Overview

This project characterizes the dynamic behavior of a BLDC motor and its driver under speed control using Modbus RTU communication.  
The goal of this experiment was to:

- Establish reliable Modbus communication with the motor driver
- Command motor speed through register writes
- Log real-time telemetry from the driver (speed and current)
- Characterize system response under different operating conditions

The experiments performed include:

1. No-load step response
2. Loaded step response
3. Disturbance rejection testing

These experiments provide insight into the **motor-drive system dynamics**, including time constants, acceleration behavior, current demand, and controller disturbance rejection.

---

# System Description

## Hardware

The control and measurement system consists of the following components:

| Component | Description |
|--------|--------|
| BLDC Motor | Brushless DC motor used as the plant |
| BLD-305S Motor Driver | Closed-loop motor driver with Modbus RTU interface |
| Arduino Mega 2560 | Microcontroller used to generate Modbus commands and log telemetry |
| MAX485 | RS485 transceiver used to interface the Arduino with the driver |
| External Load | Manual load applied during disturbance tests |

The motor driver internally performs closed-loop control of the motor using a speed control algorithm.

The Arduino acts as a **supervisory controller**, sending commands and collecting data.

---

# Communication Architecture

Communication between the Arduino and motor driver is performed using **Modbus RTU over RS485**.

### Communication parameters
Baud Rate: 9600
Data Bits: 8
Parity: None
Stop Bits: 1
Protocol: Modbus RTU


### Key Registers Used

| Register | Description |
|--------|--------|
| `0x0136` | Control mode (internal speed control) |
| `0x0066` | Run command |
| `0x0056` | Speed command |
| `0x005F` | Actual speed feedback |
| `0x00B6` | Motor current |
| `0x0076` | Fault register |

Commands were issued using Modbus function codes:  

0x03 Read Holding Register   
0x06 Write Single Register  


---

# Software Architecture

The Arduino firmware performs three main tasks:

1. Send speed commands to the driver
2. Query driver telemetry
3. Log measurements to serial output

### Data Logged

The following data was recorded during experiments:

time    
commanded speed  
actual speed  
motor current  

Data was exported to CSV format and analyzed using MATLAB / Python plotting tools.  

---

# Experiment 1: No-Load Step Response

### Objective

Characterize the dynamic response of the motor-driver system without external load.  

### Test Sequence

The motor was commanded through a sequence of speed steps:  
  
0 RPM  
500 RPM  
1500 RPM  
2500 RPM  
3000 RPM  
1500 RPM  
0 RPM  


Each step was held long enough for the system to reach steady state.  

### Observations

Key observations include:

- The speed response follows approximately **first-order behavior**  
- The system settles quickly with minimal overshoot  
- Current spikes during acceleration and drops once steady state is reached  

Estimated system properties:

| Parameter | Approximate Value |
|--------|--------|
| Time constant | ~0.25–0.35 s |
| Settling time | ~1 s |
| Maximum tested speed | ~3000 RPM |

This indicates a well-tuned internal controller.  

---

# Experiment 2: Loaded Step Response

### Objective

Evaluate how additional load affects system dynamics.  
A load was applied to the motor shaft during the test sequence.  

### Observations

Compared to the no-load experiment:

- Acceleration became slightly slower
- Current spikes increased during acceleration
- Speed tracking remained stable

This indicates that the internal driver controller compensates for increased torque demand while maintaining speed regulation.

---

# Experiment 3: Disturbance Rejection

### Objective

Evaluate the motor driver's ability to maintain speed when external torque disturbances occur.

### Procedure

The motor was commanded to run at constant speed:  
  
1500 RPM   
2500 RPM   
  
External load was applied manually to the shaft for short intervals.  

### Observations

During disturbance:

- Speed dropped slightly but remained close to the command value
- Current increased significantly to compensate for the load

Measured current spikes reached approximately:  
  
~5 A  


After the disturbance was removed:

- Current quickly returned to nominal levels
- Speed recovered almost immediately

### Interpretation

This behavior indicates:

- Strong disturbance rejection
- Aggressive internal speed loop
- Current-limited torque response

---

# System Behavior Summary

From the experiments performed, the motor-driver system exhibits the following characteristics:

| Property | Observation |
|--------|--------|
| Speed loop behavior | Stable and responsive |
| Dynamic model | Approximate first-order system |
| Time constant | ~0.25–0.35 s |
| Settling time | ~1 s |
| Maximum observed current | ~5 A |
| Disturbance rejection | Strong |

The driver maintains speed by increasing motor current when torque demand increases.  

After the disturbance was removed:

- Current quickly returned to nominal levels
- Speed recovered almost immediately

---  

### Interpretation

This behavior indicates:

- Strong disturbance rejection
- Aggressive internal speed loop
- Current-limited torque response

---  

# Control Architecture Insight

The experiments confirm the following control hierarchy:

External Controller (Arduino)  
↓  
Speed Command (Modbus)  
↓  
Motor Driver Speed Loop  
↓  
Internal Current Control  
↓  
Motor Torque  

This is a **cascaded control architecture** commonly used in robotics and electric vehicles.

---

# Lessons Learned

Key takeaways from this project include:

- Reliable Modbus communication requires careful handling of RS485 timing and bus turnaround
- Echo handling is necessary when using certain RS485 transceivers
- Current measurements provide valuable insight into motor torque behavior
- Step response experiments are effective for estimating system dynamics
- Disturbance rejection testing reveals controller stiffness and torque capability

---

# Future Work

Future development will build upon this characterization work.

### Motion Profile Generation

Implement velocity ramp generators instead of instantaneous speed commands.

Example:

0 → 3000 RPM over 5 seconds  

This introduces:

- acceleration limits
- jerk limits
- trajectory planning

---

### System Identification and Modeling

Using the experimental data collected, a mathematical model of the motor-drive system will be developed in the future.

Possible tools:

- Python
- MATLAB
- Simulink

The model will be used to simulate system response and design higher-level controllers.

---

### Supervisory Control

Future work will implement higher-level control strategies such as:

- velocity trajectory control
- outer PID control loops
- vehicle traction control (for mobile robotics applications)

---

# Repository Structure

Motor_Drive_Characterization/  
  
README.md  
step_test_data.csv  
disturbance_test_data.csv  
  
plots/  
step_test_response.png  
loaded_step_response.png  
disturbance_rejection.png  
  
scripts/  
DisturbanceRejectionTest.ino  
DriverStepTest_Day3.ino  
  

---

# Conclusion

This project successfully demonstrated control and characterization of a BLDC motor driver using Modbus RTU communication.  
  
Through step response, load testing, and disturbance rejection experiments, the system's dynamic behavior and control characteristics were experimentally validated.  
  
The results confirm that the motor driver provides robust speed regulation and strong disturbance rejection, making it suitable for integration into higher-level robotic and vehicle control systems.  
