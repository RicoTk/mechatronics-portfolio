# Day 2 – Encoder RPM Measurement (Manual)

## Setup
- Arduino Mega
- Quadrature encoder (A/B), powered at 5V
- ISR on Channel A (CHANGE), direction from Channel B
- Sample window: 100 ms
- Filter: EMA (alpha=0.8)

## Results
- Raw RPM shows quantization noise at low speeds (small count deltas per 100 ms window).
- At higher manual speeds, raw RPM variation increases mainly due to non-uniform hand input.
- EMA filtering produces a usable speed signal but introduces lag during transitions.
- Direction decoding validated (sign change during reversal).
- End-to-end pipeline validated: Arduino → CSV → MATLAB plot.

## Next Experiments
- Tune alpha to reduce lag while preserving stability.
- Reduce sample window to improve responsiveness and quantify the noise tradeoff.
- (Future) Evaluate period-based estimation for low-speed operation and compare to window method.
