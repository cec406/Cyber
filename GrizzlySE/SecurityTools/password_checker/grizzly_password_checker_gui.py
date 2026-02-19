# grizzly_password_checker_gui.py
# Grizzly System Engineering – East Helena, Montana
# Lightweight GUI Password Strength Checker
# https://grizzlyse.com | (406) 439-8127 | info@grizzlyse.com
#
# WARNING: For educational and testing use only.
# NEVER enter real, active passwords into any tool (even local ones).
# Use a password manager for real secrets.

import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import re
from pathlib import Path

# ────────────────────────────────────────────────
# Force wordlist to be in THE SAME FOLDER as this script
# This fixes the #1 Windows issue where cwd != script location
SCRIPT_DIR = Path(__file__).resolve().parent

# Primary name
WORDLIST_PATH = SCRIPT_DIR / "common_passwords.txt"

# Fallback names (in case you renamed it)
FALLBACK_NAMES = [
    "common-passwords.txt",
    "rockyou.txt",
    "passwords.txt",
    "10k-most-common.txt",
    "top-10000.txt",
    "leaked-passwords.txt"
]

# Try fallbacks if primary doesn't exist
if not WORDLIST_PATH.exists():
    for alt in FALLBACK_NAMES:
        candidate = SCRIPT_DIR / alt
        if candidate.exists():
            WORDLIST_PATH = candidate
            break

class GrizzlyPasswordChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("Grizzly Password Checker")
        self.root.geometry("520x420")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f4f8")

        # Load common passwords (now using forced path)
        self.common_passwords = set()
        self.load_common_passwords()

        # Style
        style = ttk.Style()
        style.configure("TLabel", background="#f0f4f8", font=("Helvetica", 11))
        style.configure("TButton", font=("Helvetica", 10, "bold"))
        style.configure("Result.TLabel", font=("Helvetica", 12, "bold"))

        # Header
        header = tk.Label(root, text="Grizzly Password Checker", font=("Helvetica", 16, "bold"),
                          bg="#2c3e50", fg="white", pady=10)
        header.pack(fill="x")

        subtitle = tk.Label(root, text="Check if your password is weak or leaked", bg="#f0f4f8",
                            fg="#34495e", font=("Helvetica", 10))
        subtitle.pack(pady=(5, 15))

        # Password entry frame
        frame = ttk.Frame(root, padding=15)
        frame.pack(fill="x")

        ttk.Label(frame, text="Enter password to test:").grid(row=0, column=0, sticky="w", pady=5)
        
        self.pwd_var = tk.StringVar()
        self.entry = ttk.Entry(frame, textvariable=self.pwd_var, show="*", width=35, font=("Courier", 12))
        self.entry.grid(row=1, column=0, sticky="ew", pady=5)
        self.entry.focus()

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, pady=15, sticky="ew")

        ttk.Button(btn_frame, text="Check Strength", command=self.check_password).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Generate Strong", command=self.generate_strong_password).pack(side="left", padx=5)

        # Result area
        self.result_var = tk.StringVar(value="Enter a password above and click 'Check Strength'")
        result_label = ttk.Label(root, textvariable=self.result_var, wraplength=480,
                                 justify="center", style="Result.TLabel")
        result_label.pack(pady=20, padx=20)

        # Footer branding
        footer = tk.Label(root, text="Grizzly System Engineering • East Helena, MT • grizzlyse.com",
                          bg="#f0f4f8", fg="#7f8c8d", font=("Helvetica", 9))
        footer.pack(side="bottom", pady=10)

        # Bind Enter key to check
        self.root.bind("<Return>", lambda event: self.check_password())

    def load_common_passwords(self):
        if not WORDLIST_PATH.exists():
            messagebox.showwarning("Missing Wordlist",
                                   f"Could not find a common passwords file in:\n{SCRIPT_DIR}\n\n"
                                   "Expected names: common_passwords.txt (or one of the fallbacks)\n\n"
                                   "Download example:\n"
                                   "https://github.com/danielmiessler/SecLists/raw/master/Passwords/Common-Credentials/10k-most-common.txt\n\n"
                                   "Save it in the same folder as this script.\n\n"
                                   "Tool will still work with basic strength rules.")
            return

        try:
            with open(WORDLIST_PATH, encoding="utf-8", errors="ignore") as f:
                self.common_passwords = {line.strip().lower() for line in f if line.strip()}
            print(f"[Grizzly] Loaded {len(self.common_passwords):,} common passwords from {WORDLIST_PATH.name}")
        except Exception as e:
            messagebox.showerror("Load Error", f"Could not read wordlist:\n{e}")

    def check_password(self):
        pwd = self.pwd_var.get().strip()
        if not pwd:
            self.result_var.set("Please enter a password.")
            return

        # Basic strength scoring
        score = 0
        issues = []

        length = len(pwd)
        if length < 8:
            issues.append("Too short (< 8 chars)")
        elif length >= 16:
            score += 3
        elif length >= 12:
            score += 2
        elif length >= 10:
            score += 1

        has_lower = bool(re.search(r"[a-z]", pwd))
        has_upper = bool(re.search(r"[A-Z]", pwd))
        has_digit = bool(re.search(r"\d", pwd))
        has_special = bool(re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", pwd))

        if has_lower: score += 1
        else: issues.append("No lowercase letters")
        if has_upper: score += 1
        else: issues.append("No uppercase letters")
        if has_digit: score += 1
        else: issues.append("No numbers")
        if has_special: score += 1
        else: issues.append("No special characters")

        # Bonus for good mix + length
        if length >= 12 and sum([has_lower, has_upper, has_digit, has_special]) >= 3:
            score += 1

        # Common password check
        is_common = pwd.lower() in self.common_passwords

        # Determine overall strength
        if is_common:
            strength = "DANGEROUS"
            color = "red"
            msg = "This password appears in known leaked/common lists!\nDO NOT USE IT ANYWHERE."
        elif score >= 6:
            strength = "Strong"
            color = "green"
            msg = "Good strength – still use unique passwords + manager."
        elif score >= 4:
            strength = "Moderate"
            color = "orange"
            msg = "Okay, but could be stronger."
        else:
            strength = "Weak"
            color = "red"
            msg = "Too weak – easy to crack."

        # Build result text
        result_text = f"Strength: {strength}\n\n"
        result_text += f"Score: {score}/7   Length: {length} chars\n\n"

        if is_common:
            result_text += "!!! FOUND IN COMMON LEAKED PASSWORDS !!!\n\n"

        if issues:
            result_text += "Issues:\n• " + "\n• ".join(issues) + "\n\n"

        result_text += msg + "\n\n"
        result_text += "Recommendation: 16+ random characters via password manager."

        self.result_var.set(result_text)

        # Try to color the result text (best effort)
        try:
            result_label = self.root.nametowidget(self.result_var._name)
            result_label.config(foreground=color)
        except:
            pass

    def generate_strong_password(self):
        length = 16
        chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
        password = ''.join(random.SystemRandom().choice(chars) for _ in range(length))
        
        messagebox.showinfo("Strong Password Suggestion",
                            f"Here's a strong, random password:\n\n{password}\n\n"
                            "Copy it now and store in a password manager.\n"
                            "Never reuse passwords across sites!")

if __name__ == "__main__":
    root = tk.Tk()
    app = GrizzlyPasswordChecker(root)
    root.mainloop()
