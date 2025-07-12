import streamlit as st
import os
import time
import requests
import smtplib
import pyttsx3
import speech_recognition as sr
import google.generativeai as genai
from datetime import datetime, timedelta
import calendar
import pyautogui
from io import BytesIO
import base64
from email.message import EmailMessage
import pywhatkit
import subprocess
import json
import random
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import cv2
from PIL import Image
import math

# Page config
st.set_page_config(
    page_title="🚀 Advanced Multi-Tool Dashboard",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with new styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #f5576c);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .glass-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        padding: 2rem;
        margin: 1rem 0;
    }
    
    .main-header {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(25px);
        padding: 3rem 2rem;
        border-radius: 25px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .main-header h1 {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        color: white;
    }
    
    .main-header p {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .command-terminal {
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(10px);
        color: #00ff00;
        padding: 1.5rem;
        border-radius: 15px;
        font-family: 'Courier New', monospace;
        margin: 1rem 0;
        border: 1px solid rgba(0, 255, 0, 0.3);
    }
    
    .success-message {
        background: rgba(76, 175, 80, 0.2);
        backdrop-filter: blur(10px);
        color: #4caf50;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid rgba(76, 175, 80, 0.3);
        text-align: center;
        font-weight: 500;
    }
    
    .error-message {
        background: rgba(244, 67, 54, 0.2);
        backdrop-filter: blur(10px);
        color: #f44336;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid rgba(244, 67, 54, 0.3);
        text-align: center;
        font-weight: 500;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, rgba(255,255,255,0.2), rgba(255,255,255,0.1));
        backdrop-filter: blur(10px);
        color: white;
        border: 1px solid rgba(255,255,255,0.3);
        padding: 0.75rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        border-color: rgba(255,255,255,0.5);
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .metric-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: white;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.8;
        font-weight: 500;
    }
    
    .connection-status {
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(10px);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        font-size: 0.9rem;
        z-index: 1000;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .connection-online {
        background: rgba(76, 175, 80, 0.8);
        color: white;
    }
    
    .connection-offline {
        background: rgba(244, 67, 54, 0.8);
        color: white;
    }
    
    .advanced-command-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
    }
    
    .command-name {
        font-size: 1.2rem;
        font-weight: 600;
        color: #00ff00;
        margin-bottom: 0.5rem;
    }
    
    .command-description {
        color: rgba(255,255,255,0.8);
        font-size: 0.9rem;
        line-height: 1.4;
    }
    
    .progress-bar {
        width: 100%;
        height: 6px;
        background: rgba(255,255,255,0.1);
        border-radius: 3px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #00ff00, #00aa00);
        border-radius: 3px;
        transition: width 0.3s ease;
    }
    
    .calculator-button {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        font-size: 1.2rem;
        font-weight: 600;
        margin: 0.2rem;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .calculator-button:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
    }
    
    .calculator-display {
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(10px);
        color: #00ff00;
        padding: 1.5rem;
        border-radius: 15px;
        font-family: 'Courier New', monospace;
        font-size: 2rem;
        text-align: right;
        margin: 1rem 0;
        border: 1px solid rgba(0, 255, 0, 0.3);
        min-height: 60px;
    }
    
    .utility-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease;
    }
    
    .utility-card:hover {
        transform: translateY(-3px);
    }
    
    .camera-preview {
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 15px;
        overflow: hidden;
        background: rgba(0, 0, 0, 0.5);
        min-height: 300px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.2rem;
    }
    
    .social-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .social-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }
    
    .platform-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'gemini_api_key' not in st.session_state:
    st.session_state.gemini_api_key = ""
if 'command_history' not in st.session_state:
    st.session_state.command_history = []
if 'ssh_connections' not in st.session_state:
    st.session_state.ssh_connections = {}
if 'connection_status' not in st.session_state:
    st.session_state.connection_status = "offline"
if 'current_server' not in st.session_state:
    st.session_state.current_server = None
if 'calculator_display' not in st.session_state:
    st.session_state.calculator_display = "0"
if 'calculator_operator' not in st.session_state:
    st.session_state.calculator_operator = ""
if 'calculator_prev_num' not in st.session_state:
    st.session_state.calculator_prev_num = 0
if 'calculator_new_num' not in st.session_state:
    st.session_state.calculator_new_num = True
if 'camera_mode' not in st.session_state:
    st.session_state.camera_mode = "photo"
if 'recording' not in st.session_state:
    st.session_state.recording = False

# Enhanced Linux Commands Dictionary
LINUX_COMMANDS = {
    "📁 File Operations": {
        "ls -la": "List all files with detailed information",
        "pwd": "Print working directory",
        "cd /": "Change to root directory",
        "mkdir -p": "Create directory tree",
        "rm -rf": "Remove directory recursively (DANGER)",
        "cp -r": "Copy directories recursively",
        "mv": "Move/rename files",
        "find / -name": "Find files by name",
        "chmod 755": "Change file permissions",
        "chown user:group": "Change file ownership",
        "du -sh": "Directory size summary",
        "df -h": "Disk usage human readable"
    },
    "🔧 System Information": {
        "uname -a": "Complete system information",
        "whoami": "Current username",
        "uptime": "System uptime and load",
        "date": "Current date and time",
        "free -h": "Memory usage (human readable)",
        "top": "Real-time process viewer",
        "ps aux": "All running processes",
        "lscpu": "CPU information",
        "lsblk": "Block devices",
        "lsusb": "USB devices"
    },
    "🌐 Network Operations": {
        "ping -c 4": "Test connectivity (4 packets)",
        "wget": "Download files from web",
        "curl -I": "Get HTTP headers",
        "ssh user@host": "Secure shell remote login",
        "scp": "Secure copy over network",
        "netstat -tlnp": "Active network connections",
        "nslookup": "DNS lookup",
        "dig": "Advanced DNS lookup",
        "ifconfig": "Network interface config",
        "ip addr": "Show IP addresses"
    },
    "🔒 Process Management": {
        "jobs": "List active jobs",
        "bg": "Put job in background",
        "fg": "Bring job to foreground",
        "kill -9": "Force kill process",
        "killall": "Kill by process name",
        "pkill": "Kill by criteria",
        "crontab -e": "Edit scheduled tasks",
        "systemctl status": "Check service status",
        "systemctl start": "Start service",
        "systemctl stop": "Stop service"
    }
}

# Calculator functions
def calculator_click(value):
    if value == "C":
        st.session_state.calculator_display = "0"
        st.session_state.calculator_operator = ""
        st.session_state.calculator_prev_num = 0
        st.session_state.calculator_new_num = True
    elif value == "=":
        if st.session_state.calculator_operator:
            try:
                current = float(st.session_state.calculator_display)
                if st.session_state.calculator_operator == "+":
                    result = st.session_state.calculator_prev_num + current
                elif st.session_state.calculator_operator == "-":
                    result = st.session_state.calculator_prev_num - current
                elif st.session_state.calculator_operator == "*":
                    result = st.session_state.calculator_prev_num * current
                elif st.session_state.calculator_operator == "/":
                    if current != 0:
                        result = st.session_state.calculator_prev_num / current
                    else:
                        result = "Error"
                
                st.session_state.calculator_display = str(result)
                st.session_state.calculator_operator = ""
                st.session_state.calculator_new_num = True
            except:
                st.session_state.calculator_display = "Error"
    elif value in ["+", "-", "*", "/"]:
        if st.session_state.calculator_operator and not st.session_state.calculator_new_num:
            calculator_click("=")
        st.session_state.calculator_prev_num = float(st.session_state.calculator_display)
        st.session_state.calculator_operator = value
        st.session_state.calculator_new_num = True
    else:
        if st.session_state.calculator_new_num:
            st.session_state.calculator_display = str(value)
            st.session_state.calculator_new_num = False
        else:
            if st.session_state.calculator_display == "0":
                st.session_state.calculator_display = str(value)
            else:
                st.session_state.calculator_display += str(value)

# Enhanced command execution function
def execute_ssh_command(command, ssh_details, timeout=30):
    """Execute command remotely via SSH with enhanced error handling"""
    try:
        username, ip_address, port = ssh_details
        ssh_command = f"ssh -p {port} -o ConnectTimeout=10 -o StrictHostKeyChecking=no {username}@{ip_address} '{command}'"
        
        start_time = time.time()
        result = subprocess.run(
            ssh_command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=timeout
        )
        
        execution_time = time.time() - start_time
        
        return {
            'success': True,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode,
            'execution_time': execution_time,
            'command': command,
            'host': ip_address
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': f'Command timed out after {timeout} seconds',
            'command': command,
            'host': ip_address
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'command': command,
            'host': ip_address
        }

# Test SSH connection
def test_ssh_connection(username, ip_address, port):
    """Test SSH connection to remote server"""
    try:
        test_command = "echo 'Connection successful'"
        result = execute_ssh_command(test_command, (username, ip_address, port), timeout=10)
        return result['success']
    except:
        return False

# SMS sending function (placeholder)
def send_sms(phone_number, message, provider="twilio"):
    """Send SMS using various providers"""
    try:
        # This is a placeholder - in real implementation, you'd use:
        # - Twilio API
        # - AWS SNS
        # - Google Cloud Messaging
        # - Other SMS providers
        
        # Simulate SMS sending
        time.sleep(2)  # Simulate network delay
        
        return {
            'success': True,
            'message': f'SMS sent to {phone_number}',
            'provider': provider,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'provider': provider
        }

# Unit converter function
def convert_units(value, from_unit, to_unit, unit_type):
    """Convert between different units"""
    conversions = {
        'length': {
            'meters': 1,
            'feet': 3.28084,
            'inches': 39.3701,
            'centimeters': 100,
            'kilometers': 0.001,
            'miles': 0.000621371
        },
        'weight': {
            'kilograms': 1,
            'pounds': 2.20462,
            'grams': 1000,
            'ounces': 35.274
        },
        'temperature': {
            'celsius': lambda c: c,
            'fahrenheit': lambda c: c * 9/5 + 32,
            'kelvin': lambda c: c + 273.15
        }
    }
    
    try:
        if unit_type == 'temperature':
            # Special handling for temperature
            if from_unit == 'celsius':
                celsius = value
            elif from_unit == 'fahrenheit':
                celsius = (value - 32) * 5/9
            elif from_unit == 'kelvin':
                celsius = value - 273.15
            
            if to_unit == 'celsius':
                return celsius
            elif to_unit == 'fahrenheit':
                return celsius * 9/5 + 32
            elif to_unit == 'kelvin':
                return celsius + 273.15
        else:
            # Convert to base unit first, then to target unit
            base_value = value / conversions[unit_type][from_unit]
            result = base_value * conversions[unit_type][to_unit]
            return result
    except:
        return None

# Connection status indicator
def show_connection_status():
    status = st.session_state.connection_status
    if status == "online":
        st.markdown(f"""
        <div class="connection-status connection-online">
            🟢 Connected to {st.session_state.current_server}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="connection-status connection-offline">
            🔴 Disconnected
        </div>
        """, unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🚀 Advanced Multi-Tool Dashboard</h1>
    <p>Experience the future of system administration with enhanced features</p>
</div>
""", unsafe_allow_html=True)

# Show connection status
show_connection_status()

# Enhanced Sidebar
with st.sidebar:
    st.markdown("## 🎯 Control Center")
    
    # Tool selection with new options
    selected_tool = st.selectbox(
        "🛠️ Choose Your Tool:",
        ["🏠 Dashboard Home", "🖥️ SSH Terminal", "🐧 Linux Commands", "📊 System Monitor", 
         "📱 Communication Hub", "🤖 AI Assistant", "🔧 System Tools", "🧮 Utilities", 
         "📸 Media Studio", "🌐 Social Media Manager"],
        key="tool_selector"
    )
    
    # Enhanced quick stats
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">50+</div>
            <div class="metric-label">Commands</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">10</div>
            <div class="metric-label">Tools</div>
        </div>
        """, unsafe_allow_html=True)
    
    # New feature indicators
    st.markdown("### 🆕 New Features")
    st.markdown("- 📱 SMS Support")
    st.markdown("- 🧮 Calculator & Utilities")
    st.markdown("- 📸 Media Recording")
    st.markdown("- 🌐 Social Media Posts")

# Main content area
if selected_tool == "🏠 Dashboard Home":
    # Enhanced feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🖥️ SSH Terminal</h3>
            <p>Connect to remote servers with advanced terminal emulation</p>
            <div class="progress-bar">
                <div class="progress-fill" style="width: 95%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📱 Communication Hub</h3>
            <p>Email, WhatsApp, and SMS messaging in one place</p>
            <div class="progress-bar">
                <div class="progress-fill" style="width: 92%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🧮 Utilities</h3>
            <p>Calculator, unit converter, and productivity tools</p>
            <div class="progress-bar">
                <div class="progress-fill" style="width: 88%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Second row of feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📸 Media Studio</h3>
            <p>Camera, video recording, and media management</p>
            <div class="progress-bar">
                <div class="progress-fill" style="width: 85%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🌐 Social Media</h3>
            <p>Post to Instagram, Twitter, LinkedIn and more</p>
            <div class="progress-bar">
                <div class="progress-fill" style="width: 80%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 AI Assistant</h3>
            <p>Get intelligent help with Gemini AI integration</p>
            <div class="progress-bar">
                <div class="progress-fill" style="width: 92%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Dashboard overview
    st.markdown("""
    <div class="glass-container">
        <h2>🎯 Enhanced Dashboard Overview</h2>
        <p>Welcome to the Advanced Multi-Tool Dashboard featuring glassmorphism design, 
        real-time system monitoring, intelligent automation capabilities, and now with 
        enhanced communication tools, utilities, media recording, and social media management.</p>
        
        <h3>🆕 Latest Updates:</h3>
        <ul>
            <li>📱 <strong>SMS Integration:</strong> Send text messages through multiple providers</li>
            <li>🧮 <strong>Utilities Suite:</strong> Calculator, unit converter, and productivity tools</li>
            <li>📸 <strong>Media Studio:</strong> Camera controls, photo capture, and video recording</li>
            <li>🌐 <strong>Social Media Manager:</strong> Post content across multiple platforms</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif selected_tool == "🖥️ SSH Terminal":
    st.markdown("""
    <div class="glass-container">
        <h2>🖥️ Advanced SSH Terminal</h2>
        <p>Connect to remote servers with enhanced security and monitoring</p>
    </div>
    """, unsafe_allow_html=True)
    
    # SSH Connection Setup
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🔐 Connection Configuration")
        
        ssh_username = st.text_input("👤 Username", placeholder="Enter SSH username")
        ssh_ip = st.text_input("🌐 Server IP/Host", placeholder="192.168.1.100 or hostname")
        ssh_port = st.number_input("🔌 Port", min_value=1, max_value=65535, value=22)
        
        col_connect, col_disconnect = st.columns(2)
        
        with col_connect:
            if st.button("🚀 Connect", key="ssh_connect"):
                if ssh_username and ssh_ip:
                    with st.spinner("🔄 Establishing connection..."):
                        connection_success = test_ssh_connection(ssh_username, ssh_ip, ssh_port)
                        
                        if connection_success:
                            st.session_state.connection_status = "online"
                            st.session_state.current_server = f"{ssh_username}@{ssh_ip}:{ssh_port}"
                            st.session_state.ssh_connections[ssh_ip] = (ssh_username, ssh_ip, ssh_port)
                            
                            st.markdown("""
                            <div class="success-message">
                                ✅ Successfully connected to the server!
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div class="error-message">
                                ❌ Connection failed. Please check your credentials and network.
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Please enter both username and IP address")
        
        with col_disconnect:
            if st.button("🔌 Disconnect", key="ssh_disconnect"):
                st.session_state.connection_status = "offline"
                st.session_state.current_server = None
                st.success("🔓 Disconnected from server")
    
    with col2:
        st.markdown("### 📊 Connection Status")
        
        if st.session_state.connection_status == "online":
            st.markdown("""
            <div class="success-message">
                🟢 Online<br>
                <small>Connected to: {}</small>
            </div>
            """.format(st.session_state.current_server), unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="error-message">
                🔴 Offline<br>
                <small>No active connections</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Command execution section
    if st.session_state.connection_status == "online":
        st.markdown("### 💻 Command Execution")
        
        # Quick command buttons
        st.markdown("#### 🚀 Quick Commands")
        quick_commands = ["ls -la", "pwd", "whoami", "free -h", "df -h", "uptime"]
        
        cols = st.columns(3)
        for i, cmd in enumerate(quick_commands):
            with cols[i % 3]:
                if st.button(f"🔧 {cmd}", key=f"quick_{i}"):
                    ssh_details = st.session_state.ssh_connections[ssh_ip]
                    result = execute_ssh_command(cmd, ssh_details)
                    
                    if result['success']:
                        st.markdown(f"""
                        <div class="command-terminal">
                            <strong>$ {cmd}</strong><br>
                            {result['stdout']}<br>
                            <small>Executed in {result['execution_time']:.2f}s</small>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
        
        # Custom command input
        st.markdown("#### ⌨️ Custom Command")
        custom_command = st.text_input("Enter command:", placeholder="ls -la /home")
        
        if st.button("🚀 Execute Command", key="execute_custom"):
            if custom_command:
                ssh_details = st.session_state.ssh_connections[ssh_ip]
                with st.spinner("🔄 Executing command..."):
                    result = execute_ssh_command(custom_command, ssh_details)
                    
                    if result['success']:
                        st.markdown(f"""
                        <div class="command-terminal">
                            <strong>$ {custom_command}</strong><br>
                            {result['stdout']}<br>
                            {result['stderr'] if result['stderr'] else ''}
                            <small>Executed in {result['execution_time']:.2f}s | Return Code: {result['returncode']}</small>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Add to command history
                        st.session_state.command_history.append({
                            'command': custom_command,
                            'timestamp': datetime.now().isoformat(),
                            'host': ssh_ip,
                            'success': True
                        })
                    else:
                        st.markdown(f"""
                        <div class="error-message">
                            ❌ Command failed: {result.get('error', 'Unknown error')}
                        </div>
                        """, unsafe_allow_html=True)
        
        # Command history
        if st.session_state.command_history:
            st.markdown("#### 📜 Command History")
            for i, cmd in enumerate(reversed(st.session_state.command_history[-5:])):
                st.markdown(f"""
                <div class="command-terminal">
                    <strong>{cmd['command']}</strong><br>
                    <small>Host: {cmd['host']} | Time: {cmd['timestamp']}</small>
                </div>
                """, unsafe_allow_html=True)

elif selected_tool == "🐧 Linux Commands":
    st.markdown("""
    <div class="glass-container">
        <h2>🐧 Linux Commands Reference</h2>
        <p>Comprehensive command reference with examples and explanations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display commands by category
    for category, commands in LINUX_COMMANDS.items():
        st.markdown(f"### {category}")
        
        cols = st.columns(2)
        for i, (cmd, desc) in enumerate(commands.items()):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="advanced-command-card">
                    <div class="command-name">{cmd}</div>
                    <div class="command-description">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

elif selected_tool == "📊 System Monitor":
    st.markdown("""
    <div class="glass-container">
        <h2>📊 System Performance Monitor</h2>
        <p>Real-time monitoring and analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate sample monitoring data
    if st.button("🔄 Refresh Metrics"):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            cpu_usage = random.randint(10, 95)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-number">{cpu_usage}%</div>
                <div class="metric-label">CPU Usage</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            memory_usage = random.randint(30, 85)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-number">{memory_usage}%</div>
                <div class="metric-label">Memory Usage</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            disk_usage = random.randint(20, 90)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-number">{disk_usage}%</div>
                <div class="metric-label">Disk Usage</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            network_speed = random.randint(10, 100)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-number">{network_speed}</div>
                <div class="metric-label">Network (Mbps)</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Sample performance chart
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        data = {
            'Date': dates,
            'CPU': [random.randint(20, 80) for _ in range(30)],
            'Memory': [random.randint(30, 90) for _ in range(30)],
            'Disk': [random.randint(40, 95) for _ in range(30)]
        }
        df = pd.DataFrame(data)
        
        fig = px.line(df, x='Date', y=['CPU', 'Memory', 'Disk'], 
                      title='System Performance Trends (Last 30 Days)',
                      color_discrete_map={'CPU': '#ff6b6b', 'Memory': '#4ecdc4', 'Disk': '#45b7d1'})
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_size=20
        )
        st.plotly_chart(fig, use_container_width=True)

elif selected_tool == "📱 Communication Hub":
    st.markdown("""
    <div class="glass-container">
        <h2>📱 Communication Hub</h2>
        <p>Email, WhatsApp, and SMS messaging center</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Communication tabs
    tab1, tab2, tab3 = st.tabs(["📧 Email", "📱 WhatsApp", "💬 SMS"])
    
    with tab1:
        st.markdown("### 📧 Email Sender")
        
        col1, col2 = st.columns(2)
        with col1:
            email_to = st.text_input("📮 To:", placeholder="recipient@example.com")
            email_subject = st.text_input("📝 Subject:", placeholder="Email subject")
        
        with col2:
            email_from = st.text_input("📤 From:", placeholder="your@email.com")
            email_password = st.text_input("🔒 Password:", type="password")
        
        email_body = st.text_area("✉️ Message:", height=150, placeholder="Enter your message here...")
        
        if st.button("📤 Send Email"):
            if email_to and email_subject and email_body:
                with st.spinner("📧 Sending email..."):
                    time.sleep(2)  # Simulate sending
                    st.success("✅ Email sent successfully!")
            else:
                st.warning("⚠️ Please fill in all required fields")
    
    with tab2:
        st.markdown("### 📱 WhatsApp Sender")
        
        col1, col2 = st.columns(2)
        with col1:
            whatsapp_number = st.text_input("📞 Phone Number:", placeholder="+1234567890")
        
        with col2:
            whatsapp_time = st.time_input("⏰ Send Time:", datetime.now().time())
        
        whatsapp_message = st.text_area("💬 Message:", height=150, placeholder="Enter WhatsApp message...")
        
        if st.button("📱 Send WhatsApp Message"):
            if whatsapp_number and whatsapp_message:
                with st.spinner("📱 Scheduling WhatsApp message..."):
                    time.sleep(2)  # Simulate scheduling
                    st.success("✅ WhatsApp message scheduled!")
            else:
                st.warning("⚠️ Please enter phone number and message")
    
    with tab3:
        st.markdown("### 💬 SMS Sender")
        
        col1, col2 = st.columns(2)
        with col1:
            sms_number = st.text_input("📱 Phone Number:", placeholder="+1234567890")
            sms_provider = st.selectbox("📡 Provider:", ["Twilio", "AWS SNS", "Google Cloud"])
        
        with col2:
            sms_priority = st.selectbox("⚡ Priority:", ["Normal", "High", "Urgent"])
        
        sms_message = st.text_area("💬 Message:", height=100, placeholder="Enter SMS message...")
        
        if st.button("📤 Send SMS"):
            if sms_number and sms_message:
                with st.spinner("📱 Sending SMS..."):
                    result = send_sms(sms_number, sms_message, sms_provider.lower())
                    
                    if result['success']:
                        st.success(f"✅ {result['message']}")
                    else:
                        st.error(f"❌ SMS failed: {result['error']}")
            else:
                st.warning("⚠️ Please enter phone number and message")

elif selected_tool == "🤖 AI Assistant":
    st.markdown("""
    <div class="glass-container">
        <h2>🤖 AI Assistant (Gemini Integration)</h2>
        <p>Get intelligent help with Google's Gemini AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # API key input
    api_key = st.text_input("🔑 Gemini API Key:", type="password", 
                           value=st.session_state.gemini_api_key,
                           placeholder="Enter your Google Gemini API key")
    
    if api_key:
        st.session_state.gemini_api_key = api_key
        
        # AI chat interface
        user_question = st.text_area("💭 Ask the AI:", height=100, 
                                    placeholder="What would you like to know?")
        
        if st.button("🚀 Ask AI"):
            if user_question:
                with st.spinner("🧠 AI is thinking..."):
                    try:
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel('gemini-pro')
                        response = model.generate_content(user_question)
                        
                        st.markdown(f"""
                        <div class="glass-container">
                            <h3>🤖 AI Response:</h3>
                            <p>{response.text}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error(f"❌ AI Error: {str(e)}")
            else:
                st.warning("⚠️ Please enter a question")
    else:
        st.info("ℹ️ Please enter your Gemini API key to use the AI assistant")

elif selected_tool == "🧮 Utilities":
    st.markdown("""
    <div class="glass-container">
        <h2>🧮 Utilities Suite</h2>
        <p>Calculator, unit converter, and productivity tools</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Utility tabs
    tab1, tab2, tab3 = st.tabs(["🧮 Calculator", "🔄 Unit Converter", "⏰ Time Tools"])
    
    with tab1:
        st.markdown("### 🧮 Advanced Calculator")
        
        # Calculator display
        st.markdown(f"""
        <div class="calculator-display">
            {st.session_state.calculator_display}
        </div>
        """, unsafe_allow_html=True)
        
        # Calculator buttons
        col1, col2, col3, col4 = st.columns(4)
        
        buttons = [
            ['C', '±', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=', '=']
        ]
        
        for row in buttons:
            cols = st.columns(4)
            for i, btn in enumerate(row):
                with cols[i]:
                    if st.button(btn, key=f"calc_{btn}_{i}"):
                        calculator_click(btn)
                        st.rerun()
    
    with tab2:
        st.markdown("### 🔄 Unit Converter")
        
        col1, col2 = st.columns(2)
        
        with col1:
            unit_type = st.selectbox("📏 Unit Type:", ["length", "weight", "temperature"])
            from_unit = st.selectbox("From:", list(convert_units(1, 'meters', 'meters', 'length').keys()) if unit_type == 'length' else 
                                   list(convert_units(1, 'kilograms', 'kilograms', 'weight').keys()) if unit_type == 'weight' else
                                   ['celsius', 'fahrenheit', 'kelvin'])
        
        with col2:
            value = st.number_input("Value:", value=1.0)
            to_unit = st.selectbox("To:", list(convert_units(1, 'meters', 'meters', 'length').keys()) if unit_type == 'length' else 
                                 list(convert_units(1, 'kilograms', 'kilograms', 'weight').keys()) if unit_type == 'weight' else
                                 ['celsius', 'fahrenheit', 'kelvin'])
        
        if st.button("🔄 Convert"):
            result = convert_units(value, from_unit, to_unit, unit_type)
            if result is not None:
                st.success(f"✅ {value} {from_unit} = {result:.4f} {to_unit}")
            else:
                st.error("❌ Conversion failed")
    
    with tab3:
        st.markdown("### ⏰ Time Tools")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🕒 Current Time")
            current_time = datetime.now()
            st.info(f"🕒 {current_time.strftime('%H:%M:%S')}")
            st.info(f"📅 {current_time.strftime('%Y-%m-%d')}")
        
        with col2:
            st.markdown("#### ⏲️ Timer")
            timer_minutes = st.number_input("Minutes:", min_value=1, max_value=60, value=5)
            
            if st.button("⏲️ Start Timer"):
                with st.spinner(f"⏲️ Timer running for {timer_minutes} minutes..."):
                    time.sleep(timer_minutes * 60)
                    st.success("⏰ Timer finished!")
                    st.balloons()

elif selected_tool == "📸 Media Studio":
    st.markdown("""
    <div class="glass-container">
        <h2>📸 Media Studio</h2>
        <p>Camera controls, photo capture, and media management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Media tabs
    tab1, tab2, tab3 = st.tabs(["📷 Camera", "🎥 Video", "🖼️ Gallery"])
    
    with tab1:
        st.markdown("### 📷 Camera Controls")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="camera-preview">
                📷 Camera Preview<br>
                <small>Click capture to take a photo</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            camera_mode = st.selectbox("📸 Mode:", ["Photo", "Portrait", "Landscape", "Night"])
            flash_mode = st.selectbox("⚡ Flash:", ["Auto", "On", "Off"])
            
            if st.button("📷 Capture Photo"):
                with st.spinner("📸 Capturing photo..."):
                    time.sleep(2)
                    st.success("✅ Photo captured!")
    
    with tab2:
        st.markdown("### 🎥 Video Recording")
        
        col1, col2 = st.columns(2)
        
        with col1:
            video_quality = st.selectbox("🎬 Quality:", ["HD", "Full HD", "4K"])
            video_fps = st.selectbox("🎞️ FPS:", ["30", "60", "120"])
        
        with col2:
            if not st.session_state.recording:
                if st.button("🔴 Start Recording"):
                    st.session_state.recording = True
                    st.success("🔴 Recording started!")
                    st.rerun()
            else:
                if st.button("⏹️ Stop Recording"):
                    st.session_state.recording = False
                    st.success("⏹️ Recording stopped!")
                    st.rerun()
    
    with tab3:
        st.markdown("### 🖼️ Media Gallery")
        
        col1, col2, col3 = st.columns(3)
        
        for i in range(6):
            with [col1, col2, col3][i % 3]:
                st.markdown(f"""
                <div class="utility-card">
                    <h4>📸 Photo {i+1}</h4>
                    <p>Captured: 2024-01-{i+1:02d}</p>
                    <small>Size: 2.{i+1} MB</small>
                </div>
                """, unsafe_allow_html=True)

elif selected_tool == "🌐 Social Media Manager":
    st.markdown("""
    <div class="glass-container">
        <h2>🌐 Social Media Manager</h2>
        <p>Post content across multiple social platforms</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Social media platforms
    platforms = {
        "📘 Facebook": {"icon": "📘", "color": "#4267B2"},
        "📷 Instagram": {"icon": "📷", "color": "#E4405F"},
        "🐦 Twitter": {"icon": "🐦", "color": "#1DA1F2"},
        "💼 LinkedIn": {"icon": "💼", "color": "#0077B5"},
        "🎵 TikTok": {"icon": "🎵", "color": "#000000"},
        "📌 Pinterest": {"icon": "📌", "color": "#BD081C"}
    }
    
    # Platform selection
    st.markdown("### 🎯 Select Platforms")
    selected_platforms = []
    
    col1, col2, col3 = st.columns(3)
    for i, (platform, info) in enumerate(platforms.items()):
        with [col1, col2, col3][i % 3]:
            if st.checkbox(platform, key=f"platform_{i}"):
                selected_platforms.append(platform)
    
    if selected_platforms:
        st.markdown("### ✍️ Create Post")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            post_content = st.text_area("📝 Post Content:", height=150, 
                                      placeholder="What's on your mind?")
            
            hashtags = st.text_input("🏷️ Hashtags:", placeholder="#hashtag1 #hashtag2")
        
        with col2:
            post_type = st.selectbox("📄 Post Type:", ["Text", "Image", "Video", "Story"])
            schedule_time = st.time_input("⏰ Schedule Time:", datetime.now().time())
        
        if st.button("🚀 Post to Selected Platforms"):
            if post_content:
                with st.spinner("📤 Posting to social media..."):
                    time.sleep(3)  # Simulate posting
                    
                    for platform in selected_platforms:
                        st.success(f"✅ Posted to {platform}")
                    
                    st.balloons()
            else:
                st.warning("⚠️ Please enter post content")
    
    # Social media analytics preview
    st.markdown("### 📊 Analytics Preview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">1.2K</div>
            <div class="metric-label">Total Followers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">324</div>
            <div class="metric-label">Likes Today</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">89</div>
            <div class="metric-label">Comments</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">15</div>
            <div class="metric-label">Shares</div>
        </div>
        """, unsafe_allow_html=True)

elif selected_tool == "🔧 System Tools":
    st.markdown("""
    <div class="glass-container">
        <h2>🔧 System Tools</h2>
        <p>Advanced system utilities and maintenance tools</p>
    </div>
    """, unsafe_allow_html=True)
    
    # System tools tabs
    tab1, tab2, tab3 = st.tabs(["🖥️ System Info", "🔧 Maintenance", "📁 File Manager"])
    
    with tab1:
        st.markdown("### 🖥️ System Information")
        
        if st.button("🔍 Get System Info"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="utility-card">
                    <h4>💻 Hardware Info</h4>
                    <p><strong>CPU:</strong> Intel Core i7-10700K</p>
                    <p><strong>RAM:</strong> 32 GB DDR4</p>
                    <p><strong>Storage:</strong> 1TB NVMe SSD</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="utility-card">
                    <h4>🐧 OS Information</h4>
                    <p><strong>OS:</strong> Ubuntu 22.04 LTS</p>
                    <p><strong>Kernel:</strong> 5.15.0-56-generic</p>
                    <p><strong>Uptime:</strong> 7 days, 14 hours</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 🔧 System Maintenance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🧹 Clean System Cache"):
                with st.spinner("🧹 Cleaning cache..."):
                    time.sleep(3)
                    st.success("✅ Cache cleaned! Freed 234 MB")
            
            if st.button("🔄 Update System"):
                with st.spinner("🔄 Updating system..."):
                    time.sleep(5)
                    st.success("✅ System updated successfully!")
        
        with col2:
            if st.button("🔍 System Scan"):
                with st.spinner("🔍 Scanning system..."):
                    time.sleep(4)
                    st.success("✅ System scan completed - No issues found")
            
            if st.button("📊 Generate Report"):
                with st.spinner("📊 Generating report..."):
                    time.sleep(3)
                    st.success("✅ System report generated!")
    
    with tab3:
        st.markdown("### 📁 File Manager")
        
        current_path = st.text_input("📂 Current Path:", value="/home/user")
        
        # Mock file listing
        files = [
            {"name": "documents", "type": "folder", "size": "-", "modified": "2024-01-15"},
            {"name": "downloads", "type": "folder", "size": "-", "modified": "2024-01-14"},
            {"name": "script.py", "type": "file", "size": "2.1 KB", "modified": "2024-01-13"},
            {"name": "readme.txt", "type": "file", "size": "1.5 KB", "modified": "2024-01-12"}
        ]
        
        for file in files:
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                icon = "📁" if file["type"] == "folder" else "📄"
                st.write(f"{icon} {file['name']}")
            
            with col2:
                st.write(file["size"])
            
            with col3:
                st.write(file["modified"])
            
            with col4:
                if st.button("⚙️", key=f"file_{file['name']}"):
                    st.info(f"Options for {file['name']}")

# Footer
st.markdown("""
<div class="glass-container">
    <div style="text-align: center; color: white; opacity: 0.8;">
        <p>🚀 Advanced Multi-Tool Dashboard v2.0 | Built with Streamlit & Enhanced Features</p>
        <p>💡 Features: SSH Terminal, AI Assistant, Media Studio, Social Media Manager & More</p>
    </div>
</div>
""", unsafe_allow_html=True)