# Grizzly Password Checker (GUI)

**Lightweight Desktop Password Strength & Leak Checker**  
Built by **Grizzly System Engineering** – East Helena, Montana

A simple, 100% local, offline GUI tool that helps users check if a password is weak, common, or appears in known leaked lists — without ever sending data over the internet.

Perfect for:
- Home users testing passwords during setup or education
- Small businesses in Helena & Montana showing employees password risks
- IT pros demonstrating weak/reused password dangers before recommending better practices

**Critical Warnings**  
- **Educational/testing use only** — NEVER enter real, active passwords (even locally).  
- Use a password manager (Bitwarden, 1Password, etc.) for actual secrets.  
- This tool does **not** guarantee security — it’s an awareness tool, not a full security solution.

## Features
- Secure masked password input field  
- Checks against a local common/leaked passwords list (top 1M recommended)  
- Basic strength scoring: length, uppercase/lowercase, numbers, special characters  
- Color-coded results (Strong / Moderate / Weak / DANGEROUS)  
- Lists specific issues (e.g., "No numbers", "Too short")  
- "Generate Strong Password" button for quick random suggestions  
- Built with Python + Tkinter (no extra installs needed beyond Python itself)

## Requirements
- Python 3.8+ (widely available on Windows, macOS, Linux)  
- Tkinter (included with Python on Windows/macOS; on Linux may need `sudo apt install python3-tk`)  
- A common passwords wordlist file named `common_passwords.txt` in the same folder

## Installation & Setup

1. **Download the tool**  
   Clone the repo or download just the password-checker folder:
git clone https://github.com/cec406/grizzly-tools.git
cd grizzly-tools/password-checker
text2. **Add a common passwords list** (required for leak detection)  
Download one of these free, high-quality lists and save it as `common_passwords.txt` in the same folder as the script:
- **Recommended (top 1 million)**:  
  https://github.com/danielmiessler/SecLists/raw/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt  
- Smaller/fast option (top 10k):  
  https://github.com/danielmiessler/SecLists/raw/master/Passwords/Common-Credentials/10k-most-common.txt  

The tool will automatically look for `common_passwords.txt` (or a few fallback names) in the same folder.

3. **Run the tool**  
Open Command Prompt (Windows) or Terminal, navigate to the folder, and run:
python grizzly_password_checker_gui.py
text**Easy Windows one-click option**:  
Create a file called `run.bat` in the same folder with this content:
@echo off
cd /d "%~dp0"
python grizzly_password_checker_gui.py
pause
text Then double-click `run.bat` anytime.

## How to Use
1. Type or paste a test password (characters hidden for privacy)  
2. Click "Check Strength" or press Enter  
3. View instant feedback: strength level, score, issues, and whether it’s in a leaked list  
4. Click "Generate Strong" for a random 16-character suggestion  

**Example outcomes**:
- `password123` → DANGEROUS (found in leaked lists)  
- `Summer2026!` → Moderate or Weak  
- `Kj9#mP2$vL8xQ!rT` → Strong (not common)

## Why This Tool?
Unlike online checkers that send your input to servers, this runs entirely on your machine.  
It’s a quick, free way to demonstrate password risks — ideal for client education sessions, home setups, or small business awareness training.

## About Grizzly System Engineering
Home-based in **East Helena, Montana**, we provide reliable IT solutions statewide:
- Cybersecurity audits & penetration testing  
- Secure network setup (including Starlink)  
- Custom coding, automation & applications  
- Computer repair, data recovery, server builds  

**Website**: https://grizzlyse.com  
**Email**: info@grizzlyse.com  
**Phone/Text**: (406) 439-8127  

Need help with password managers, MFA rollout, or a full security review? Get in touch — we serve Helena, East Helena, and all of Montana.

Made with 🐻 in the Montana mountains.

**License**: MIT – free to use, modify, and share (attribution appreciated).
