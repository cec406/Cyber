# grizzly_security_scan_gui.py
# Grizzly System Engineering – East Helena, Montana
# GUI wrapper for the lightweight Nmap-based security scanner
# https://grizzlyse.com | (406) 439-8127 | info@grizzlyse.com
#
# WARNING: Only scan networks/IPs you OWN or have EXPLICIT WRITTEN PERMISSION for!
# This tool is for educational and authorized testing use only.

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import nmap
import sys
import subprocess
from datetime import datetime
from pathlib import Path

class GrizzlySecurityScanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Grizzly Security Scan")
        self.root.geometry("780x620")
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f4f8")

        # Style
        style = ttk.Style()
        style.configure("TLabel", background="#f0f4f8", font=("Helvetica", 10))
        style.configure("TButton", font=("Helvetica", 10, "bold"))
        style.configure("Header.TLabel", font=("Helvetica", 16, "bold"))

        # Header
        header = ttk.Label(root, text="Grizzly Security Scan", style="Header.TLabel",
                           foreground="#2c3e50")
        header.pack(pady=10)

        warning = tk.Label(root, text="ONLY SCAN NETWORKS YOU OWN OR HAVE WRITTEN PERMISSION FOR!",
                           fg="red", bg="#f0f4f8", font=("Helvetica", 10, "bold"))
        warning.pack(pady=(0, 15))

        # Input frame
        input_frame = ttk.Frame(root, padding=15)
        input_frame.pack(fill="x")

        ttk.Label(input_frame, text="Target (IP, range or hostname):").grid(row=0, column=0, sticky="w", pady=5)
        self.target_var = tk.StringVar(value="192.168.1.1")
        self.target_entry = ttk.Entry(input_frame, textvariable=self.target_var, width=40, font=("Courier", 12))
        self.target_entry.grid(row=1, column=0, sticky="ew", pady=5)
        self.target_entry.focus()

        # Buttons
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=2, column=0, pady=15, sticky="ew")

        self.scan_btn = ttk.Button(btn_frame, text="Start Scan", command=self.start_scan)
        self.scan_btn.pack(side="left", padx=5)

        ttk.Button(btn_frame, text="Save Report", command=self.save_report).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_output).pack(side="left", padx=5)

        # Output area
        self.output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=25,
                                                     font=("Consolas", 10), bg="#1e1e1e", fg="#d4d4d4")
        self.output_text.pack(padx=15, pady=10, fill="both", expand=True)

        # Footer
        footer = tk.Label(root, text="Grizzly System Engineering • East Helena, MT • grizzlyse.com",
                          bg="#f0f4f8", fg="#7f8c8d", font=("Helvetica", 9))
        footer.pack(side="bottom", pady=10)

        self.report_content = ""
        self.is_scanning = False

    def log(self, message, color="white"):
        self.output_text.insert(tk.END, message + "\n", f"color_{color}")
        self.output_text.tag_config("color_green", foreground="#00ff00")
        self.output_text.tag_config("color_yellow", foreground="#ffff00")
        self.output_text.tag_config("color_red", foreground="#ff5555")
        self.output_text.tag_config("color_cyan", foreground="#00ffff")
        self.output_text.see(tk.END)

    def check_nmap(self):
        try:
            subprocess.run(["nmap", "--version"], capture_output=True, timeout=5, check=True)
            return True
        except Exception:
            return False

    def start_scan(self):
        if self.is_scanning:
            messagebox.showinfo("Busy", "A scan is already running.")
            return

        target = self.target_var.get().strip()
        if not target:
            messagebox.showwarning("Input Required", "Please enter a target IP, range or hostname.")
            return

        if not self.check_nmap():
            messagebox.showerror("Nmap Missing", "Nmap is not installed or not in PATH.\n\n"
                                                 "Download from: https://nmap.org/download.html\n"
                                                 "Install and add to PATH (Windows).\n"
                                                 "Then restart the application.")
            return

        self.is_scanning = True
        self.scan_btn.config(state="disabled", text="Scanning...")
        self.output_text.delete("1.0", tk.END)
        self.report_content = ""
        self.log("=== Grizzly Security Scan started ===", "cyan")
        self.log(f"Target: {target}", "cyan")
        self.log(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "cyan")
        self.log("-" * 60, "cyan")
        self.log("WARNING: Only proceed if you have explicit permission!", "red")
        self.root.update()

        try:
            nm = nmap.PortScanner()
            self.log("\n[*] Scanning... (this may take 30–120 seconds)", "yellow")

            # Safe scan: service/version + safe vuln scripts, open ports only
            nm.scan(target, arguments='-sV --script vuln -T4 --open')

            results = []
            for host in nm.all_hosts():
                host_info = f"Host: {host} ({nm[host].hostname() or 'Unknown'})"
                state = nm[host].state()
                if state != 'up':
                    continue

                results.append(host_info)
                results.append(f"Status: {state}")

                for proto in nm[host].all_protocols():
                    ports = nm[host][proto].keys()
                    for port in sorted(ports):
                        pinfo = nm[host][proto][port]
                        service = pinfo.get('name', 'unknown')
                        version = pinfo.get('version', '').strip()
                        product = pinfo.get('product', '').strip()
                        line = f"Port {port}/{proto.upper()}: {service} {product} {version}".strip()

                        risk = "Low"
                        if port in [22, 23, 445, 3389]:
                            risk = "High - Potential exposure"
                        elif 'http' in service.lower() or 'https' in service.lower():
                            risk = "Medium - Check web vulns"

                        results.append(f"  {line} | Risk: {risk}")

                        if 'script' in pinfo:
                            for script, output in pinfo['script'].items():
                                results.append(f"    {script}: {output[:200]}...")

            if not results:
                results.append("No open ports or live hosts detected.")

            self.report_content = "\n".join(results)
            self.log("\nScan complete.", "green")
            self.log("\n".join(results), "white")

            recommendations = [
                "\nRecommendations:",
                "- Close unnecessary ports (especially RDP 3389, SMB 445 if not needed).",
                "- Keep services updated — outdated versions are common entry points.",
                "- For full pentest or hardening, contact Grizzly System Engineering."
            ]
            self.log("\n".join(recommendations), "yellow")

        except Exception as e:
            error_msg = f"Scan error: {str(e)}"
            self.log(error_msg, "red")
            self.report_content = error_msg

        finally:
            self.is_scanning = False
            self.scan_btn.config(state="normal", text="Start Scan")
            self.root.update()

    def save_report(self):
        if not self.report_content:
            messagebox.showinfo("No Report", "Run a scan first to generate a report.")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"gss_report_{self.target_var.get().replace('/', '_')}_{timestamp}.txt"

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Scan Report",
            initialfile=default_name
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("Grizzly Security Scan Report\n")
                    f.write(f"Target: {self.target_var.get()}\n")
                    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("-" * 60 + "\n\n")
                    f.write(self.report_content + "\n\n")
                    f.write("For full audits or remediation → Grizzly System Engineering\n")
                    f.write("https://grizzlyse.com | (406) 439-8127 | info@grizzlyse.com")
                messagebox.showinfo("Saved", f"Report saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Could not save file:\n{e}")

    def clear_output(self):
        if messagebox.askyesno("Clear", "Clear current output?"):
            self.output_text.delete("1.0", tk.END)
            self.report_content = ""

if __name__ == "__main__":
    root = tk.Tk()
    app = GrizzlySecurityScanGUI(root)
    root.mainloop()