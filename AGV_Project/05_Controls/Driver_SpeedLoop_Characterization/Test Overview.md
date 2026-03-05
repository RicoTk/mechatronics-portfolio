
# Objectives:
Understand motor dynamic behavior and driver system  
Measuring system response when speed command suddenly changes  

### System characteristics to discover:
- system time constant
- acceleration capability
- driver behavior
- load response
- current draw during acceleration

# Experimental Procedure:
1. Applying step inputs in speed
    - 500 RPM   → hold 4 s
    - 1500 RPM  → hold 4 s
    - 2500 RPM  → hold 4 s
    - 1000 RPM  → hold 4 s
    - 0 RPM     → hold 4 s
2. Log variables
    - time
    - commanded RPM
    - actual speed
    - current
3. Plot
    - speed vs time
    - current vs time


###  These values and plots should allow me to understand the systems:
- rise time
- settling time
- overshoot
- current spikes during acceleration
