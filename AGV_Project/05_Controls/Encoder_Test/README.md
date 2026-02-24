# Encoder Test (Arduino Mega)

- Encoder: quadrature A/B, powered at 5V
- Pins: A->D2 (interrupt), B->D3
- Sample: 100 ms
- Output: delta counts, rpmRaw, rpmFilt
- CPR: placeholder until datasheet confirmed

Success criteria:
- Stable RPM output at constant speed
- Sign changes with direction reversal
