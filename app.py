import streamlit as st
import psutil
import time
import pandas as pd
import plotly.graph_objects as go
import platform
from datetime import datetime


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="System Health Monitor",
    page_icon="🖥️",
    layout="wide"
)

# ==========================================
# CUSTOM UI STYLING
# ==========================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 17px;
    opacity: 0.7;
    margin-bottom: 25px;
}

.section-title {
    font-size: 26px;
    font-weight: 600;
    margin-top: 25px;
}

.metric-card {
    padding: 20px;
    border-radius: 14px;
    border: 1px solid rgba(128, 128, 128, 0.25);
    background: rgba(128, 128, 128, 0.08);
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.metric-card:hover {
    transform: translateY(-2px);
    border-color: rgba(255, 255, 255, 0.45);

}

/* Professional dashboard polish */

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.stProgress > div > div > div {
    border-radius: 10px;
}

[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)



# ==========================================
# SESSION STATE
# ==========================================

if "history" not in st.session_state:
    st.session_state.history = []


# ==========================================
# GET SYSTEM INFORMATION
# ==========================================

cpu_usage = psutil.cpu_percent(interval=0.5)

memory = psutil.virtual_memory()
ram_usage = memory.percent

disk_usage = psutil.disk_usage("/").percent

network = psutil.net_io_counters()

current_sent = network.bytes_sent
current_received = network.bytes_recv
current_time_seconds = time.time()

if "previous_network" not in st.session_state:
    st.session_state.previous_network = {
        "sent": current_sent,
        "received": current_received,
        "time": current_time_seconds
    }

previous = st.session_state.previous_network

time_difference = current_time_seconds - previous["time"]

if time_difference > 0:

    upload_speed = (
        current_sent - previous["sent"]
    ) / time_difference / (1024 * 1024)

    download_speed = (
        current_received - previous["received"]
    ) / time_difference / (1024 * 1024)

else:

    upload_speed = 0
    download_speed = 0

st.session_state.previous_network = {
    "sent": current_sent,
    "received": current_received,
    "time": current_time_seconds
}

boot_time = psutil.boot_time()
uptime_seconds = time.time() - boot_time

uptime_hours = int(uptime_seconds // 3600)
uptime_minutes = int((uptime_seconds % 3600) // 60)


# ==========================================
# SAVE HISTORY
# ==========================================

current_time = datetime.now().strftime("%H:%M:%S")

st.session_state.history.append({
    "Time": current_time,
    "CPU": cpu_usage,
    "RAM": ram_usage
})


# Keep only the latest 30 readings

if len(st.session_state.history) > 30:
    st.session_state.history.pop(0)


df = pd.DataFrame(st.session_state.history)

# ==========================================
# SIDEBAR SETTINGS
# ==========================================

st.sidebar.title("⚙️ Monitor Settings")

refresh_interval = st.sidebar.slider(
    "Refresh Interval (seconds)",
    min_value=1,
    max_value=10,
    value=8,
    step=1
)

st.sidebar.subheader("Alert Thresholds")

cpu_threshold = st.sidebar.slider(
    "CPU Warning (%)",
    min_value=50,
    max_value=100,
    value=80,
    step=5
)

ram_threshold = st.sidebar.slider(
    "RAM Warning (%)",
    min_value=50,
    max_value=100,
    value=80,
    step=5
)

disk_threshold = st.sidebar.slider(
    "Disk Warning (%)",
    min_value=50,
    max_value=100,
    value=75,
    step=5
)

st.sidebar.divider()

st.sidebar.info(
    "Adjust the thresholds to control when system alerts are generated."
)
# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<div class="main-title">🖥️ Real-Time System Health Monitor</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Monitor CPU, memory, disk, network activity and system uptime in real time.</div>',
    unsafe_allow_html=True
)


# ==========================================
# MAIN METRICS
# ==========================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🧠 CPU Usage",
        f"{cpu_usage:.1f}%"
    )

with col2:
    st.metric(
        "💾 RAM Usage",
        f"{ram_usage:.1f}%"
    )

with col3:
    st.metric(
        "💽 Disk Usage",
        f"{disk_usage:.1f}%"
    )

with col4:
    st.metric(
        "🌐 Download Speed",
        f"{download_speed:.2f} MB/s"
    )

# ==========================================
# SYSTEM HEALTH SCORE
# ==========================================

health_score = (
    100
    - (cpu_usage * 0.30)
    - (ram_usage * 0.40)
    - (disk_usage * 0.30)
)

health_score = max(0, min(100, health_score))

if health_score >= 80:
    health_status = "🟢 HEALTHY"
elif health_score >= 60:
    health_status = "🟡 WARNING"
else:
    health_status = "🔴 CRITICAL"

st.subheader("🩺 Overall System Health")

health_col1, health_col2 = st.columns([1, 3])

with health_col1:
    st.metric(
        "Health Score",
        f"{health_score:.0f}/100"
    )

with health_col2:
    st.progress(health_score / 100)
    st.write(f"System Status: **{health_status}**")

# ==========================================
# NETWORK
# ==========================================

st.subheader("🌐 Network Activity")

network_col1, network_col2 = st.columns(2)

with network_col1:

    st.metric(
        "📤 Upload Speed",
        f"{upload_speed:.2f} MB/s"
    )

with network_col2:

    st.metric(
        "📥 Download Speed",
        f"{download_speed:.2f} MB/s"
    )

# ==========================================
# SYSTEM INFORMATION
# ==========================================

st.subheader("💻 System Information")

system_col1, system_col2, system_col3 = st.columns(3)

with system_col1:

    st.write("### Operating System")
    st.write(platform.system())

    st.write("### CPU Cores")
    st.write(psutil.cpu_count(logical=False))


with system_col2:

    st.write("### CPU Architecture")
    st.write(platform.machine())

    total_ram_gb = psutil.virtual_memory().total / (1024 ** 3)

    st.write("### Total RAM")
    st.write(f"{total_ram_gb:.2f} GB")


with system_col3:

    total_disk_gb = psutil.disk_usage("/").total / (1024 ** 3)

    st.write("### Total Disk")
    st.write(f"{total_disk_gb:.2f} GB")

    st.write("### Python Version")
    st.write(platform.python_version())


# ==========================================
# SMART ALERT SYSTEM
# ==========================================

st.subheader("🚨 System Alerts")

alerts = []

current_alert_time = datetime.now().strftime("%H:%M:%S")


# CPU Alert
if cpu_usage >= 90:

    alerts.append({
        "Time": current_alert_time,
        "Level": "CRITICAL",
        "Resource": "CPU",
        "Message": f"CPU usage is extremely high ({cpu_usage:.1f}%)."
    })

elif cpu_usage >= cpu_threshold:

    alerts.append({
        "Time": current_alert_time,
        "Level": "WARNING",
        "Resource": "CPU",
        "Message": f"CPU usage is high ({cpu_usage:.1f}%)."
    })


# RAM Alert
if ram_usage >= 90:

    alerts.append({
        "Time": current_alert_time,
        "Level": "CRITICAL",
        "Resource": "RAM",
        "Message": f"RAM usage is extremely high ({ram_usage:.1f}%)."
    })

elif ram_usage >= ram_threshold:

    alerts.append({
        "Time": current_alert_time,
        "Level": "WARNING",
        "Resource": "RAM",
        "Message": f"RAM usage is high ({ram_usage:.1f}%)."
    })


# Disk Alert
if disk_usage >= 90:
    alerts.append({
        "Time": current_alert_time,
        "Level": "CRITICAL",
        "Resource": "Disk",
        "Message": f"Disk usage is extremely high ({disk_usage:.1f}%)."
    })

elif disk_usage >= disk_threshold:
    alerts.append({
        "Time": current_alert_time,
        "Level": "WARNING",
        "Resource": "Disk",
        "Message": f"Disk usage is high ({disk_usage:.1f}%)."
    })

# Display alerts

if alerts:

    alert_df = pd.DataFrame(alerts)

    st.dataframe(
        alert_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "✅ No active alerts. System is healthy."
    )


# ==========================================
# RESOURCE DETAILS
# ==========================================

st.subheader("📊 Current Resource Usage")

detail_col1, detail_col2, detail_col3 = st.columns(3)

with detail_col1:

    st.write("### CPU")

    st.progress(
        min(cpu_usage / 100, 1.0)
    )


with detail_col2:

    st.write("### RAM")

    st.progress(
        min(ram_usage / 100, 1.0)
    )


with detail_col3:

    st.write("### Disk")

    st.progress(
        min(disk_usage / 100, 1.0)
    )


# ==========================================
# LIVE CPU CHART
# ==========================================

st.subheader("📈 CPU Usage History")

cpu_chart = go.Figure()

cpu_chart.add_trace(
    go.Scatter(
        x=df["Time"],
        y=df["CPU"],
        mode="lines+markers",
        name="CPU Usage"
    )
)

cpu_chart.update_layout(
    xaxis_title="Time",
    yaxis_title="CPU Usage (%)",
    yaxis=dict(range=[0, 100]),
    height=350
)

st.plotly_chart(
    cpu_chart,
    use_container_width=True
)


# ==========================================
# LIVE RAM CHART
# ==========================================

st.subheader("📈 RAM Usage History")

ram_chart = go.Figure()

ram_chart.add_trace(
    go.Scatter(
        x=df["Time"],
        y=df["RAM"],
        mode="lines+markers",
        name="RAM Usage"
    )
)

ram_chart.update_layout(
    xaxis_title="Time",
    yaxis_title="RAM Usage (%)",
    yaxis=dict(range=[0, 100]),
    height=350
)

st.plotly_chart(
    ram_chart,
    use_container_width=True
)

# ==========================================
# TOP PROCESSES
# ==========================================

st.subheader("⚙️ Top Running Processes")

processes = []

for process in psutil.process_iter(
    ["pid", "name", "memory_percent", "cpu_percent"]
):
    try:
        info = process.info

        processes.append({
            "PID": info["pid"],
            "Process": info["name"] or "Unknown",
            "CPU (%)": info["cpu_percent"] or 0,
            "RAM (%)": info["memory_percent"] or 0
        })

    except (
        psutil.NoSuchProcess,
        psutil.AccessDenied,
        psutil.ZombieProcess
    ):
        continue


process_df = pd.DataFrame(processes)


if not process_df.empty:

    # Top 5 processes by RAM usage
    top_processes = (
        process_df
        .sort_values("RAM (%)", ascending=False)
        .head(5)
    )

    st.dataframe(
        top_processes,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No process information available.")
# ==========================================
# FOOTER
# ==========================================

st.caption(
    "Real-Time System Health Monitor • "
    "Python + Streamlit + psutil + Plotly"
)


# ==========================================
# AUTO UPDATE
# ==========================================

time.sleep(refresh_interval)
st.rerun()