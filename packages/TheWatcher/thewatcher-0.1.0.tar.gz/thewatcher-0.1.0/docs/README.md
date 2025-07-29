# 🐾 Simple Network Monitoring System  
> Real-Time Network Traffic Monitoring Tool — Cute, Powerful, and Practical! 💻📊

---

## Overview

This project is a **modular, Python-based** tool for real-time network traffic monitoring and analysis.  
Designed for **network enthusiasts** and **cybersecurity students**, it provides packet-level insights in a sleek way!

---

## ✨ Key Features

### 🔍 Packet Inspection
- 📦 Protocol-based logging
- 🎯 User-defined filters: protocol, IP, port

### ⏱️ Real-Time Monitoring
- 📈 Live traffic summaries
- 🖥️ Device scanning and monitoring

### 🚨 Alert System
- 🔔 Custom threshold-based alerts
- 🔥 Severity-level classification

### 🧩 Modular Design
- 🧱 Scalable and extendable modules
- 🖥️ CLI & GUI support (`snm_cli`, `snm_gui`)

### 🗃️ Database Setup
- 🐬 SQLite-based
- Tables: filters, thresholds, blacklists, status

---

## 🛠️ Installation

### ✅ Prerequisites

- 🐍 Python 3.x
- 📦 Required packages listed in `requirements.txt`

### 📥 Clone the Repository

```bash
git clone https://github.com/Bigst3pp3r/Simple-Network-Monitoring-System-main.git
cd Simple-Network-Monitoring-System-main
```
### 📦 Install Dependencies
```bash
pip install -r requirements.txt
```

### 🚀 Usage
🖥️ Command-Line Interface (CLI)
Navigate to the project directory

Run the main script:
```bash
python main.py
```

### 🎛️ CLI Options
- Set Filters 🧪
- Manage Thresholds ⚙️
- Start Monitoring 📡
- Scan Network 🌐
- Monitor Devices 🕵️

### 🧸 Graphical User Interface (GUI)
Launch the GUI:
```bash
python src/main_gui.py
```
### 🖼️ GUI Features
- 🔐 Login system (role-based access)
- 🧭 Dashboard, settings, alerts, devices, packets
- 🧵 Multi-threaded real-time monitoring

### 🗂️ File Structure
```bash
📁 Simple-Network-Monitoring-System
├── main.py                    # CLI entry point
├── src/
│   ├── main_gui.py            # GUI entry point
│   ├── monitoring_core.py     # Core monitoring logic
│   ├── filters.py             # Filter + DB logic
│   ├── devices_gui.py         # Device GUI
│   ├── alerts_gui.py          # Alerts GUI
│   └── packets_gui.py         # Packets GUI
├── src/database/              # Database files
└── tests/                     # Unit tests
```

### 🐢 Made with Python, curiosity, and a love for clean networks!
