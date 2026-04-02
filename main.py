import socket
import threading
import time
import os
from scanner import worker, port_queue, open_ports
from utils import detect_os
from report import save_report
from colorama import Fore, init

init(autoreset=True)
G, R, Y, C, W, B = Fore.GREEN, Fore.RED, Fore.YELLOW, Fore.CYAN, Fore.WHITE, Fore.BLUE

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{R}" + "=" * 50)
    print(f"{R}[!] LEGAL DISCLAIMER: FOR ETHICAL USE ONLY")
    print(f"{Y}Scanning without permission is illegal globally")
    print(f"{Y}The creater of syr is NOT responsable for any illegal use ")
    print(f"{R}" + "=" * 50 + f"{W}\n")
    
    while True:
        agreement = input(f"{Y}Do you agree to terms? (i agree /no): {W}").strip().lower()
        if agreement == 'i agree': break
        print(f"{R}[!] You must agree to proceed.")

    print(f"\n{C}=== Syr Tool v2 (Professional Mode) ==={W}\n")

    while True:
        target = input(f"{Y}Target IP/Domain: {W}").strip()
        try:
            target_ip = socket.gethostbyname(target)
            print(f"{G}[+] Resolved to {target_ip}")
            break
        except:
            print(f"{R}[!] Invalid target. Please try again.")

    while True:
        ports = input(f"{Y}Port range (e.g. 20-100): {W}").strip()
        if '-' in ports:
            try:
                start_p, end_p = map(int, ports.split('-'))
                if 1 <= start_p <= 65535 and 1 <= end_p <= 65535 and start_p <= end_p:
                    break
                print(f"{R}[!] Invalid range (1-65535).")
            except:
                print(f"{R}[!] Use numbers (e.g. 80-443).")
        else:
            print(f"{R}[!] Use format Start-End.")

    while True:
        print(f"\n{C}Modes: {W}1.Normal (100 threads) | 2.Fast (200) | 3.Stealth (30)")
        mode = input(f"{Y}Choose (1/2/3): {W}").strip()
        if mode == "1": THREADS, timeout = 100, 0.8; break
        elif mode == "2": THREADS, timeout = 200, 0.3; break
        elif mode == "3": THREADS, timeout = 30, 1.5; break
        print(f"{R}[!] Invalid choice.")

    print(f"\n{B}[*] OS Guess: {detect_os(target_ip)}")
    print(f"{B}[*] Starting Scan...\n")

    for p in range(start_p, end_p + 1):
        port_queue.put(p)

    start_time = time.time()
    for _ in range(THREADS):
        t = threading.Thread(target=worker, args=(target_ip, timeout))
        t.daemon = True
        t.start()

    port_queue.join()
    duration = round(time.time() - start_time, 2)
    
    save_report(target_ip, duration)
    print(f"\n{G}[#] Finished in {duration}s")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()