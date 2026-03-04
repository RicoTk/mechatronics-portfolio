# Modbus RTU Debugging Log  
### BLDC Motor Driver (BLD-305S) + Arduino Mega + MAX485

## Overview

This document records the full debugging process used to establish reliable **Modbus RTU communication** between an **Arduino Mega 2560** and a **BLD-305S BLDC motor driver** using a **MAX485 RS-485 transceiver**.

The purpose of this work was to:

- Send speed commands to the motor driver
- Read telemetry from the driver
- Build a stable communication layer for future **motor characterization experiments**

Telemetry of interest included:

- Actual motor speed
- Motor current
- Driver status and faults

The debugging process required multiple iterations of hardware validation, Modbus frame inspection, and timing adjustments.

---

# Hardware Setup

## Controller
Arduino Mega 2560

## RS485 Interface
MAX485 Module

## Motor Driver
BLD-305S BLDC Driver

---

# Wiring

### MAX485 → Arduino

| MAX485 | Arduino Mega |
|------|------|
| DI | TX1 (Pin 18) |
| RO | RX1 (Pin 19) |
| DE | Pin 4 |
| RE | Pin 3 |
| VCC | 5V |
| GND | GND |

### RS485 Bus

Motor Driver A → MAX485 A
Motor Driver B → MAX485 B
Motor Driver GND → Arduino GND


---

# Serial Configuration

According to the driver documentation the communication parameters are:
Baud rate: 9600
Data bits: 8
Parity: None
Stop bits: 1


Arduino configuration:

```cpp
Serial1.begin(9600);

Earlier attempts used:
SERIAL_8E1

This caused communication errors and was removed.

---

Initial Goal

Create a script that:
Sets the motor to internal control mode
Clears faults
Commands the motor to run
Sets a speed reference
Reads telemetry registers (speed and current)

# Problem 1 — Modbus Read Commands Failing

Symptoms
Write commands worked correctly and the motor responded to speed commands.

However, all read operations returned:
READ FAIL

Example debug output:
got=0 (amount of bits received during read attempt)
Read FAIL

## Investigation

A raw RX dump was implemented to inspect the serial data.

Example:
TX: 01 03 00 5F 00 01 B4 18
RX: 01 03 00 5F 00 01 B4 18
    01 03 02 00 00 B8 44

Two frames were observed:
Echo of the transmitted request
Actual Modbus response from the motor driver

## Root Cause
The MAX485 receiver was active during transmission, causing the Arduino to receive its own transmitted frame.
The parser incorrectly interpreted the echo as the response.

## Solution
Discard the echoed request before parsing the response.

Example logic:
send request
read and discard 8 byte echo
read actual response
parse data

# Problem 2 — Motor Stopped Working When Reads Were Added
After implementing read commands, the motor stopped responding to speed commands.

Example log:
speed_raw = 0
curr_raw = 0
motor not spinning

## Investigation
The script was issuing multiple Modbus requests sequentially:
write command
read speed
read current

These were executed too quickly.
At 9600 baud, Modbus RTU requires a silent interval between frames.

## Root Cause
The motor driver was still processing the previous request when the next request arrived.
This caused dropped responses and corrupted transactions.

## Solution
Enforce a quiet interval after each Modbus transmission.
delay(6 ms)
This corresponds to the Modbus RTU silent interval requirement.

# Problem 3 — Bus Congestion From Sequential Reads
Even after adding delays, sometimes only one variable would read correctly.

The script was requesting:
read speed
read current

back-to-back.

## Solution
Implement cycle-based telemetry polling.
Instead of reading both values every loop:

Cycle 1 → read speed
Cycle 2 → read current
Cycle 3 → read speed
Cycle 4 → read current

This reduces bus load and increases reliability.

---

# Final Working Architecture
## Write Commands

Function:

0x06

Registers used:

Register	Description
0x0136	Control mode
0x0076	Clear fault
0x0066	Run command
0x0056	Speed reference

Startup sequence:

set internal control mode
clear fault
stop motor
set speed = 0
run forward
set target speed
Read Commands

Function:

0x03

Registers used:

Register	Data
0x005F	Actual motor speed
0x00B6	Motor current

Final Telemetry Logging Format
t_ms,cmd_rpm,speed_raw,curr_raw,curr_A

Example output:
991777,1000,1000,15,0.600
991977,1000,990,15,0.600
992177,1000,990,17,0.680
992377,1000,990,17,0.680
992578,1000,990,21,0.840
992778,1000,990,21,0.840
992978,1000,990,27,1.080
