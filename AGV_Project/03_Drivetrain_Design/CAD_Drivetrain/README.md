# 4:1 Spur Gear Gearbox Design (AGV Drivetrain)

## Overview
This project consists of the design and modeling of a **4:1 gear reduction gearbox** intended for use in a small autonomous ground vehicle (AGV). The gearbox is designed to increase output torque while reducing motor speed, supporting traction and load requirements for off-road operation.

The design was developed in SolidWorks and focuses on:
- Compact packaging
- Structural integrity
- Ease of assembly
- Proper shaft support and alignment

---

## Key Specifications

| Parameter            | Value              |
|---------------------|-------------------|
| Gear Ratio          | 4:1               |
| Gear Type           | Spur Gears        |
| Number of Stages    | Single-stage      |
| Housing             | Split enclosure   |
| Shaft Support       | Ball bearings     |
| Mounting            | Base flange mount |

---

## Design Highlights

- **4:1 Reduction** achieved using a small pinion and larger driven gear
- **Bearing-supported shafts** to reduce friction and ensure alignment
- **Split housing design** for easy assembly and maintenance
- **Compact footprint** suitable for integration into small robotic platforms
- **Fully constrained gear alignment** within a rigid enclosure

---

## CAD Model

### Isometric View
![Isometric View]([images/gearbox_iso.png](https://github.com/RicoTk/mechatronics-portfolio/blob/main/AGV_Project/03_Drivetrain_Design/CAD_Drivetrain/Pictures/gearbox_iso.png))

### Internal Gear Layout
![Gear Layout]([images/gear_layout.png](https://github.com/RicoTk/mechatronics-portfolio/blob/main/AGV_Project/03_Drivetrain_Design/CAD_Drivetrain/Pictures/gear_layout.png))

### Alternate Isometric View
![Alt View]([images/gearbox_iso_2.png](https://github.com/RicoTk/mechatronics-portfolio/blob/main/AGV_Project/03_Drivetrain_Design/CAD_Drivetrain/Pictures/gearbox_iso_2.png))

---

## Technical Breakdown

### Gear Train
- Input shaft drives a **small pinion gear**
- Pinion engages with a **larger output gear**
- Gear ratio: 4:1
  

### Shaft Support
- Each shaft is supported by **dual bearings**
- Reduces:
  - Radial deflection
  - Misalignment
  - Friction losses

### Housing Design
- Bottom block contains:
  - Bearing seats
  - Shaft channels
- Top cover:
  - Encloses gear train
  - Protects from debris
  - Maintains alignment

---

## Exploded View

![Exploded View]([images/gearbox_exploded.png](https://github.com/RicoTk/mechatronics-portfolio/blob/main/AGV_Project/03_Drivetrain_Design/CAD_Drivetrain/Pictures/gearbox_exploded2.png))

---

## Front and Top Views

### Front View
![Front View]([images/front_view.png](https://github.com/RicoTk/mechatronics-portfolio/blob/main/AGV_Project/03_Drivetrain_Design/CAD_Drivetrain/Pictures/front_view.png))

### Top View
![Top View]([images/top_view.png](https://github.com/RicoTk/mechatronics-portfolio/blob/main/AGV_Project/03_Drivetrain_Design/CAD_Drivetrain/Pictures/top_view.png))

---

## Design Considerations

### 1. Load Handling
- Designed to increase torque output for:
  - Incline operation
  - Load Handling

### 2. Alignment & Tolerances
- Bearing pockets ensure coaxial alignment
- Housing geometry minimizes shaft misalignment

### 3. Manufacturability
- Geometry compatible with:
  - CNC machining
  - 3D printing (prototype stage)

### 4. Serviceability
- Split housing allows:
  - Easy inspection
  - Gear replacement
  - Maintenance access

---

## Possible Future Improvements

- Add **lubrication system** (grease pocket or oil bath)
- Perform **stress analysis (FEA)** on gears and shafts
- Evaluate **gear material selection** (steel vs polymer)
- Add **sealing features** for dust protection (important for agricultural environments)
- Integrate with **motor mounting plate**
- Perform **efficiency and backlash testing**

---

## Application in AGV System

This gearbox will be integrated into the AGV drivetrain to:
- Convert high-speed motor output into usable torque
- Improve traction on uneven terrain
- Enable controlled motion under load

---

## Author
Frederico Ferreira do Nascimento  
Mechanical Engineer | Robotics & Mechatronics  

---
