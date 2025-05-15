# ⚔️ TzCyberNinja-C2

<div align="center">
  <img src="https://github.com/user-attachments/assets/2c9d0c9a-5bb6-4bbc-b3d6-3bd3a0d2afb2" alt="TzCyberNinja Logo" width="400"/>
  
  [![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
  [![Platform](https://img.shields.io/badge/platform-Linux-lightgrey)](https://www.linux.org)
  [![Target](https://img.shields.io/badge/target-Windows-lightgrey)](https://www.microsoft.com/windows)
  [![Status](https://img.shields.io/badge/status-Active-brightgreen)](https://github.com/AuxGrep/TzCyberNinja-C2)
  [![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org)
  [![Security](https://img.shields.io/badge/Security-Advanced-red)](SECURITY.md)
</div>

> A sophisticated Command-and-Control (C2) payload management framework designed for **educational purposes and authorized penetration testing** only. Built with advanced evasion techniques and modular architecture.

## 📋 Table of Contents
- [Disclaimer](#-disclaimer)
- [Features](#-features)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [Security](#-security)
- [Contributing](#-contributing)

## 🚨 Disclaimer

This project is intended **strictly for ethical hacking**, red team simulations, and **educational use**.  
**Do not deploy** this framework against systems you do not own or have explicit permission to test.

### Legal Notice
- ⚖️ **Compliance**: Ensure compliance with local and international laws
- 🔒 **Authorization**: Always obtain proper authorization before testing
- 📝 **Documentation**: Maintain detailed records of all testing activities
- 🛡️ **Responsibility**: Use responsibly and ethically

## 🎯 Features

### 🔍 Advanced Runtime Environment Detection

Sophisticated detection mechanisms to identify and evade analysis environments:

- 🖥️ **Virtual Machine Detection**
  - CPU architecture analysis
  - RAM size verification
  - Hardware fingerprinting
  - Hypervisor presence checks

- 🛠️ **Debugger Detection**
  - Anti-debugging techniques
  - Process monitoring evasion
  - Memory analysis protection
  - Common debugger signatures

- 🧬 **Sandbox Detection**
  - Suspicious DLL analysis
  - System behavior monitoring
  - Network traffic patterns
  - Resource usage profiling

- ⏱️ **Timing Analysis**
  - Runtime duration verification
  - System clock manipulation detection
  - Quick-analysis snapshot bypass
  - Time-based execution control

### 🧬 Advanced Persistence Techniques

Multiple persistence mechanisms with fallback options:

- 🪟 **Windows Service Integration**
  - Service registration as "Windows Update"
  - Automatic recovery options
  - Service dependency management
  - Privilege escalation handling

- 🧾 **Registry Manipulation**
  - Multiple registry key locations
  - Run key persistence
  - Service configuration
  - Startup program registration

- 📁 **File System Persistence**
  - Startup folder injection
  - System directory placement
  - File attribute modification
  - Alternate data streams

- ⏰ **Task Scheduler Integration**
  - Logon-triggered tasks
  - Elevated privilege execution
  - Task persistence
  - Recovery mechanisms

### 🔐 Security Features

- 🔒 **Encryption**
  - End-to-end encryption
  - Secure key exchange
  - Data obfuscation
  - Anti-tampering protection

- 🌐 **Network Security**
  - Encrypted communication
  - Protocol obfuscation
  - Traffic analysis evasion
  - Connection resilience

## 🛠️ Getting Started

### Prerequisites
- Python 3.8 or higher
- Linux-based operating system
- Administrative privileges
- Network access

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/TzCyberNinja-C2.git

# Navigate to project directory
cd TzCyberNinja-C2

# Install dependencies
pip3 install -r requirements.txt

# Verify installation
python3 --version
pip3 list | grep -E "required-package-1|required-package-2"

# install Mingw-w4
sudo apt update
sudo apt install mingw-w64
```

### Basic Usage
```bash
# Start the C2 server
python3 server2.py

# Build payload
python3 buildPayload.py
```

## 📚 Documentation

For detailed documentation and usage instructions, visit our [Wiki](https://github.com/AuxGrep/TzCyberNinja-C2/wiki/TzCyberNinja%E2%80%90C2).

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <sub>Built with ❤️ by AuxGrep</sub>
  <br>
  <sub>For support, please open an issue on GitHub</sub>
</div>



