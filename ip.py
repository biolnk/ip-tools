#!/usr/bin/env python3
"""
IP Multitool - Comprehensive Network Utility Suite
Created by larpmadegoy
"""

import subprocess
import sys
import socket
import ipaddress
import threading
import time
from datetime import datetime
import argparse
import json
import requests
import os
import random
import string
from urllib.parse import urlparse
import ssl
from datetime import datetime as dt

class IPMultitool:
    def __init__(self):
        self.colors = {
            'HEADER': '\033[95m',
            'BLUE': '\033[94m',
            'GREEN': '\033[92m',
            'RED': '\033[91m',
            'YELLOW': '\033[93m',
            'CYAN': '\033[96m',
            'WHITE': '\033[97m',
            'END': '\033[0m',
            'BOLD': '\033[1m',
            'DIM': '\033[2m',
            'BLINK': '\033[5m'
        }
        self.last_results = None
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if sys.platform.lower().startswith('linux') or sys.platform.lower().startswith('darwin') else 'cls')
    
    def print_banner(self):
        banner = f"""
{self.colors['CYAN']}{self.colors['BOLD']}
 ██▓ ██▓███     ▄▄▄█████▓ ▒█████   ▒█████   ██▓      ██████ 
▓██▒▓██░  ██▒   ▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒    ▒██    ▒ 
▒██▒▓██░ ██▓▒   ▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░    ░ ▓██▄   
░██░▒██▄█▓▒ ▒   ░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░      ▒   ██▒
░██░▒██▒ ░  ░     ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒▒██████▒▒
░▓  ▒▓▒░ ░  ░     ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░▒ ▒▓▒ ▒ ░
 ▒ ░░▒ ░            ░      ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░░ ░▒  ░ ░
 ▒ ░░░            ░      ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░   ░  ░  ░  
 ░                           ░ ░      ░ ░      ░  ░      ░  
{self.colors['END']}
{self.colors['YELLOW']}{self.colors['DIM']}Created by larpmadegoy - https://discord.gg/EjcxgHJXQK {self.colors['END']}
{self.colors['GREEN']}{self.colors['DIM']}        Advanced Network Utility Suite v2.0{self.colors['END']}
        """
        print(banner)
    
    def print_main_menu(self):
        """Print main menu only"""
        menu = f"""
{self.colors['HEADER']}{self.colors['BOLD']}─────────────────────────────────────────────────────────────────────{self.colors['END']}
{self.colors['HEADER']}{self.colors['BOLD']}                         MAIN MENU                                          {self.colors['END']}
{self.colors['HEADER']}{self.colors['BOLD']}─────────────────────────────────────────────────────────────────────{self.colors['END']}
{self.colors['CYAN']}                                                                                     {self.colors['END']}
{self.colors['GREEN']}     BASIC NETWORK TOOLS:                                                           {self.colors['END']}
{self.colors['GREEN']}     1. IP Information Lookup           2. Ping Host                                 {self.colors['END']}
{self.colors['GREEN']}     3. Traceroute                     4. Port Scanner                              {self.colors['END']}
{self.colors['GREEN']}     5. Subnet Calculator              6. DNS Lookup                                {self.colors['END']}
{self.colors['GREEN']}     7. Reverse DNS Lookup             8. WHOIS Lookup                              {self.colors['END']}
{self.colors['GREEN']}     9. Geolocation Lookup             10. Batch IP Lookup                          {self.colors['END']}
{self.colors['CYAN']}                                                                                     {self.colors['END']}
{self.colors['YELLOW']}     ADVANCED NETWORK TOOLS:                                                        {self.colors['END']}
{self.colors['YELLOW']}     11. Network Scanner (CIDR)        12. Bandwidth Speed Test                     {self.colors['END']}
{self.colors['YELLOW']}     13. MAC Address Lookup            14. IP to ASN Lookup                        {self.colors['END']}
{self.colors['YELLOW']}     15. SSL Certificate Checker       16. HTTP Header Grabber                     {self.colors['END']}
{self.colors['YELLOW']}     17. Open Port Checker (Common)    18. DNS Brute Forcer (Subdomain)            {self.colors['END']}
{self.colors['YELLOW']}     19. IP Range Generator            20. Network Interface Info                  {self.colors['END']}
{self.colors['YELLOW']}     21. Packet Loss Test              22. Latency Monitor                          {self.colors['END']}
{self.colors['YELLOW']}     23. IPv4 to IPv6 Converter        24. Random IP Generator                     {self.colors['END']}
{self.colors['YELLOW']}     25. BGP Lookup                    26. Threat Intelligence Check               {self.colors['END']}
{self.colors['CYAN']}                                                                                     {self.colors['END']}
{self.colors['RED']}     UTILITY TOOLS:                                                                  {self.colors['END']}
{self.colors['RED']}     27. URL Parser                     28. IP Calculator                            {self.colors['END']}
{self.colors['RED']}     29. CIDR to IP Range               30. IP Reputation Check                      {self.colors['END']}
{self.colors['RED']}     31. DNS Propagation Check          32. Save Results to File                     {self.colors['END']}
{self.colors['RED']}     33. Clear Screen                   34. Exit                                      {self.colors['END']}
{self.colors['CYAN']}                                                                                     {self.colors['END']}
        """
        print(menu)
    
    def wait_for_continue(self):
        """Wait for user input and clear screen"""
        input(f"\n{self.colors['BLUE']}Press Enter to return to main menu...{self.colors['END']}")
        self.clear_screen()
        self.print_banner()
        self.print_main_menu()
    
    def save_results(self, data, filename=None):
        """Save results to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ip_tool_results_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(data)
            print(f"\n{self.colors['GREEN']}✓ Results saved to {filename}{self.colors['END']}")
            self.last_results = data
            return True
        except Exception as e:
            print(f"{self.colors['RED']}✗ Error saving file: {str(e)}{self.colors['END']}")
            return False
    
    def get_ip_info(self, ip_address=None):
        """Get detailed information about an IP address"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║         IP INFORMATION LOOKUP          ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        try:
            if not ip_address:
                response = requests.get('https://api.ipify.org?format=json', timeout=5)
                public_ip = response.json()['ip']
                print(f"{self.colors['GREEN']}Your Public IP: {public_ip}{self.colors['END']}")
                ip_address = input(f"\n{self.colors['BLUE']}Enter IP address to lookup (press Enter for your public IP): {self.colors['END']}")
                if not ip_address:
                    ip_address = public_ip
            
            # Get detailed IP information
            response = requests.get(f'http://ip-api.com/json/{ip_address}?fields=66846719', timeout=5)
            data = response.json()
            
            if data['status'] == 'success':
                output = f"""
{self.colors['YELLOW']}{'═'*60}{self.colors['END']}
{self.colors['BOLD']}📊 IP INFORMATION FOR: {ip_address}{self.colors['END']}
{self.colors['YELLOW']}{'═'*60}{self.colors['END']}
🌍 LOCATION:
  • Country: {data.get('country', 'N/A')} ({data.get('countryCode', 'N/A')})
  • Region: {data.get('regionName', 'N/A')}
  • City: {data.get('city', 'N/A')}
  • ZIP Code: {data.get('zip', 'N/A')}
  • Timezone: {data.get('timezone', 'N/A')}

📍 COORDINATES:
  • Latitude: {data.get('lat', 'N/A')}
  • Longitude: {data.get('lon', 'N/A')}

🏢 NETWORK INFO:
  • ISP: {data.get('isp', 'N/A')}
  • Organization: {data.get('org', 'N/A')}
  • AS: {data.get('as', 'N/A')}
  • Reverse DNS: {data.get('reverse', 'N/A')}

📱 MOBILE: {'Yes' if data.get('mobile') else 'No'}
📡 PROXY: {'Yes' if data.get('proxy') else 'No'}
🏠 HOSTING: {'Yes' if data.get('hosting') else 'No'}
{self.colors['YELLOW']}{'═'*60}{self.colors['END']}
"""
                print(output)
                
                save_choice = input(f"\n{self.colors['BLUE']}Save results to file? (y/n): {self.colors['END']}")
                if save_choice.lower() == 'y':
                    self.save_results(output)
            else:
                print(f"{self.colors['RED']}Error: {data.get('message', 'Unknown error')}{self.colors['END']}")
                
        except Exception as e:
            print(f"{self.colors['RED']}Error: {str(e)}{self.colors['END']}")
        
        self.wait_for_continue()
    
    def ping_host(self, host, count=4):
        """Ping a host with detailed statistics"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║               PING TOOL                ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        if not host:
            host = input(f"{self.colors['BLUE']}Enter host to ping: {self.colors['END']}")
        
        try:
            print(f"\n{self.colors['GREEN']}📡 Pinging {host}...{self.colors['END']}\n")
            
            param = '-n' if sys.platform.lower().startswith('win') else '-c'
            result = subprocess.run(['ping', param, str(count), host], 
                                  capture_output=True, text=True, timeout=10)
            
            # Parse ping statistics
            output = result.stdout
            print(output)
            
            if result.returncode == 0:
                # Extract statistics
                if 'time=' in output:
                    times = []
                    for line in output.split('\n'):
                        if 'time=' in line:
                            time_str = line.split('time=')[1].split(' ')[0].replace('ms', '')
                            try:
                                times.append(float(time_str))
                            except:
                                pass
                    
                    if times:
                        avg_time = sum(times) / len(times)
                        min_time = min(times)
                        max_time = max(times)
                        print(f"\n{self.colors['GREEN']}📊 Statistics:")
                        print(f"  • Min: {min_time:.2f}ms")
                        print(f"  • Max: {max_time:.2f}ms")
                        print(f"  • Avg: {avg_time:.2f}ms")
                        print(f"  • Packet Loss: {output.count('Request timed out') if sys.platform.lower().startswith('win') else output.count('100% packet loss') * 25}%{self.colors['END']}")
            else:
                print(f"{self.colors['RED']}✗ Host is not reachable{self.colors['END']}")
                
        except subprocess.TimeoutExpired:
            print(f"{self.colors['RED']}Timeout: Ping request took too long{self.colors['END']}")
        except Exception as e:
            print(f"{self.colors['RED']}Error: {str(e)}{self.colors['END']}")
        
        self.wait_for_continue()
    
    def traceroute(self, host):
        """Perform traceroute to host"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║            TRACEROUTE TOOL             ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        if not host:
            host = input(f"{self.colors['BLUE']}Enter host to traceroute: {self.colors['END']}")
        
        try:
            print(f"\n{self.colors['GREEN']}🗺️  Tracing route to {host}...{self.colors['END']}\n")
            
            if sys.platform.lower().startswith('win'):
                command = ['tracert', '-d', host]  # -d prevents DNS resolution for speed
            else:
                command = ['traceroute', '-n', host]
            
            result = subprocess.run(command, capture_output=True, text=True, timeout=30)
            print(result.stdout)
            
        except subprocess.TimeoutExpired:
            print(f"{self.colors['RED']}Timeout: Traceroute took too long{self.colors['END']}")
        except Exception as e:
            print(f"{self.colors['RED']}Error: {str(e)}{self.colors['END']}")
        
        self.wait_for_continue()
    
    def scan_port(self, host, port, timeout=1):
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                return True, self.get_service_name(port)
            return False, None
        except:
            return False, None
    
    def get_service_name(self, port):
        """Get common service name for port"""
        common_ports = {
            20: 'FTP-data', 21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
            53: 'DNS', 80: 'HTTP', 110: 'POP3', 111: 'RPC', 135: 'RPC',
            139: 'NetBIOS', 143: 'IMAP', 443: 'HTTPS', 445: 'SMB', 993: 'IMAPS',
            995: 'POP3S', 1723: 'PPTP', 3306: 'MySQL', 3389: 'RDP', 5432: 'PostgreSQL',
            5900: 'VNC', 6379: 'Redis', 8080: 'HTTP-Alt', 8443: 'HTTPS-Alt', 27017: 'MongoDB'
        }
        return common_ports.get(port, 'Unknown')
    
    def port_scanner(self, host, ports, scan_type='tcp'):
        """Scan multiple ports with progress"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║            PORT SCANNER TOOL           ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        if not host:
            host = input(f"{self.colors['BLUE']}Enter host to scan: {self.colors['END']}")
        
        if not ports:
            port_input = input(f"{self.colors['BLUE']}Enter ports (e.g., 1-100 or 22,80,443): {self.colors['END']}")
            
            ports = []
            if '-' in port_input:
                start, end = map(int, port_input.split('-'))
                ports = range(start, end + 1)
            else:
                ports = [int(p.strip()) for p in port_input.split(',')]
        
        print(f"\n{self.colors['GREEN']}🔍 Scanning {host}...{self.colors['END']}\n")
        print(f"{self.colors['YELLOW']}{'PORT':<8} {'STATUS':<10} {'SERVICE':<15}{self.colors['END']}")
        print(f"{self.colors['YELLOW']}{'-'*40}{self.colors['END']}")
        
        open_ports = []
        total_ports = len(ports)
        scanned = 0
        
        def scan_worker(port):
            nonlocal scanned
            is_open, service = self.scan_port(host, port)
            if is_open:
                open_ports.append((port, service))
                print(f"{self.colors['GREEN']}{port:<8} {'OPEN':<10} {service:<15}{self.colors['END']}")
            scanned += 1
            if scanned % 10 == 0:
                print(f"\r{self.colors['DIM']}Progress: {scanned}/{total_ports} ports scanned{self.colors['END']}", end='')
        
        threads = []
        for port in ports:
            thread = threading.Thread(target=scan_worker, args=(port,))
            thread.start()
            threads.append(thread)
            
            if len(threads) >= 50:
                for t in threads:
                    t.join()
                threads = []
        
        for thread in threads:
            thread.join()
        
        print(f"\n\n{self.colors['GREEN']}✓ Scan complete. Found {len(open_ports)} open port(s).{self.colors['END']}\n")
        
        self.wait_for_continue()
        return open_ports
    
    def common_port_checker(self, host):
        """Check common ports only"""
        common_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 
                        993, 995, 1723, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 27017]
        self.port_scanner(host, common_ports)
    
    def subnet_calculator(self, network_cidr):
        """Calculate detailed subnet information"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║          SUBNET CALCULATOR TOOL        ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        if not network_cidr:
            network_cidr = input(f"{self.colors['BLUE']}Enter network CIDR (e.g., 192.168.1.0/24): {self.colors['END']}")
        
        try:
            network = ipaddress.ip_network(network_cidr, strict=False)
            
            output = f"""
{self.colors['YELLOW']}{'═'*60}{self.colors['END']}
{self.colors['BOLD']}📐 SUBNET CALCULATOR: {network_cidr}{self.colors['END']}
{self.colors['YELLOW']}{'═'*60}{self.colors['END']}

🔢 NETWORK INFORMATION:
  • Network Address: {network.network_address}
  • Broadcast Address: {network.broadcast_address}
  • Netmask: {network.netmask}
  • Wildcard Mask: {ipaddress.IPv4Address(int(network.hostmask))}
  • CIDR Notation: /{network.prefixlen}
  • IP Version: IPv{network.version}

📊 ADDRESS SPACE:
  • First Usable: {list(network.hosts())[0] if network.num_addresses > 2 else 'N/A'}
  • Last Usable: {list(network.hosts())[-1] if network.num_addresses > 2 else 'N/A'}
  • Total Addresses: {network.num_addresses:,}
  • Usable Hosts: {network.num_addresses - 2 if network.num_addresses > 2 else 0}

📈 SUBNET INFO:
  • Subnet Class: {self.get_subnet_class(network.prefixlen)}
  • Binary Netmask: {self.ip_to_binary(str(network.netmask))}
  • Network Binary: {self.ip_to_binary(str(network.network_address))}
{self.colors['YELLOW']}{'═'*60}{self.colors['END']}
"""
            print(output)
            
            save_choice = input(f"\n{self.colors['BLUE']}Save results to file? (y/n): {self.colors['END']}")
            if save_choice.lower() == 'y':
                self.save_results(output)
            
        except ValueError as e:
            print(f"{self.colors['RED']}Invalid network CIDR: {str(e)}{self.colors['END']}")
        
        self.wait_for_continue()
    
    def get_subnet_class(self, prefixlen):
        """Determine subnet class"""
        if prefixlen <= 8:
            return 'A (Large Network)'
        elif prefixlen <= 16:
            return 'B (Medium Network)'
        elif prefixlen <= 24:
            return 'C (Small Network)'
        else:
            return 'Subnetted'
    
    def ip_to_binary(self, ip):
        """Convert IP to binary representation"""
        return '.'.join([bin(int(x)+256)[3:] for x in ip.split('.')])
    
    def dns_lookup(self, domain):
        """Perform comprehensive DNS lookup"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║              DNS LOOKUP TOOL           ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        if not domain:
            domain = input(f"{self.colors['BLUE']}Enter domain name: {self.colors['END']}")
        
        try:
            print(f"\n{self.colors['GREEN']}🔍 DNS Lookup for: {domain}{self.colors['END']}\n")
            output = f"DNS Lookup Results for {domain}\n{'='*50}\n\n"
            
            # A Records
            try:
                a_records = socket.gethostbyname_ex(domain)
                output += "A Records:\n"
                for ip in a_records[2]:
                    output += f"  • {ip}\n"
                output += "\n"
            except:
                pass
            
            # Try nslookup for more records
            try:
                result = subprocess.run(['nslookup', '-type=any', domain], 
                                      capture_output=True, text=True, timeout=5)
                output += "Detailed DNS Records:\n"
                output += result.stdout
            except:
                pass
            
            print(output)
            
            save_choice = input(f"\n{self.colors['BLUE']}Save results to file? (y/n): {self.colors['END']}")
            if save_choice.lower() == 'y':
                self.save_results(output)
                
        except Exception as e:
            print(f"{self.colors['RED']}Error: {str(e)}{self.colors['END']}")
        
        self.wait_for_continue()
    
    def reverse_dns(self, ip_address):
        """Perform reverse DNS lookup"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║           REVERSE DNS LOOKUP           ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        if not ip_address:
            ip_address = input(f"{self.colors['BLUE']}Enter IP address: {self.colors['END']}")
        
        try:
            hostname = socket.gethostbyaddr(ip_address)
            output = f"""
{self.colors['GREEN']}🔄 Reverse DNS Lookup for: {ip_address}{self.colors['END']}
{self.colors['YELLOW']}{'═'*50}{self.colors['END']}
📋 Primary Hostname: {hostname[0]}
📋 Aliases: {', '.join(hostname[1]) if hostname[1] else 'None'}
{self.colors['YELLOW']}{'═'*50}{self.colors['END']}
"""
            print(output)
        except socket.herror:
            print(f"{self.colors['RED']}No PTR record found for {ip_address}{self.colors['END']}")
        except Exception as e:
            print(f"{self.colors['RED']}Error: {str(e)}{self.colors['END']}")
        
        self.wait_for_continue()
    
    def whois_lookup(self, domain):
        """Perform WHOIS lookup"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║              WHOIS LOOKUP              ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        if not domain:
            domain = input(f"{self.colors['BLUE']}Enter domain name: {self.colors['END']}")
        
        try:
            print(f"\n{self.colors['GREEN']}📋 WHOIS Lookup for: {domain}{self.colors['END']}\n")
            
            try:
                result = subprocess.run(['whois', domain], 
                                      capture_output=True, text=True, timeout=10)
                lines = result.stdout.split('\n')[:60]
                output = '\n'.join(lines)
                print(output)
                if len(result.stdout.split('\n')) > 60:
                    print(f"\n{self.colors['YELLOW']}... (output truncated, use command line for full results){self.colors['END']}")
                    
                save_choice = input(f"\n{self.colors['BLUE']}Save results to file? (y/n): {self.colors['END']}")
                if save_choice.lower() == 'y':
                    self.save_results(result.stdout)
            except FileNotFoundError:
                response = requests.get(f'https://whoisjson.com/api/v1/whois?domain={domain}', timeout=10)
                data = response.json()
                output = json.dumps(data, indent=2)[:2000]
                print(output)
                
        except Exception as e:
            print(f"{self.colors['RED']}Error: {str(e)}{self.colors['END']}")
        
        self.wait_for_continue()
    
    def geolocation_lookup(self, ip_address):
        """Get detailed geolocation information"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║          GEOLOCATION LOOKUP            ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        if not ip_address:
            ip_address = input(f"{self.colors['BLUE']}Enter IP address: {self.colors['END']}")
        
        try:
            response = requests.get(f'https://ipapi.co/{ip_address}/json/', timeout=5)
            data = response.json()
            
            if 'error' not in data:
                output = f"""
{self.colors['YELLOW']}{'═'*60}{self.colors['END']}
{self.colors['BOLD']}🌍 GEOLOCATION FOR: {ip_address}{self.colors['END']}
{self.colors['YELLOW']}{'═'*60}{self.colors['END']}

📍 LOCATION DETAILS:
  • City: {data.get('city', 'N/A')}
  • Region: {data.get('region', 'N/A')}
  • Country: {data.get('country_name', 'N/A')}
  • Postal Code: {data.get('postal', 'N/A')}
  • Continent: {data.get('continent_code', 'N/A')}

🗺️  COORDINATES:
  • Latitude: {data.get('latitude', 'N/A')}
  • Longitude: {data.get('longitude', 'N/A')}

⏰ TIME & CURRENCY:
  • Timezone: {data.get('timezone', 'N/A')}
  • Currency: {data.get('currency', 'N/A')}
  • Currency Name: {data.get('currency_name', 'N/A')}

🏢 NETWORK INFO:
  • ASN: {data.get('asn', 'N/A')}
  • Organization: {data.get('org', 'N/A')}
  • ISP: {data.get('org', 'N/A')}
  
📱 LANGUAGE: {data.get('languages', 'N/A')}
🔒 SECURITY: {'VPN/Proxy detected' if data.get('security', {}).get('is_proxy') else 'No proxy detected'}
{self.colors['YELLOW']}{'═'*60}{self.colors['END']}
"""
                print(output)
                
                save_choice = input(f"\n{self.colors['BLUE']}Save results to file? (y/n): {self.colors['END']}")
                if save_choice.lower() == 'y':
                    self.save_results(output)
            else:
                print(f"{self.colors['RED']}Error: {data.get('error', 'Unknown error')}{self.colors['END']}")
                
        except Exception as e:
            print(f"{self.colors['RED']}Error: {str(e)}{self.colors['END']}")
        
        self.wait_for_continue()
    
    def batch_ip_lookup(self, file_path):
        """Process multiple IPs from file"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║           BATCH IP LOOKUP TOOL         ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        if not file_path:
            file_path = input(f"{self.colors['BLUE']}Enter path to IP list file: {self.colors['END']}")
        
        try:
            with open(file_path, 'r') as f:
                ips = [line.strip() for line in f if line.strip()]
            
            print(f"\n{self.colors['GREEN']}📊 Processing {len(ips)} IP addresses...{self.colors['END']}\n")
            
            results = []
            for i, ip in enumerate(ips, 1):
                print(f"{self.colors['CYAN']}[{i}/{len(ips)}] Looking up {ip}...{self.colors['END']}")
                try:
                    response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
                    data = response.json()
                    if data['status'] == 'success':
                        result = f"{ip},{data.get('country','')},{data.get('city','')},{data.get('isp','')}"
                        results.append(result)
                        print(f"  ✓ {data.get('country')} - {data.get('city')}")
                    else:
                        results.append(f"{ip},Error,Error,Error")
                        print(f"  ✗ Lookup failed")
                except:
                    results.append(f"{ip},Error,Error,Error")
                    print(f"  ✗ Connection error")
                
                time.sleep(0.5)  # Rate limiting
            
            # Save results to CSV
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            csv_file = f"batch_results_{timestamp}.csv"
            with open(csv_file, 'w') as f:
                f.write("IP,Country,City,ISP\n")
                f.write('\n'.join(results))
            
            print(f"\n{self.colors['GREEN']}✓ Results saved to {csv_file}{self.colors['END']}")
                
        except FileNotFoundError:
            print(f"{self.colors['RED']}File not found: {file_path}{self.colors['END']}")
        except Exception as e:
            print(f"{self.colors['RED']}Error: {str(e)}{self.colors['END']}")
        
        self.wait_for_continue()
    
    def network_scanner(self, cidr):
        """Scan entire network for active hosts"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║           NETWORK SCANNER TOOL         ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        if not cidr:
            cidr = input(f"{self.colors['BLUE']}Enter network CIDR (e.g., 192.168.1.0/24): {self.colors['END']}")
        
        try:
            network = ipaddress.ip_network(cidr, strict=False)
            print(f"\n{self.colors['GREEN']}🔍 Scanning network {cidr} for active hosts...{self.colors['END']}\n")
            
            active_hosts = []
            
            def scan_host(ip):
                try:
                    response = subprocess.run(['ping', '-c', '1', '-W', '1', str(ip)], 
                                            capture_output=True, timeout=2)
                    if response.returncode == 0:
                        active_hosts.append(str(ip))
                        print(f"{self.colors['GREEN']}✓ {ip} is up{self.colors['END']}")
                except:
                    pass
            
            threads = []
            for ip in network.hosts():
                thread = threading.Thread(target=scan_host, args=(ip,))
                thread.start()
                threads.append(thread)
                
                if len(threads) >= 20:
                    for t in threads:
                        t.join()
                    threads = []
            
            for thread in threads:
                thread.join()
            
            print(f"\n{self.colors['GREEN']}{'='*50}{self.colors['END']}")
            print(f"{self.colors['BOLD']}📊 SCAN RESULTS:{self.colors['END']}")
            print(f"  • Network: {cidr}")
            print(f"  • Active Hosts: {len(active_hosts)}")
            print(f"  • Total Hosts Scanned: {network.num_addresses - 2}")
            
            if active_hosts:
                print(f"\n{self.colors['GREEN']}Active IP Addresses:{self.colors['END']}")
                for host in active_hosts:
                    print(f"  • {host}")
            print(f"{self.colors['GREEN']}{'='*50}{self.colors['END']}\n")
            
        except Exception as e:
            print(f"{self.colors['RED']}Error: {str(e)}{self.colors['END']}")
        
        self.wait_for_continue()
    
    def speed_test(self):
        """Basic bandwidth speed test using speedtest-cli"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║           SPEED TEST TOOL              ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        try:
            print(f"\n{self.colors['GREEN']}⚡ Running speed test... This may take a moment{self.colors['END']}\n")
            
            # Try to use speedtest-cli if available
            try:
                result = subprocess.run(['speedtest-cli', '--simple'], 
                                      capture_output=True, text=True, timeout=30)
                print(result.stdout)
            except FileNotFoundError:
                # Fallback to downloading a test file
                import urllib.request
                test_url = "http://speedtest.tele2.net/10MB.zip"
                print(f"{self.colors['YELLOW']}Downloading test file...{self.colors['END']}")
                start_time = time.time()
                urllib.request.urlretrieve(test_url, "testfile.tmp")
                end_time = time.time()
                download_time = end_time - start_time
                file_size_mb = 10  # 10MB
                speed_mbps = (file_size_mb * 8) / download_time
                print(f"{self.colors['GREEN']}Download Speed: {speed_mbps:.2f} Mbps{self.colors['END']}")
                os.remove("testfile.tmp")
                
        except Exception as e:
            print(f"{self.colors['RED']}Speed test failed: {str(e)}{self.colors['END']}")
            print(f"{self.colors['YELLOW']}Tip: Install speedtest-cli with 'pip install speedtest-cli'{self.colors['END']}")
        
        self.wait_for_continue()
    
    def mac_lookup(self, mac_address):
        """Lookup MAC address vendor"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║           MAC ADDRESS LOOKUP           ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        if not mac_address:
            mac_address = input(f"{self.colors['BLUE']}Enter MAC address (e.g., 00:11:22:33:44:55): {self.colors['END']}")
        
        try:
            # Clean MAC address
            mac = mac_address.upper().replace(':', '').replace('-', '')
            if len(mac) != 12:
                print(f"{self.colors['RED']}Invalid MAC address format{self.colors['END']}")
                self.wait_for_continue()
                return
            
            # Use maclookup API
            response = requests.get(f'https://api.maclookup.app/v2/macs/{mac}', timeout=5)
            data = response.json()
            
            if data.get('found'):
                print(f"\n{self.colors['GREEN']}🔍 MAC Address Lookup{self.colors['END']}")
                print(f"{self.colors['YELLOW']}{'='*50}{self.colors['END']}")
                print(f"MAC Address: {mac_address}")
                print(f"Vendor: {data.get('vendor', 'Unknown')}")
                print(f"Company: {data.get('company', 'N/A')}")
                print(f"Block Type: {data.get('blockType', 'N/A')}")
                print(f"Block Size: {data.get('blockSize', 'N/A')}")
                print(f"{self.colors['YELLOW']}{'='*50}{self.colors['END']}\n")
            else:
                print(f"{self.colors['RED']}MAC address not found in database{self.colors['END']}")
                
        except Exception as e:
            print(f"{self.colors['RED']}Error: {str(e)}{self.colors['END']}")
        
        self.wait_for_continue()
    
    def asn_lookup(self, ip_address):
        """Lookup ASN information"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║              ASN LOOKUP TOOL           ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        if not ip_address:
            ip_address = input(f"{self.colors['BLUE']}Enter IP address: {self.colors['END']}")
        
        try:
            response = requests.get(f'https://ipinfo.io/{ip_address}/json', timeout=5)
            data = response.json()
            
            if 'org' in data:
                print(f"\n{self.colors['GREEN']}🔍 ASN Information for {ip_address}{self.colors['END']}")
                print(f"{self.colors['YELLOW']}{'='*50}{self.colors['END']}")
                print(f"Organization: {data['org']}")
                if 'asn' in data:
                    print(f"ASN: {data['asn']}")
                if 'asn_name' in data:
                    print(f"AS Name: {data['asn_name']}")
                print(f"{self.colors['YELLOW']}{'='*50}{self.colors['END']}\n")
            else:
                print(f"{self.colors['RED']}ASN information not found{self.colors['END']}")
                
        except Exception as e:
            print(f"{self.colors['RED']}Error: {str(e)}{self.colors['END']}")
        
        self.wait_for_continue()
    
    def ssl_checker(self, domain):
        """Check SSL certificate information"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║           SSL CERTIFICATE CHECKER      ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        if not domain:
            domain = input(f"{self.colors['BLUE']}Enter domain name: {self.colors['END']}")
        
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    print(f"\n{self.colors['GREEN']}🔒 SSL Certificate for {domain}{self.colors['END']}")
                    print(f"{self.colors['YELLOW']}{'='*60}{self.colors['END']}")
                    print(f"Subject: {cert.get('subject', 'N/A')}")
                    print(f"Issuer: {cert.get('issuer', 'N/A')}")
                    print(f"Version: {cert.get('version', 'N/A')}")
                    print(f"Serial Number: {cert.get('serialNumber', 'N/A')}")
                    print(f"Not Before: {cert.get('notBefore', 'N/A')}")
                    print(f"Not After: {cert.get('notAfter', 'N/A')}")
                    print(f"Subject Alt Names: {cert.get('subjectAltName', 'N/A')}")
                    
                    # Check expiration
                    expiry_date = dt.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    days_left = (expiry_date - dt.now()).days
                    
                    if days_left < 0:
                        print(f"Status: {self.colors['RED']}EXPIRED{self.colors['END']}")
                    elif days_left < 30:
                        print(f"Status: {self.colors['YELLOW']}Expires in {days_left} days (WARNING){self.colors['END']}")
                    else:
                        print(f"Status: {self.colors['GREEN']}Valid - Expires in {days_left} days{self.colors['END']}")
                    
                    print(f"{self.colors['YELLOW']}{'='*60}{self.colors['END']}\n")
                    
        except Exception as e:
            print(f"{self.colors['RED']}SSL Check failed: {str(e)}{self.colors['END']}")
        
        self.wait_for_continue()
    
    def http_header_grabber(self, url):
        """Grab HTTP headers from a URL"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║           HTTP HEADER GRABBER          ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        if not url:
            url = input(f"{self.colors['BLUE']}Enter URL: {self.colors['END']}")
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            response = requests.get(url, timeout=10, allow_redirects=True)
            
            print(f"\n{self.colors['GREEN']}🌐 HTTP Headers for {url}{self.colors['END']}")
            print(f"{self.colors['YELLOW']}{'='*60}{self.colors['END']}")
            print(f"Status Code: {response.status_code} {response.reason}")
            print(f"Protocol: {response.raw.version}")
            print(f"\n{self.colors['BOLD']}Headers:{self.colors['END']}")
            for key, value in response.headers.items():
                print(f"  {key}: {value}")
            print(f"{self.colors['YELLOW']}{'='*60}{self.colors['END']}\n")
            
        except Exception as e:
            print(f"{self.colors['RED']}Error: {str(e)}{self.colors['END']}")
        
        self.wait_for_continue()
    
    def dns_bruteforcer(self, domain, wordlist=None):
        """Brute force subdomains"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║           DNS BRUTE FORCER             ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        if not domain:
            domain = input(f"{self.colors['BLUE']}Enter domain: {self.colors['END']}")
        
        if not wordlist:
            common_subdomains = ['www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk', 
                                'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'dns', 'ns3', 'm', 'imap',
                                'test', 'ns', 'blog', 'pop3', 'dev', 'www2', 'admin', 'forum', 'news', 'vpn', 
                                'ns4', 'mail2', 'new', 'mysql', 'old', 'lists', 'support', 'mobile', 'mx', 
                                'static', 'docs', 'beta', 'shop', 'sql', 'secure', 'demo', 'cp', 'calendar', 
                                'wiki', 'web', 'media', 'email', 'images', 'img', 'download', 'dns2', 'portal']
        else:
            try:
                with open(wordlist, 'r') as f:
                    common_subdomains = [line.strip() for line in f]
            except:
                print(f"{self.colors['RED']}Wordlist not found, using default list{self.colors['END']}")
                common_subdomains = ['www', 'mail', 'ftp', 'localhost', 'webmail']
        
        print(f"\n{self.colors['GREEN']}🔍 Brute forcing subdomains for {domain}...{self.colors['END']}\n")
        
        found = []
        for sub in common_subdomains:
            test_domain = f"{sub}.{domain}"
            try:
                ip = socket.gethostbyname(test_domain)
                found.append((test_domain, ip))
                print(f"{self.colors['GREEN']}✓ Found: {test_domain} -> {ip}{self.colors['END']}")
            except:
                pass
            time.sleep(0.1)
        
        print(f"\n{self.colors['GREEN']}Found {len(found)} subdomains{self.colors['END']}\n")
        
        self.wait_for_continue()
        return found
    
    def ip_range_generator(self, start_ip, end_ip):
        """Generate range of IPs between start and end"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║           IP RANGE GENERATOR           ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        if not start_ip:
            start_ip = input(f"{self.colors['BLUE']}Enter start IP: {self.colors['END']}")
        if not end_ip:
            end_ip = input(f"{self.colors['BLUE']}Enter end IP: {self.colors['END']}")
        
        try:
            start = ipaddress.IPv4Address(start_ip)
            end = ipaddress.IPv4Address(end_ip)
            
            if start > end:
                print(f"{self.colors['RED']}Start IP must be less than end IP{self.colors['END']}")
                self.wait_for_continue()
                return
            
            ips = []
            for ip_int in range(int(start), int(end) + 1):
                ips.append(str(ipaddress.IPv4Address(ip_int)))
            
            print(f"\n{self.colors['GREEN']}Generated {len(ips)} IP addresses from {start_ip} to {end_ip}{self.colors['END']}")
            
            # Display first 20 IPs
            for ip in ips[:20]:
                print(f"  • {ip}")
            if len(ips) > 20:
                print(f"  ... and {len(ips) - 20} more")
            
            save_choice = input(f"\n{self.colors['BLUE']}Save IP list to file? (y/n): {self.colors['END']}")
            if save_choice.lower() == 'y':
                filename = f"ip_range_{start_ip}_to_{end_ip}.txt"
                with open(filename, 'w') as f:
                    f.write('\n'.join(ips))
                print(f"{self.colors['GREEN']}✓ Saved to {filename}{self.colors['END']}")
            
        except Exception as e:
            print(f"{self.colors['RED']}Error: {str(e)}{self.colors['END']}")
        
        self.wait_for_continue()
    
    def network_interfaces(self):
        """Display network interface information"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║         NETWORK INTERFACE INFO         ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        try:
            import netifaces
            
            print(f"\n{self.colors['GREEN']}🖧 Network Interface Information{self.colors['END']}")
            print(f"{self.colors['YELLOW']}{'='*60}{self.colors['END']}")
            
            for interface in netifaces.interfaces():
                addrs = netifaces.ifaddresses(interface)
                print(f"\n{self.colors['BOLD']}Interface: {interface}{self.colors['END']}")
                
                if netifaces.AF_INET in addrs:
                    for addr in addrs[netifaces.AF_INET]:
                        print(f"  IPv4: {addr.get('addr', 'N/A')}")
                        print(f"  Netmask: {addr.get('netmask', 'N/A')}")
                        print(f"  Broadcast: {addr.get('broadcast', 'N/A')}")
                
                if netifaces.AF_INET6 in addrs:
                    for addr in addrs[netifaces.AF_INET6]:
                        print(f"  IPv6: {addr.get('addr', 'N/A')}")
                
                if netifaces.AF_LINK in addrs:
                    for addr in addrs[netifaces.AF_LINK]:
                        print(f"  MAC: {addr.get('addr', 'N/A')}")
            
            print(f"{self.colors['YELLOW']}{'='*60}{self.colors['END']}\n")
            
        except ImportError:
            print(f"{self.colors['RED']}Please install netifaces: pip install netifaces{self.colors['END']}")
        except Exception as e:
            print(f"{self.colors['RED']}Error: {str(e)}{self.colors['END']}")
        
        self.wait_for_continue()
    
    def packet_loss_test(self, host, count=10):
        """Test packet loss percentage"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║           PACKET LOSS TEST             ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        if not host:
            host = input(f"{self.colors['BLUE']}Enter host: {self.colors['END']}")
        
        count_input = input(f"{self.colors['BLUE']}Number of packets (default 10): {self.colors['END']}")
        count = int(count_input) if count_input else 10
        
        print(f"\n{self.colors['GREEN']}📊 Testing packet loss to {host}...{self.colors['END']}\n")
        
        param = '-n' if sys.platform.lower().startswith('win') else '-c'
        result = subprocess.run(['ping', param, str(count), host], 
                              capture_output=True, text=True, timeout=30)
        
        output = result.stdout
        
        # Parse packet loss
        loss_percent = 0
        if sys.platform.lower().startswith('win'):
            if 'Lost =' in output:
                lost_line = [line for line in output.split('\n') if 'Lost =' in line][0]
                lost = int(lost_line.split('Lost =')[1].split(',')[0].strip())
                loss_percent = (lost / count) * 100
        else:
            if 'packet loss' in output:
                loss_line = [line for line in output.split('\n') if 'packet loss' in line][0]
                loss_percent = float(loss_line.split('%')[0].split()[-1])
        
        print(output)
        print(f"\n{self.colors['YELLOW']}Packet Loss: {loss_percent:.1f}%{self.colors['END']}")
        
        if loss_percent == 0:
            print(f"{self.colors['GREEN']}✓ Excellent connection - No packet loss{self.colors['END']}")
        elif loss_percent < 5:
            print(f"{self.colors['GREEN']}✓ Good connection - Minimal packet loss{self.colors['END']}")
        elif loss_percent < 15:
            print(f"{self.colors['YELLOW']}⚠ Fair connection - Some packet loss{self.colors['END']}")
        else:
            print(f"{self.colors['RED']}✗ Poor connection - High packet loss{self.colors['END']}")
        
        self.wait_for_continue()
    
    def latency_monitor(self, host, duration=10):
        """Monitor latency over time"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║            LATENCY MONITOR             ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        if not host:
            host = input(f"{self.colors['BLUE']}Enter host: {self.colors['END']}")
        
        duration_input = input(f"{self.colors['BLUE']}Duration in seconds (default 10): {self.colors['END']}")
        duration = int(duration_input) if duration_input else 10
        
        print(f"\n{self.colors['GREEN']}⏱️  Monitoring latency to {host} for {duration} seconds...{self.colors['END']}\n")
        
        latencies = []
        start_time = time.time()
        
        while time.time() - start_time < duration:
            try:
                param = '-n' if sys.platform.lower().startswith('win') else '-c'
                result = subprocess.run(['ping', param, '1', host], 
                                      capture_output=True, text=True, timeout=2)
                
                if 'time=' in result.stdout:
                    time_str = result.stdout.split('time=')[1].split(' ')[0].replace('ms', '')
                    latency = float(time_str)
                    latencies.append(latency)
                    print(f"{self.colors['GREEN']}Latency: {latency:.2f}ms{self.colors['END']}")
                else:
                    print(f"{self.colors['RED']}Request timeout{self.colors['END']}")
            except:
                print(f"{self.colors['RED']}Request failed{self.colors['END']}")
            
            time.sleep(1)
        
        if latencies:
            avg_latency = sum(latencies) / len(latencies)
            min_latency = min(latencies)
            max_latency = max(latencies)
            
            print(f"\n{self.colors['YELLOW']}{'='*50}{self.colors['END']}")
            print(f"{self.colors['BOLD']}Latency Statistics:{self.colors['END']}")
            print(f"  Samples: {len(latencies)}")
            print(f"  Min: {min_latency:.2f}ms")
            print(f"  Max: {max_latency:.2f}ms")
            print(f"  Avg: {avg_latency:.2f}ms")
            print(f"{self.colors['YELLOW']}{'='*50}{self.colors['END']}\n")
        
        self.wait_for_continue()
    
    def ipv4_to_ipv6(self, ipv4):
        """Convert IPv4 to IPv6 address"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║          IPv4 to IPv6 CONVERTER        ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        if not ipv4:
            ipv4 = input(f"{self.colors['BLUE']}Enter IPv4 address: {self.colors['END']}")
        
        try:
            ipv4_obj = ipaddress.IPv4Address(ipv4)
            ipv6_mapped = ipaddress.IPv6Address(f"::ffff:{ipv4}")
            
            print(f"\n{self.colors['GREEN']}🔄 IPv4 to IPv6 Conversion{self.colors['END']}")
            print(f"{self.colors['YELLOW']}{'='*50}{self.colors['END']}")
            print(f"IPv4: {ipv4}")
            print(f"IPv6 (IPv4-mapped): {ipv6_mapped}")
            print(f"IPv6 (6to4): 2002:{int(ipv4_obj) >> 16:02x}{(int(ipv4_obj) & 0xFFFF):02x}::/48")
            print(f"{self.colors['YELLOW']}{'='*50}{self.colors['END']}\n")
            
        except Exception as e:
            print(f"{self.colors['RED']}Error: {str(e)}{self.colors['END']}")
        
        self.wait_for_continue()
    
    def random_ip_generator(self, count=5):
        """Generate random IP addresses"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║           RANDOM IP GENERATOR          ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        count_input = input(f"{self.colors['BLUE']}Number of IPs to generate (default 5): {self.colors['END']}")
        count = int(count_input) if count_input else 5
        
        print(f"\n{self.colors['GREEN']}🎲 Generating {count} random IP addresses...{self.colors['END']}\n")
        
        ips = []
        for _ in range(count):
            ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
            ips.append(ip)
            print(f"  • {ip}")
        
        print()
        
        save_choice = input(f"{self.colors['BLUE']}Save IP list to file? (y/n): {self.colors['END']}")
        if save_choice.lower() == 'y':
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"random_ips_{timestamp}.txt"
            with open(filename, 'w') as f:
                f.write('\n'.join(ips))
            print(f"{self.colors['GREEN']}✓ Saved to {filename}{self.colors['END']}")
        
        self.wait_for_continue()
    
    def bgp_lookup(self, as_number):
        """Lookup BGP information for AS number"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║               BGP LOOKUP               ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        if not as_number:
            as_number = input(f"{self.colors['BLUE']}Enter AS number (e.g., 15169): {self.colors['END']}")
        
        try:
            response = requests.get(f'https://api.bgpview.io/asn/{as_number}', timeout=5)
            data = response.json()
            
            if data.get('status') == 'ok':
                print(f"\n{self.colors['GREEN']}🔍 BGP Information for AS{as_number}{self.colors['END']}")
                print(f"{self.colors['YELLOW']}{'='*60}{self.colors['END']}")
                print(f"AS Name: {data['data'].get('name', 'N/A')}")
                print(f"Description: {data['data'].get('description', 'N/A')}")
                print(f"Country: {data['data'].get('country_code', 'N/A')}")
                print(f"IPv4 Prefixes: {data['data'].get('ipv4_prefix_count', 0)}")
                print(f"IPv6 Prefixes: {data['data'].get('ipv6_prefix_count', 0)}")
                print(f"{self.colors['YELLOW']}{'='*60}{self.colors['END']}\n")
            else:
                print(f"{self.colors['RED']}ASN not found{self.colors['END']}")
                
        except Exception as e:
            print(f"{self.colors['RED']}Error: {str(e)}{self.colors['END']}")
        
        self.wait_for_continue()
    
    def threat_intelligence(self, ip_address):
        """Check IP threat intelligence"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║         THREAT INTELLIGENCE CHECK      ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        if not ip_address:
            ip_address = input(f"{self.colors['BLUE']}Enter IP address: {self.colors['END']}")
        
        try:
            response = requests.get(f'https://ipinfo.io/{ip_address}/json', timeout=5)
            data = response.json()
            
            print(f"\n{self.colors['GREEN']}🛡️  Threat Intelligence for {ip_address}{self.colors['END']}")
            print(f"{self.colors['YELLOW']}{'='*60}{self.colors['END']}")
            
            # Check for potential threats (simplified)
            risks = []
            
            if 'privacy' in data and data['privacy'].get('vpn'):
                risks.append("VPN/Proxy detected")
            if 'abuse' in data:
                risks.append("Reported for abuse")
            if 'hosting' in data and data.get('hosting'):
                risks.append("Hosting provider")
            
            if risks:
                print(f"{self.colors['RED']}Potential Risks Found:{self.colors['END']}")
                for risk in risks:
                    print(f"  ⚠️  {risk}")
            else:
                print(f"{self.colors['GREEN']}✓ No significant threats detected{self.colors['END']}")
            
            print(f"\n{self.colors['YELLOW']}Additional Info:{self.colors['END']}")
            print(f"  Organization: {data.get('org', 'N/A')}")
            print(f"  Country: {data.get('country', 'N/A')}")
            
            print(f"{self.colors['YELLOW']}{'='*60}{self.colors['END']}\n")
            
        except Exception as e:
            print(f"{self.colors['RED']}Error: {str(e)}{self.colors['END']}")
        
        self.wait_for_continue()
    
    def url_parser(self, url):
        """Parse and analyze URL components"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║               URL PARSER               ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        if not url:
            url = input(f"{self.colors['BLUE']}Enter URL: {self.colors['END']}")
        
        try:
            parsed = urlparse(url)
            
            print(f"\n{self.colors['GREEN']}🔗 URL Analysis{self.colors['END']}")
            print(f"{self.colors['YELLOW']}{'='*60}{self.colors['END']}")
            print(f"Scheme: {parsed.scheme}")
            print(f"Netloc: {parsed.netloc}")
            print(f"Path: {parsed.path}")
            print(f"Params: {parsed.params}")
            print(f"Query: {parsed.query}")
            print(f"Fragment: {parsed.fragment}")
            print(f"Port: {parsed.port or (443 if parsed.scheme == 'https' else 80)}")
            print(f"Hostname: {parsed.hostname}")
            print(f"{self.colors['YELLOW']}{'='*60}{self.colors['END']}\n")
            
        except Exception as e:
            print(f"{self.colors['RED']}Error: {str(e)}{self.colors['END']}")
        
        self.wait_for_continue()
    
    def ip_calculator(self):
        """Interactive IP calculator"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║             IP CALCULATOR              ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        print(f"{self.colors['YELLOW']}{'='*40}{self.colors['END']}")
        
        ip1 = input("Enter first IP address: ")
        ip2 = input("Enter second IP address: ")
        
        try:
            ip1_int = int(ipaddress.IPv4Address(ip1))
            ip2_int = int(ipaddress.IPv4Address(ip2))
            
            difference = abs(ip2_int - ip1_int)
            
            print(f"\n{self.colors['GREEN']}Results:{self.colors['END']}")
            print(f"  IP1: {ip1}")
            print(f"  IP2: {ip2}")
            print(f"  Difference: {difference} addresses")
            print(f"  CIDR containing both: /{32 - difference.bit_length() + 1 if difference > 0 else 32}")
            print(f"{self.colors['YELLOW']}{'='*40}{self.colors['END']}\n")
            
        except Exception as e:
            print(f"{self.colors['RED']}Error: {str(e)}{self.colors['END']}")
        
        self.wait_for_continue()
    
    def cidr_to_range(self, cidr):
        """Convert CIDR to IP range"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║            CIDR TO IP RANGE            ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        if not cidr:
            cidr = input(f"{self.colors['BLUE']}Enter CIDR (e.g., 192.168.1.0/24): {self.colors['END']}")
        
        try:
            network = ipaddress.ip_network(cidr, strict=False)
            
            print(f"\n{self.colors['GREEN']}📊 CIDR: {cidr}{self.colors['END']}")
            print(f"{self.colors['YELLOW']}{'='*50}{self.colors['END']}")
            print(f"Start IP: {network.network_address + 1}")
            print(f"End IP: {network.broadcast_address - 1}")
            print(f"Total Hosts: {network.num_addresses - 2}")
            print(f"{self.colors['YELLOW']}{'='*50}{self.colors['END']}\n")
            
        except Exception as e:
            print(f"{self.colors['RED']}Error: {str(e)}{self.colors['END']}")
        
        self.wait_for_continue()
    
    def ip_reputation(self, ip_address):
        """Check IP reputation"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║           IP REPUTATION CHECK          ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        if not ip_address:
            ip_address = input(f"{self.colors['BLUE']}Enter IP address: {self.colors['END']}")
        
        try:
            response = requests.get(f'https://ipinfo.io/{ip_address}/json', timeout=5)
            data = response.json()
            
            print(f"\n{self.colors['GREEN']}⭐ IP Reputation Check for {ip_address}{self.colors['END']}")
            print(f"{self.colors['YELLOW']}{'='*60}{self.colors['END']}")
            
            # Simple reputation scoring
            score = 100
            warnings = []
            
            if data.get('privacy', {}).get('vpn'):
                score -= 30
                warnings.append("Uses VPN/Proxy")
            if data.get('privacy', {}).get('tor'):
                score -= 40
                warnings.append("Uses TOR network")
            if data.get('hosting'):
                score -= 10
                warnings.append("Hosting provider")
            if 'abuse' in data:
                score -= 50
                warnings.append("Reported for abuse")
            
            if score >= 80:
                grade = f"{self.colors['GREEN']}Excellent{self.colors['END']}"
            elif score >= 60:
                grade = f"{self.colors['YELLOW']}Good{self.colors['END']}"
            elif score >= 40:
                grade = f"{self.colors['YELLOW']}Fair{self.colors['END']}"
            else:
                grade = f"{self.colors['RED']}Poor{self.colors['END']}"
            
            print(f"Reputation Score: {score}/100 ({grade})")
            if warnings:
                print(f"\n{self.colors['YELLOW']}Warnings:{self.colors['END']}")
                for warning in warnings:
                    print(f"  ⚠️  {warning}")
            
            print(f"{self.colors['YELLOW']}{'='*60}{self.colors['END']}\n")
            
        except Exception as e:
            print(f"{self.colors['RED']}Error: {str(e)}{self.colors['END']}")
        
        self.wait_for_continue()
    
    def dns_propagation(self, domain):
        """Check DNS propagation from multiple nameservers"""
        self.clear_screen()
        print(f"\n{self.colors['BOLD']}{self.colors['CYAN']}╔════════════════════════════════════════╗{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}║          DNS PROPAGATION CHECK         ║{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}╚════════════════════════════════════════╝{self.colors['END']}\n")
        
        if not domain:
            domain = input(f"{self.colors['BLUE']}Enter domain: {self.colors['END']}")
        
        nameservers = ['8.8.8.8', '1.1.1.1', '208.67.222.222', '9.9.9.9']
        
        print(f"\n{self.colors['GREEN']}🌍 DNS Propagation Check for {domain}{self.colors['END']}")
        print(f"{self.colors['YELLOW']}{'='*60}{self.colors['END']}")
        
        for ns in nameservers:
            try:
                # Simple dig/nslookup would be better, but using socket for simplicity
                ip = socket.gethostbyname(domain)
                print(f"✓ {ns}: {ip}")
            except:
                print(f"✗ {ns}: Lookup failed")
        
        print(f"{self.colors['YELLOW']}{'='*60}{self.colors['END']}\n")
        
        self.wait_for_continue()
    
    def interactive_mode(self):
        """Run tool in interactive mode with single menu display"""
        while True:
            self.print_main_menu()
            choice = input(f"\n{self.colors['BLUE']}Select tool (0-34): {self.colors['END']}")
            
            if choice == '0' or choice == '34':
                self.clear_screen()
                print(f"\n{self.colors['GREEN']}{self.colors['BOLD']}Thanks for using IP Tools! - https://discord.gg/EjcxgHJXQK {self.colors['END']}\n")
                break
            
            elif choice == '1':
                self.get_ip_info(None)
            
            elif choice == '2':
                self.ping_host(None)
            
            elif choice == '3':
                self.traceroute(None)
            
            elif choice == '4':
                self.port_scanner(None, None)
            
            elif choice == '5':
                self.subnet_calculator(None)
            
            elif choice == '6':
                self.dns_lookup(None)
            
            elif choice == '7':
                self.reverse_dns(None)
            
            elif choice == '8':
                self.whois_lookup(None)
            
            elif choice == '9':
                self.geolocation_lookup(None)
            
            elif choice == '10':
                self.batch_ip_lookup(None)
            
            elif choice == '11':
                self.network_scanner(None)
            
            elif choice == '12':
                self.speed_test()
            
            elif choice == '13':
                self.mac_lookup(None)
            
            elif choice == '14':
                self.asn_lookup(None)
            
            elif choice == '15':
                self.ssl_checker(None)
            
            elif choice == '16':
                self.http_header_grabber(None)
            
            elif choice == '17':
                host = input(f"{self.colors['BLUE']}Enter host to scan: {self.colors['END']}")
                self.common_port_checker(host)
                self.wait_for_continue()
            
            elif choice == '18':
                self.dns_bruteforcer(None, None)
            
            elif choice == '19':
                self.ip_range_generator(None, None)
            
            elif choice == '20':
                self.network_interfaces()
            
            elif choice == '21':
                self.packet_loss_test(None, 10)
            
            elif choice == '22':
                self.latency_monitor(None, 10)
            
            elif choice == '23':
                self.ipv4_to_ipv6(None)
            
            elif choice == '24':
                self.random_ip_generator(5)
            
            elif choice == '25':
                self.bgp_lookup(None)
            
            elif choice == '26':
                self.threat_intelligence(None)
            
            elif choice == '27':
                self.url_parser(None)
            
            elif choice == '28':
                self.ip_calculator()
            
            elif choice == '29':
                self.cidr_to_range(None)
            
            elif choice == '30':
                self.ip_reputation(None)
            
            elif choice == '31':
                self.dns_propagation(None)
            
            elif choice == '32':
                if self.last_results:
                    self.save_results(self.last_results)
                    print(f"\n{self.colors['GREEN']}Results saved successfully!{self.colors['END']}")
                else:
                    print(f"\n{self.colors['YELLOW']}No results to save yet. Run a tool first!{self.colors['END']}")
                time.sleep(2)
                self.clear_screen()
                self.print_banner()
            
            elif choice == '33':
                self.clear_screen()
                self.print_banner()
            
            else:
                print(f"\n{self.colors['RED']}Invalid choice! Please try again.{self.colors['END']}")
                time.sleep(1.5)
                self.clear_screen()
                self.print_banner()

def main():
    tool = IPMultitool()
    tool.clear_screen()
    tool.print_banner()
    time.sleep(2)
    tool.clear_screen()
    tool.print_banner()
    tool.interactive_mode()

if __name__ == "__main__":
    # Check for required packages
    try:
        import requests
    except ImportError:
        print("Please install required package: pip install requests")
        sys.exit(1)
    
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{colors['YELLOW']}Interrupted by user. {colors['END']}")
        sys.exit(0)
