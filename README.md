# 🖥️ Real-Time System Health Monitor

A real-time system monitoring dashboard built with Python and Streamlit that tracks CPU, RAM, disk usage, network activity, system information, running processes, and system health alerts.

## 📌 Features

- 📊 Real-time CPU usage monitoring
- 💾 RAM usage monitoring
- 💿 Disk usage monitoring
- 🌐 Upload and download speed monitoring
- ❤️ Overall system health score
- 🚨 Configurable system alerts
- 📈 CPU usage history chart
- 📈 RAM usage history chart
- ⚙️ System information display
- 🖥️ Top running processes
- 🔄 Automatic dashboard refresh
- 🎛️ Customizable monitoring thresholds

## 🛠️ Technologies Used

- Python
- Streamlit
- Psutil
- Pandas
- Plotly
- Git & GitHub

## 📊 Monitoring Dashboard

The dashboard provides real-time information about:

| Resource | Monitoring |
|---|---|
| CPU | Current CPU utilization |
| RAM | Current memory utilization |
| Disk | Current disk utilization |
| Network | Upload and download speed |
| Processes | Top running processes |
| System | OS, CPU architecture, RAM, disk and Python version |
| Health | Overall system health score |

## 🚨 Smart Alert System

The application generates alerts when resource usage becomes high.

Users can configure warning thresholds for:

- CPU
- RAM
- Disk

The dashboard also identifies critical resource usage conditions.

## 📈 Data Visualization

The application uses Plotly to visualize CPU and RAM usage history in real time.

Historical readings are maintained during the active monitoring session to help observe system resource trends.

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Jagadeeshagouda-R-B/System-Health-Monitor.git

cd System-Health-Monitor
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py