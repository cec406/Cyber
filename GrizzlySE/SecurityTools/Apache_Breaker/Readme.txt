Script runs nmap on desired network or single IP, finds open apache tomcat ports, then runs hydra to 
get username and password, it uses the Hydra commands. 
Ex. sudo python3 ./script.py xx.xx.xx.xx(or0/24) -C (user:pass file) -L(username file) -P (password file) -l(single username) -p (single password)
sudo python3 ./port_scan_auth_cracker.py 192.168.56.105 -C tomcat-betterdefaultpasslist(1).txt 
I prefer to run the terminal in the location of the py with the pass lists in the same folder. 
