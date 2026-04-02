import socket
import threading
from queue import Queue
from utils import detect_service, grab_banner
from db import vuln_db
from colorama import Fore

G, R, Y, C, W, B = Fore.GREEN, Fore.RED, Fore.YELLOW, Fore.CYAN, Fore.WHITE, Fore.BLUE

port_queue = Queue()
open_ports = []
print_lock = threading.Lock()

def port_scan(target_ip, port, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            if s.connect_ex((target_ip, port)) == 0:
                service = detect_service(port)
                banner = grab_banner(target_ip, port)
                vuln = vuln_db.get(port, {"risk": "No info", "severity": "-"})

                with print_lock:
                    print(f"{G}[+] {port:<5} OPEN | {service:<10} | {vuln['risk']} | {banner}")
                    open_ports.append({
                        "port": port, "service": service, 
                        "banner": banner, "vulnerability": vuln
                    })
    except:
        pass

def worker(target_ip, timeout):
    while not port_queue.empty():
        port = port_queue.get()
        port_scan(target_ip, port, timeout)
        port_queue.task_done()