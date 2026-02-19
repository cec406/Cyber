# Apache Tomcat Breaker

**Lightweight Tomcat /manager/html Credential Scanner**  
Built by **Grizzly System Engineering** – East Helena, Montana

A command-line tool that:
- Scans for Apache Tomcat instances using Nmap (ports 80, 8080, 8443)
- Attempts credential brute-force against the Tomcat Manager login (/manager/html) using Hydra
- Supports separate username/password wordlists or combined credential lists

**Critical Legal & Ethical Warning**  
This tool is **STRICTLY for authorized penetration testing only**.  
You **must** have **explicit written permission** from the system owner before scanning or attempting credential testing on any network, device, or service that is not 100% yours.  
Unauthorized use violates U.S. federal law (CFAA) and can result in severe penalties.  
Use **only** in controlled lab environments, CTF challenges, or approved client pentest engagements.

## Features
- Targeted Nmap service/version detection for Tomcat  
- Hydra brute-force on /manager/html endpoint  
- Supports:
  - Separate username (-L) and password (-P) wordlists
  - Combined username:password credential lists (-C)
- Color-coded, timestamped console output  
- Custom ASCII art title with cat (terminal width adaptive)  
- Built-in argument validation and error handling

## Requirements
- **Python 3.8+**  
- **Nmap** installed and in PATH[](https://nmap.org/download.html)  
- **Hydra** installed and in PATH[](https://github.com/vanhauser-thc/thc-hydra)  
  - Kali Linux: pre-installed  
  - Windows: via WSL, Cygwin, or pre-built binaries  
- Wordlists (e.g., rockyou.txt, SecLists, custom combos)

## Installation & Setup

1. **Clone or download**
git clone https://github.com/cec406/Cyber/GrizzlySE/SecurityTools/Apache_Breaker.git

cd Apache_Breaker
text2. **Prepare wordlists** (place in same folder or use full paths)  
- Username list: `users.txt`  
- Password list: `passwords.txt` (rockyou.txt is a good start)  
- Combo list: `combos.txt` (format: `username:password` per line)

3. **Run the tool**  
Examples:

```bash
# Separate username + password lists
python apache_breaker.py 192.168.56.0/24 -L users.txt -P passwords.txt

# Combined credential list (faster/more efficient)
python apache_breaker.py 192.168.56.101 -C combos.txt

# Force HTTPS protocol
python apache_breaker.py 10.10.10.10 -C combos.txt -p https
Windows one-click option:
Create run.bat in the folder:
text@echo off
cd /d "%~dp0"
python apache_tomcat_breaker.py %*
pause
Double-click or run: run.bat 192.168.1.0/24 -C combos.txt
Important Notes

Run as administrator/root — Nmap and Hydra require elevated privileges for full scans.
Performance — Small wordlists = fast tests; large lists (full rockyou) = longer runtime.
Limitations — Assumes default /manager/html exposure; modern Tomcat often has protections (locking, IP restrictions).
Output — Console only (redirect to file if needed: > report.txt)

About Grizzly System Engineering
Home-based in East Helena, Montana, we provide reliable IT solutions statewide:

Custom PC & server builds
Secure network setup (including Starlink)
Cybersecurity audits & penetration testing
Computer repair, data recovery, digital forensics
Custom applications, automation & scripting

Website: https://grizzlyse.com
Email: info@grizzlyse.com
Phone/Text: (406) 439-8127
Need professional Tomcat hardening, full pentest services, or secure application deployment? Get in touch — we serve Helena, East Helena, and all of Montana.
Made with 🐻 in the Montana mountains.
License: For personal/authorized lab use only. No redistribution without permission.
