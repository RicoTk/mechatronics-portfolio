# Discrete vs Continuous Control – Day 2

## Continuous-Time System
- Defined by differential equations
- Time flows continuously
- Example: τ dy/dt + y = x

## Discrete-Time System
- Defined by difference equations
- Updated at sampling intervals DT
- Example: y[k] = α y[k-1] + (1-α)x[k]

## Key Differences
- Sampling introduces delay
- Sampling affects stability margins
- Time constant depends on DT

## Insight From Encoder Experiment
- Changing DT changed filter dynamics
- α alone does not define system behavior
- Discrete implementation matters
