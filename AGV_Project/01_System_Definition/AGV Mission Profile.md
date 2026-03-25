# AGV Mission Profiles

## 1. Environment Assumptions
- Terrain: Dry soil and flat plains, with clay-like porous soil characteristics
- Slopes: Typical operating slopes of 5–10% grade
- Obstacles: Dust, loose soil patches, shrubbery, and small vegetation
- Weather: Warm subtropical climate with seasonal rainfall
- Temperature Range: 18–35 °C
- Surface Variability: Vehicle may encounter local transitions between compact soil, loose patches, and muddy soil after rainfall

## 2. Primary Mission Scenarios

### Scenario 1 — Flat Transport
- Payload: 20 kg
- Speed: 2–3 m/s
- Terrain: Flat, compact soil
- Duration: Sustained transport operation
- Behavior: Straight-line travel between field points

### Scenario 2 — Incline Operation
- Payload: 20 kg
- Slope: 5–10% grade
- Speed: 1–2 m/s
- Behavior: Climb from flat terrain and maintain controlled uphill motion

### Scenario 3 — Turning Maneuver
- Payload: 20 kg
- Speed: 0.5–1 m/s
- Behavior: Tight turning at low speed
- Terrain: Compact soil or higher-resistance surface
- Notes: Used to evaluate steering geometry and steering actuator load

### Scenario 4 — Start/Stop Operation
- Payload: 20 kg
- Behavior: Frequent acceleration, deceleration, and speed adjustment during short movements
- Notes: Used to evaluate transient torque demand and control responsiveness

### Scenario 5 — Idle / Standby
- Behavior: Motors off or at minimal power
- Sensors and control electronics remain active
- Notes: Used to estimate auxiliary power draw and standby energy use

## 3. Worst-Case Design Scenarios

### Worst Case 1 — Grade Start
- Full payload: 20 kg
- Slope: 10% grade
- Starting from rest
- Reduced traction surface possible

### Worst Case 2 — Low-Traction Patch
- Full payload: 20 kg
- Loose or muddy soil
- Low-speed maneuvering or restart condition
- Used to evaluate traction margin and slip risk

### Worst Case 3 — Steering Load Case
- Full payload: 20 kg
- Low-speed tight turn
- High steering resistance due to terrain
- Used to size steering actuator and linkage

## 4. Degraded / Off-Nominal Conditions
- Battery state of charge below 15%
- Heavy rainfall or muddy terrain
- Ambient temperature near 35 °C
- Dust exposure affecting sensors and driveline interfaces

## 5. First-Pass Duty Cycle
- Flat transport: 40%
- Incline operation: 15%
- Turning maneuvers: 10%
- Start/stop operation: 15%
- Idle / standby: 20%

Note: Worst-case and degraded conditions are treated as design checks, not regular duty-cycle categories.
