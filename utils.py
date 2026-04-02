import socket
import subprocess
import os

def grab_banner(ip, port):
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect((ip, port))
        try:
            s.send(b"HEAD / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")
        except:
            pass
        banner = s.recv(2048).decode(errors="ignore").strip()
        return banner.split("\n")[0] if banner else "No banner"
    except:
        return "No banner"

def detect_os(ip):
    try:
        if os.name == "nt":
            output = subprocess.check_output(["ping", "-n", "1", ip]).decode()
        else:
            output = subprocess.check_output(["ping", "-c", "1", ip]).decode()

        if "ttl=64" in output: return "Linux"
        elif "ttl=128" in output: return "Windows"
        else: return "Unknown"
    except:
        return "Unknown"

def detect_service(port):
    try:
        return socket.getservbyport(port, 'tcp')
    except:
        return "Unknown"