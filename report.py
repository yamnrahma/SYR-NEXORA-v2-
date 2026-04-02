from datetime import datetime
from scanner import open_ports
from colorama import Fore

G, R, Y, C, W, B = Fore.GREEN, Fore.RED, Fore.YELLOW, Fore.CYAN, Fore.WHITE, Fore.BLUE

def save_report(target_ip, duration):
    if not open_ports: return
    name = f"report_{target_ip}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(name, "w") as f:
        f.write(f"Syr Tool Report\nTarget: {target_ip}\nDuration: {duration}s\n\n")
        f.write("PORT  | SERVICE    | RISK\n" + "-"*30 + "\n")
        for p in open_ports:
            f.write(f"{p['port']} | {p['service']} | {p['vulnerability']['risk']}\n")
    print(f"\n{C}[+] Report saved as: {name}")