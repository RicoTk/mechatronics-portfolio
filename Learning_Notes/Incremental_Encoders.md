# What is an incremental encoder?

- An incremental encoder is an electromechanical device that measures changes in motion and direction.
- Incremental rotary encoders generate A/B digital output signals based on a specific number of pulses per rotation.
- In this way, the angular motion of a shaft is converted into a code (encoded) to determine its velocity or relative position.
- Incremental encoders give near instantaneous feedback on position changes, they’re often used in applications where highly precise measurement and motion control is required.

## How do they work?

- Encoders generate a fixed amount of electrical pulses per rotation, this mechanical characteristic defines the resolution of the encoder.
- A digital signal is sent through channels A and B of an encoder, for quadrature encoders these channels are at a phasing offset of 90 degrees.
- Tracking one channel will only give pulses per rotation information (which gives you the magnitude of your speed) while trackign both A and B allows you to get magnitude and direction.
- When the shaft rotates in one direction, the A signal will lead the B signal, and for the opposite direction, B will lead A.

 # Incremental Encoder vs Absolute Encoder

 ## Incremental Encoder  
 
 | Advantages | Disadvantages|
| --- | --- |
| Less expensive than an absolute encoder | Lose position data after losing power | 
| Great for speed measurement  | Susceptible to signal noise |

 ## Absolute Encoder  
 
 | Advantages | Disadvantages|
| --- | --- |
| More accurate position measurement | More expensive than an incremental encoder | 
| Doesn't lose position report after losing power  | More complex hardware setup |

# Velocity Estimation in Incremental Encoders  

## Time between pulses
- pulse ---- 5 ms ---- pulse
- RPM ∝ 1 / time_between_pulses
- Excellent low speed resolution
- Very noisy at high speed
- Used in high precision robotics and low speed motion systems

## Fixed time window
- 100 ms window
- count = 120 pulses
- RPM = counts / CPR (counts per revolution) * 60 / time
- Most motor controllers and PLCs use this technique
- It is simple, stable, has low load on the CPU and works well for controls loops
- 
- 

- 
