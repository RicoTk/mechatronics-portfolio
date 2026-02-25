# Encoder Measurement Experiments 

## Objective
Develop a robust RPM estimation pipeline for a quadrature encoder using an Arduino Mega, evaluating tradeoffs between window-based and period-based measurement methods.

---

## 1. Window-Based Velocity Estimation

### Method
- Count encoder edges over fixed sampling window (Δt).
- Compute:
  RPM = (Δcounts / Δt) / CPR × 60
- CPR = 2 × PPR_A (A channel on CHANGE)

### Observations

- At low speeds:
  - Very small Δcounts per window.
  - Quantization effects dominate.
  - Raw RPM signal becomes noisy or zero.
- At higher speeds:
  - Measurement becomes stable.
  - Natural averaging effect from larger count values.

### Tradeoff
- Larger window → smoother, more lag.
- Smaller window → faster response, more jitter.

---

## 2. Exponential Moving Average (EMA) Filter

### Implementation
y_k = α y_{k-1} + (1 - α) x_k

### Key Insight
Effective time constant:

τ ≈ DT / (1 - α)

This links sampling period and filter coefficient.

### Experiments

| SAMPLE_MS | ALPHA | Behavior |
|------------|--------|----------|
| 100 ms | 0.8 | Stable, noticeable lag |
| 50 ms | 0.9 | Similar lag (τ preserved), smoother updates |
| 50 ms | 0.8 | Faster response, acceptable noise |

### Conclusion
50 ms sampling with α = 0.8 provides improved responsiveness while maintaining stability.

---

## 3. Period-Based Velocity Estimation

### Method
- Measure time between consecutive A edges using micros().
- Compute:
  RPM = 60 / (Δt_edge × CPR)

### Observations
- Performs well at very low speeds.
- Provides non-zero RPM when window method fails.
- Requires proper direction handling.

---

## Engineering Takeaways

- Sampling frequency directly affects filter dynamics.
- Measurement method must be matched to speed regime.
- Quantization dominates at low speeds.
- Proper documentation of tradeoffs prevents premature optimization.

---

## Next Steps

- Integrate velocity estimator into closed-loop speed control.
- Validate under motor-driven conditions.
- Integrate velocity estimator into closed-loop speed control.
- Validate under motor-driven conditions.
- Characterize estimator behavior under load.
