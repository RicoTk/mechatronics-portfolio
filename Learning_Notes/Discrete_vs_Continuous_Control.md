# Discrete vs Continuous Control – Day 2

## Continuous-Time System
- Defined by differential equations
- Time flows continuously
- Example: τ dy/dt + y = x
- This example is the standard form of a first-order dynamic system
- These systems: Respond gradually; Cannot change instantly; Have inertia; and Smooth inputs over time
- τ defines: How fast the system reacts; How much lag it introduces
- Large τ -> slower response; more smoothing
- Small τ -> faster response; less smoothing

## Discrete-Time System
- Defined by difference equations
- Updated at sampling intervals DT
- Example: y[k] = α y[k-1] + (1-α)x[k]
- τ = DT/(1 - alpha) (meaning that samplign period directly affects system dynamics)

## Key Differences
- Sampling introduces delay
- Sampling affects stability margins
- Time constant depends on DT

## Insight From Encoder Experiment
- Changing DT changed filter dynamics
- α alone does not define system behavior
- Discrete implementation matters

## Control Systems Insight
- There is always tension between: Responsiveness; Noise Rejection; and Stability Margin. The three can't be maximized.
- If filtered signal becomes equal to raw signal:  all quantization noise, measurement jitter, timing issues, and vibrations pass through
- In a PI loop: the proportional term reacts immediately to error, in the integral term, error gets accumulated and causes drift
- P reacts to noise instantaneously
- I reacts to sustained bias
- Quantization errors occur when the error becomes large relative to the signal (example: a +-1 error to a signal with an average of 2). Solution: better measurement resolution.

| Term | Sensitive to Noise? | Why                                                |
| ---- | ------------------- | -------------------------------------------------- |
| P    | Yes                 | Directly scales noisy error                        |
| I    | Moderately          | Integrates bias, less sensitive to high freq noise |
| D    | Extremely           | Amplifies noise (d/dt effect)                      |


## Miscellaneous Notes
- EMA filter = first-order low-pass (IIR)
- τ depends on DT and α
- Sampling changes dynamics
- Low-speed quantization is the bottleneck
- Noise impacts P-term instantly; bias impacts I-term slowly
