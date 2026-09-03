# Algorithmic-Pathfinding-Engine

A high-performance C++17 algorithmic engine that benchmarks BFS vs. A* search complexities, paired with an automated Python ETL pipeline that warehouses the results in Microsoft Azure for visualization.

## The Tech Stack
* **Algorithmic Engine:** C++17, Polymorphic Memory Resources (PMR)
* **Cloud Infrastructure:** Microsoft Azure SQL Database
* **ETL Pipeline:** Python, Subprocess, PyODBC, SQLAlchemy
* **Data Visualization:** Pandas, Seaborn, Matplotlib

## Core Architecture
1. **Memory-Pooled C++ Engine:** Utilizes 1D grid mapping and C++17 `std::pmr` memory pooling to prevent heap fragmentation during massive Pathfinding Node expansions.
2. **Automated Subprocess Controller:** A Python daemon that programmatically compiles, executes, and harvests standard output from the C++ binaries across scaling grid complexities.
3. **Fault-Tolerant Cloud ETL:** Incorporates automated retry logic and batch-processing (`executemany`) to securely upload execution metrics to a remote Microsoft Azure SQL database.
4. **Automated Dashboarding:** Uses SQLAlchemy to pull remote data back to the local machine, rendering publication-ready Seaborn charts analyzing algorithmic compute vs. memory costs.

## Visual Proof

<img width="1751" height="745" alt="Screenshot 2026-07-25 120020" src="https://github.com/user-attachments/assets/df447da9-9723-4fe7-bacf-633b3545596d" />



##  How to Run Locally
**0. The Compile Command:**
```bash
g++ -std=c++17 main.cpp -o main.exe
```
**1. Define Environment Variables:** 
```bash
Create a `.env` file with your Azure credentials (`AZURE_SERVER_NAME`, `AZURE_DATABASE`, etc.).
```
**2. Install Dependencies:**
```bash
pip install -r requirements.txt
```
**3. Run the Automated Benchmark Pipeline:**
```bash
python python_control.py
```
**4. Render the Analytics Dashboard:**
```bash
python python_dashboard.py
```
