#!/usr/bin/env python3
import sys
import subprocess
import argparse
from datetime import datetime
import nmap  # ← This was missing at global scope — add it here!

# Try to import colorama (optional for colors)
try:
    from colorama import init, Fore, Style
    COLOR_AVAILABLE = True
    init(autoreset=True)
except ImportError:
    COLOR_AVAILABLE = False
    # Fallback dummy class for colors
    class Dummy:
        def __getattr__(self, name): return ''
    Fore = Style = Dummy()

def colored(text, color):
    if COLOR_AVAILABLE:
        return f"{color}{text}{Style.RESET_ALL if hasattr(Style, 'RESET_ALL') else ''}"
    return text

def print_banner():
    print(colored("=== Grizzly Security Scan (GSS) ===", Fore.GREEN))
    print(colored("Lightweight Cybersecurity Audit Tool - Grizzly System Engineering", Fore.YELLOW))
    print(colored("WARNING: Only scan networks/IPs you OWN or have WRITTEN PERMISSION for!", Fore.RED))
    print("Montana-based | East Helena | (406) 439-8127 | info@grizzlyse.com\n")

def check_dependencies():
    missing = []
    
    # Check python-nmap (we already imported it globally, but verify it's usable)
    try:
        _ = nmap.PortScanner()  # Just instantiate to confirm
    except Exception as e:
        missing.append(f"python-nmap ({str(e)})")
    
    # Check Nmap binary
    try:
        result = subprocess.run(["nmap", "--version"], capture_output=True, text=True, timeout=8)
        if result.returncode != 0 or "Nmap" not in result.stdout:
            missing.append("nmap_binary")
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        missing.append("nmap_binary")
    
    if missing:
        print(colored("\n=== MISSING DEPENDENCIES DETECTED ===", Fore.RED))
        print("Please install/fix the following:\n")
        
        if "nmap_binary" in missing:
            print("1. Nmap binary:")
            print("   → Download: https://nmap.org/download.html")
            print("   → Windows installer → Install Npcap + Add to PATH")
            print("   → Verify: cmd → nmap -V\n")
        
        if any("python-nmap" in m for m in missing):
            print("2. python-nmap module:")
            print("   → pip install python-nmap\n")
        
        if not COLOR_AVAILABLE:
            print("3. colorama (optional):")
            print("   → pip install colorama\n")
        
        print(colored("Fix these, then re-run the script.", Fore.YELLOW))
        sys.exit(1)
    
    print(colored("[✔] Dependencies OK. Starting scan...\n", Fore.GREEN))
    return True

def run_scan(target):
    print(colored(f"[*] Starting scan on {target} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...", Fore.CYAN))
    
    nm = nmap.PortScanner()
    
    try:
        # Safe scan options
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
                lport = nm[host][proto].keys()
                for port in sorted(lport):
                    port_info = nm[host][proto][port]
                    service = port_info.get('name', 'unknown')
                    version = port_info.get('version', '').strip()
                    product = port_info.get('product', '').strip()
                    line = f"Port {port}/{proto.upper()}: {service} {product} {version}".strip()
                    
                    risk = "Low"
                    if port in [22, 23, 445, 3389]:
                        risk = "High - Potential exposure"
                    elif 'http' in service.lower() or 'https' in service.lower():
                        risk = "Medium - Check web vulns"
                    
                    results.append(colored(f"  {line} | Risk: {risk}", Fore.YELLOW))
                    
                    if 'script' in port_info:
                        for script, output in port_info['script'].items():
                            results.append(colored(f"    {script}: {output[:200]}...", Fore.MAGENTA))
        
        return results or ["No open ports or live hosts detected."]
    
    except Exception as e:
        return [f"Scan error: {str(e)}"]

def generate_report(results, target):
    report = [
        "Grizzly Security Scan Report",
        f"Target: {target}",
        f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "-" * 60,
        "",
    ]
    report.extend(results)
    report.append("")
    report.append("Recommendations:")
    report.append("- Close unnecessary ports (RDP 3389, SMB 445, etc. if not needed).")
    report.append("- Patch and update all services/software.")
    report.append("- For full pentest, hardening, or remediation → contact us!")
    report.append("Grizzly System Engineering | (406) 439-8127 | info@grizzlyse.com")
    
    return "\n".join(report)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Grizzly Security Scan - Lightweight Audit Tool")
    parser.add_argument("target", help="Target IP, range (e.g., 192.168.1.0/24), or hostname")
    args = parser.parse_args()
    
    print_banner()
    
    if check_dependencies():
        scan_results = run_scan(args.target)
        report = generate_report(scan_results, args.target)
        
        print(report)
        
        filename = f"gss_report_{args.target.replace('/', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print(colored(f"\nReport saved: {filename}", Fore.GREEN))
