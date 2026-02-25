# Speed Control Architecture (Draft)

## Objective
Maintain target wheel speed (RPM) under varying load using closed-loop control.

## Signals
- Command: rpm_cmd (RPM)
- Measurement: rpm_meas (hybrid estimator: window+period)
- Error: e = rpm_cmd - rpm_meas
- Output: u (motor command, e.g., PWM duty or driver speed command)

## Update Rates
- Encoder ISR: edge-based
- Velocity estimate update: 50 ms
- Control loop update: 50 ms (typically same as velocity update)

## Controller
- Type: PI controller
- Proportional: uP = Kp * e
- Integral: uI += Ki * e * DT
- Total: u = uP + uI

## Output Limits & Safety
- Saturation: u clipped to [u_min, u_max]
- Anti-windup: freeze/clamp integrator when saturated
- Fault handling: if rpm_meas invalid for > 300 ms → set u=0

## Testing Plan
1. Open-loop step test (command → response)
2. Closed-loop small Kp, Ki=0
3. Add Ki slowly (remove steady-state error)
4. Test at low speed and high speed
5. Test under load disturbance
