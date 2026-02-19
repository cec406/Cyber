#!/usr/bin/env python3
"""
Grizzly Password Checker
Lightweight tool to check if a password is common (leaked) or weak.
Built by Grizzly System Engineering – East Helena, Montana
https://grizzlyse.com | (406) 439-8127 | info@grizzlyse.com

WARNING: Never enter your real/active password here or anywhere untrusted!
This is for educational/testing purposes only.
"""

import sys
import re
from getpass import getpass
from pathlib import Path

# Config – change this to your downloaded list
WORDLIST_PATH = Path("common_passwords.txt")  # or "rockyou.txt" if you use full

def load_common_passwords(file_path):
    if not file_path.exists():
        print(f"[!] Wordlist not found: {file_path}")
        print("Download one from e.g.: https://github.com/danielmiessler/SecLists")
        print("   → Common-Credentials/10-million-password-list-top-1000000.txt")
        sys.exit(1)
    
    print(f"[*] Loading {file_path.name} ...")
    with open(file_path, encoding="utf-8", errors="ignore") as f:
        passwords = {line.strip().lower() for line in f if line.strip()}
    print(f"[+] Loaded {len(passwords):,} common passwords.")
    return passwords

def check_strength(password):
    score = 0
    feedback = []

    length = len(password)
    if length < 8:
        feedback.append("Too short (<8 chars)")
    elif length >= 12:
        score += 2
    elif length >= 10:
        score += 1

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("No uppercase letters")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("No lowercase letters")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("No numbers")

    if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", password):
        score += 1
    else:
        feedback.append("No special characters")

    # Bonus: mix of types
    if length >= 12 and score >= 4:
        score += 1

    if score >= 5:
        strength = "Strong"
    elif score >= 3:
        strength = "Moderate"
    else:
        strength = "Weak"

    return strength, score, feedback

def main():
    print("=== Grizzly Password Checker ===")
    print("Montana-based security tool from Grizzly System Engineering")
    print("→ For education only – do NOT use real passwords!\n")

    common_pwds = load_common_passwords(WORDLIST_PATH)

    while True:
        pwd = getpass("Enter password to check (or 'q' to quit): ").strip()
        if pwd.lower() in ['q', 'quit', 'exit']:
            print("Exiting.")
            break
        if not pwd:
            print("No password entered.\n")
            continue

        # Check against common list (case-insensitive)
        is_common = pwd.lower() in common_pwds

        strength, score, issues = check_strength(pwd)

        print("\nResults:")
        print(f"  Strength:     {strength} (score: {score}/6)")
        if is_common:
            print("  [!] DANGER: This password is in a leaked/common list!")
            print("      → Appears in known breaches – DO NOT USE!")
        else:
            print("  Not found in common leaked list (good sign, but not guaranteed)")

        if issues:
            print("  Issues:")
            for issue in issues:
                print(f"    - {issue}")
        else:
            print("  No major issues found in basic checks.")

        print("\nRecommendation: Use a password manager + 16+ random chars.")
        print("Need help with secure setup? Call Grizzly System Engineering!\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled.")