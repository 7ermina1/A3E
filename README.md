# Project A3E: Automated Agentless Adversarial Emulation

A modular Python-based tool for automated adversarial emulation, designed for offensive security training and thesis research.

## Features
- **Agentless**: No pre-installed agents required on targets.
- **Automated Attack Tree**:
  - **Recon**: Port scanning via Nmap.
  - **Path A (SMB)**: MS17-010 (EternalBlue) exploitation via Metasploit RPC.
  - **Path B (FTP)**: Anonymous FTP authentication checks.
- **Modular**: extensible design for adding new attack vectors.

## Prerequisites
- **OS**: Kali Linux (Recommended) or Linux with Nmap installed.
- **Metasploit**: `msfconsole` and `msfrpcd` must be installed.
- **Python**: 3.x

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Metasploit RPC Server**:
   You must start the MSF RPC daemon before running the tool for exploit functionality.
   ```bash
   msfrpcd -P password -S -f
   ```

## Usage

Run the main tool with a target IP:

```bash
python main.py <TARGET_IP> --msf-pass <YOUR_MSF_PASSWORD> --lhost <YOUR_IP>
```

Example:
```bash
python main.py 192.168.1.105 --msf-pass mypassword --lhost 192.168.1.5
```

## Structure
- `src/`: Core modules (Recon, MSF Client, FTP Client, Engine).
- `config/`: Configuration files.
- `tests/`: Unit tests.

## Disclaimer
For educational and authorized testing purposes only.