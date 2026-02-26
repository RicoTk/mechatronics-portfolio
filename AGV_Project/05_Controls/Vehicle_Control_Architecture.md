# Vehicle Control Architecture (V1)

## Actuation Interface
- Motor driver accepts: Speed command register (RPM)
- Driver internally controls: current/torque/speed loops (black box)

## Measurements
- Primary (today): driver speed feedback register (RPM)
- Secondary (future validation): Arduino quadrature encoder RPM

## Control Layers
1. Driver internal speed control (existing)
2. Vehicle-level wheel behavior (future):
   - left/right speed matching for straight driving
   - turning behavior via target wheel speeds
3. Higher-level (future): position/path tracking

## Loop Timing Targets
- Telemetry logging: 10 Hz (100 ms)
- Vehicle-level correction loop (future): 20 Hz (50 ms)

## Safety
- E-stop or fault -> command speed = 0 immediately
- Loss of comms timeout -> command speed = 0 after ___ ms (start 500 ms)

## Day 3 Goal
Characterize the driver’s internal speed-loop response to step commands.
