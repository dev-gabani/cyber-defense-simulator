# 🔥 Cyber Defense Simulator

A full-stack cyber security simulation system that detects and defends against attacks in real-time using behavioral analysis and machine learning.

---

## 🚀 Overview

This project simulates a real-world cyber defense pipeline:

Attack → Logging → Feature Extraction → Detection → Defense → Live Dashboard

It generates different types of traffic, analyzes behavior patterns, detects anomalies, and blocks malicious IPs — all in real-time.

---

## 🧠 Key Features

### ⚔️ Attack Simulation
- Normal user traffic
- DoS-style flooding
- Brute-force login attempts
- Custom IP simulation using headers

### 🗄️ Backend (FastAPI)
- REST APIs for login and data access
- Real-time logging into SQLite database
- WebSocket server for live updates
- Automatic IP blocking system

### 📊 Feature Engineering
- Requests per second
- Failed login ratio
- Unique endpoint access
- Sliding time window analysis (last 60 seconds)

### 🤖 Detection System
- Rule-based anomaly detection
- Machine learning using Isolation Forest (optional module)
- Real-time threat identification

### 🛡️ Defense System
- Automatic IP blocking
- Persistent block storage (SQLite)
- Request-level protection

### 📡 Real-Time Dashboard (React)
- Live traffic monitoring
- Attack visualization
- Blocked IP tracking
- Interactive charts and metrics
- Connection status indicator

---

## 🏗️ Project Structure


cyber_project/
│
├── attack_simulator/
├── database/
├── defense/
├── detection/
├── server/
├── frontend/
│
├── requirements.txt
├── .gitignore
├── README.md


---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/dev-gabani/cyber-defense-simulator.git
cd cyber-defense-simulator
2️⃣ Backend Setup
pip install -r requirements.txt
uvicorn server.main:app --reload
3️⃣ Frontend Setup
cd frontend
npm install
npm run build
4️⃣ Open Dashboard
http://127.0.0.1:8000
⚔️ Run Attack Simulator
cd attack_simulator
python attacker.py

Choose:

Normal Traffic
DoS Attack
Brute Force Attack
🔍 How It Works
Attacker sends traffic to server
Server logs requests into database
Feature extractor analyzes behavior patterns
Detection system identifies anomalies
Defense system blocks malicious IPs
Dashboard updates in real-time via WebSocket
🧪 Technologies Used
Backend
FastAPI
SQLite
Python
Frontend
React + Vite
Chart.js
Tailwind CSS
ML
Scikit-learn (Isolation Forest)
NumPy
📈 Future Improvements
Full ML integration into real-time pipeline
Attack classification (DDoS / Brute Force / Bot)
Authentication & role-based access
Deployment on cloud (AWS / Docker)
👨‍💻 Author

Dev Gabani

⭐ If you like this project

Give it a star ⭐ and feel free to fork!