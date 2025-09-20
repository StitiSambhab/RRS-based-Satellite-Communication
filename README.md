# Reconfigurable Intelligent Surface Based Satellite Communication

This project explores **satellite communication optimization** using **Line-of-Sight (LOS)** paths and **Reconfigurable Refractive Surfaces (RRS)** to minimize the number of satellite hops required to connect two Earth-based locations.  
It demonstrates how incorporating RRS nodes in orbital space improves connectivity, reduces delays, and enhances efficiency compared to pure LOS-based communication.

---

## 📖 Project Overview
- Traditional satellite communication relies only on **direct LOS**, often leading to inefficient routing.  
- This project introduces **RRS nodes** (virtual "mirrors" in space) that redirect signals when direct LOS is unavailable.  
- A **Python-based simulation** evaluates both LOS-only and RRS-assisted paths.

---

## 🛠 Features
- Convert geographic coordinates (latitude, longitude, altitude) to 3D Cartesian space.
- Generate **satellite constellations** in configurable orbits (planes × satellites per plane).
- Insert **RRS nodes** at random orbital offsets to simulate refractive surfaces.
- Implement **LOS checking** between Earth points and satellites.
- Use **Breadth-First Search (BFS)** to find the minimum-hop path between satellites.
- Compare performance **with vs. without RRS**.

---

## 📂 Repository Structure
- main.py # Main simulation script
- Report.pdf # Full project report with methodology, analysis, and references
- README.md # Project documentation

---

## 📊 Results
- LOS-only model often requires longer paths and more satellites.
- RRS-assisted model reduces satellite hops, improving efficiency and reliability.
- Signal quality (measured via ∑ 1/√d) generally improves with RRS.

---

## 📌 Future Work
- Implement smarter RRS placement strategies.
- Explore dynamic, programmable metasurfaces for real-time adaptation.
- Optimize pathfinding with A* or heuristic algorithms for scalability.
---
## 📚 References
- Rayees, M. A., et al. (2021). Satellite relay optimization with LOS constraints.
- Xie, H., et al. (2020). Reconfigurable Refractive Surfaces: An Energy-Efficient Way to Holographic MIMO.
- Starlink constellation public data.
- BFS Pathfinding in Graph Theory.

---
## 👤 Author

- Stiti Sambhab Das     
Supervised by** Dr. Syed Mohammad Zafaruddin**
