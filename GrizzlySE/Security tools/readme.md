# Grizzly Security Scan (GSS)

**Lightweight Cybersecurity Audit Tool**  
Built by **Grizzly System Engineering** – Montana-based IT solutions from East Helena.

![Grizzly Logo](/grizzly-logo.png) 

Grizzly Security Scan is a simple, ethical, command-line tool for performing quick, non-intrusive security audits on your own networks or devices. It uses Nmap to identify open ports, detect services/versions, run safe vulnerability scripts, and provide clear risk flags + recommendations.

Perfect for:
- Home users checking their router/Wi-Fi security
- Small businesses in Helena and across Montana auditing basic exposures
- IT pros wanting a fast starting point before deeper pentesting

**Important**: This tool is for **authorized use only**. Always obtain explicit written permission before scanning any network that is not yours.

## Features

- Scans single IPs, ranges (e.g., 192.168.1.0/24), or hostnames
- Detects open ports, service versions, and runs safe NSE vuln scripts
- Simple risk scoring (Low/Medium/High) with explanations
- Colored console output (when colorama is installed)
- Generates timestamped text reports
- Built-in dependency checker with friendly installation instructions
- Montana-focused recommendations (e.g., rural network hardening tips)

## Requirements

- Python 3.8+
- Nmap[](https://nmap.org/download.html) – must be installed and in your PATH
- Python packages: `python-nmap`, `colorama` (optional but recommended)

## Installation

1. **Install Nmap**  
   - Windows: Download the installer from https://nmap.org/download.html  
     → Include Npcap and check "Add to PATH" during setup  
   - Linux/macOS: `sudo apt install nmap` or `brew install nmap`

2. **Install Python dependencies**  
   Open Command Prompt (Windows) or Terminal (macOS/Linux) and run:pip install python-nmap coloramatext3. **Get the tool**  
Option 1: Clone the repo (if you have Git installed)git clone https://github.com/[your-username]/grizzly-security-scan.git
cd grizzly-security-scantextOption 2: Download `grizzly_scan.py` directly from this repository and save it to any folder.

## Usage

Open Command Prompt (Windows: search "cmd" in Start menu) or Terminal, navigate to the folder containing the script, and run:python grizzly_scan.py <target>textOn Windows, right-click Command Prompt → "Run as administrator" for the most complete scan results.

Examples:python grizzly_scan.py 192.168.1.1              # Single device
python grizzly_scan.py 192.168.30.0/24          # Your local subnet
python grizzly_scan.py myrouter.local           # Hostnametext- The tool checks dependencies first and gives instructions if anything is missing.
- A report is automatically saved as `gss_report_<target>_<date>_<time>.txt`

## Example Output=== Grizzly Security Scan (GSS) ===
Lightweight Cybersecurity Audit Tool - Grizzly System Engineering
WARNING: Only scan networks/IPs you OWN or have WRITTEN PERMISSION for![✔] Dependencies OK. Starting scan...[*] Starting scan on 192.168.30.56 at 2026-02-19 09:12:00...
Host: 192.168.30.56 (Unknown)
Status: up
Port 22/tcp: ssh OpenSSH 8.9 | Risk: High - Potential exposure
ssh-hostkey: ...
Port 80/tcp: http Apache httpd 2.4.52 | Risk: Medium - Check web vulnsRecommendations:
Close unnecessary ports (especially RDP 3389, SMB 445 if not needed).
...
Report saved: gss_report_192.168.30.56_20260219_091200.txttext## Legal & Ethical Use

- **Do not** scan networks without explicit written permission.
- This tool performs only safe, non-destructive checks.
- For full penetration testing, vulnerability remediation, or enterprise-grade hardening, contact Grizzly System Engineering.

## About Grizzly System Engineering

Home-based in **East Helena, Montana**, we provide reliable IT solutions statewide:  
- Custom PC & server builds  
- Secure network setup (including Starlink)  
- Cybersecurity audits & pentesting  
- Computer repair, data recovery, custom coding & automation  

**Website**: https://grizzlyse.com  
**Email**: info@grizzlyse.com  
**Phone/Text**: (406) 439-8127  

Ready to grizzly-proof your tech? Get in touch — we serve Helena and all of Montana.

## License

MIT License – feel free to use, modify, and distribute.  
Attribution appreciated: "Built with help from Grizzly System Engineering".

Made with 🐻 in Montana.
