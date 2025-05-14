# ⚔️ TzCyberNinja-C2

> A Command-and-Control (C2) payload management framework for **educational and authorized penetration testing** only.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey)
![Target](https://img.shields.io/badge/target-Windows-lightgrey)
![Status](https://img.shields.io/badge/status-Active-brightgreen)

---

## 🚨 Disclaimer

This project is intended **strictly for ethical hacking**, red team simulations, and **educational use**.  
**Do not deploy** this framework against systems you do not own or have explicit permission to test.

---

## 🎯 Features

### 🔍 Runtime Environment Detection

Detects execution in analysis or sandboxed environments using several heuristics:

- 🖥️ **Virtual machine detection** via CPU & RAM size checks
- 🛠️ **Debugger detection** (e.g., OllyDbg, IDA, ProcMon)
- 🧬 **Suspicious DLLs** (commonly found in sandboxes)
- ⏱️ **Runtime duration check** to bypass quick-analysis snapshots

---

### 🧬 Persistence Techniques

Once deployed, the payload attempts to persist using multiple mechanisms:

- 🪟 **Windows Service Installation**  
  Registers itself as a fake "Windows Update" service.

- 🧾 **Registry Run Key**  
  Adds itself to `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`.

- 📁 **Startup Folder Injection**  
  Copies itself as `WindowsUpdate.exe` into the user’s Startup folder.

- ⏰ **Scheduled Task**  
  Creates a logon-triggered task with elevated privileges.

---

## 🛠️ Getting Started

```bash
git clone https://github.com/yourusername/TzCyberNinja-C2.git
cd TzCyberNinja-C2
pip3 install -r requirements.txt







