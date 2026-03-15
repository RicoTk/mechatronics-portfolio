# Day 4 Experiment Log

Time spent: ~1.5 hours

## Goal

Validate motor speed measurements using three independent signals:

- driver speed register
- driver PG pulse output
- external incremental encoder

## Work Completed

Implemented pulse counting for both encoder and PG signals.

Integrated Modbus communication with the motor driver to read the speed register.

Performed step speed tests between:

0 → 1000 → 1500 → 2000 → 2500 RPM

Collected and plotted the data using Excel.

## Key Finding

The external encoder consistently reported speeds approximately 25% higher than the actual motor speed.

Manual rotation tests confirmed the encoder produces approximately 600 pulses per revolution.

The discrepancy only occurs while the motor is running.

## Diagnosis

The most likely cause is electrical noise from the motor driver creating false encoder pulses.

The driver PG output was confirmed to match the actual motor speed.

## Decision

Use PG signal as the primary speed measurement for the next experiments.

## Next Step

Motor system identification using step response experiments.
