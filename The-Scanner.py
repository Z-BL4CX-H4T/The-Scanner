import os
import socket
import subprocess
import requests
from urllib.parse import urlparse

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_green(text):
    print(f"\033[92m{text}\033[0m")

def print_red(text):
    print(f"\033[91m{text}\033[0m")

def print_white(text):
    print(f"\033[97m{text}\033[0m")

def print_yellow(text):
    print(f"\033[93m{text}\033[0m")

def print_bold(text):
    print(f"\033[36m{text}\033[0m")

def update():
    print_red("\n[+] The-Scanner UPDATE UTILITY [+]")
    print("Update sedang berlangsung, harap tunggu...")
    os.system("git fetch origin && git reset --hard origin/master && git clean -f -d")
    print_green("[i] Pembaruan selesai! Silakan restart The-Scanner.")
    exit()

def check_dependencies():
    try:
        import requests
    except ImportError:
        print_red("\n[!] Modul requests tidak ditemukan! Harap instal terlebih dahulu.")
        exit()

def show_help():
    print_bold("[+] The-Scanner Help Screen [+]")
    print_white("""
    1. help: Menampilkan Menu Bantuan
    2. fix: Menginstal Modul yang Dibutuhkan
    3. URL: Memasukkan Domain yang Akan Dipindai
    4. update: Memperbarui The-Scanner ke Versi Terbaru
    5. all: Menjalankan Semua Pemindaian Sekaligus
    """)

def fix_modules():
    print_red("[+] Memperbaiki Modul yang Dibutuhkan [+]")
    os.system("sudo apt-get install python3-requests")

def check_hostalive(website):
    try:
        socket.gethostbyname(website)
        return True
    except socket.error:
        return False

def action_menu(website):
    print_green("""
___       ___     __   __                  ___  __  
 |  |__| |__  __ /__` /  `  /\  |\ | |\ | |__  |__) 
 |  |  | |___    .__/ \__, /~~\ | \| | \| |___ |  \ 
""")                                                    
    print_white("\nPilih tindakan yang ingin Anda lakukan:")
    print_bold("[1] Whois Lookup")
    print_bold("[2] Geo-IP Lookup")
    print_bold("[3] DNS Lookup")
    print_bold("[4] Subdomain Scanner")
    print_bold("[5] Nmap Port Scan")
    print_bold("[6] SQLi Scanner")
    print_bold("[7] XSS Scanner")
    print_bold("[8] Vulnerabilities Scan")
    print_bold("[9] Email Harvester")
    print_bold("[10] Reverse DNS Lookup")
    print_bold("[11] SSL/TLS Certificate Info")
    print_bold("[12] HTTP Headers")
    print_bold("[13] Crawl Website (Link Finder)")
    print_bold("[A] Jalankan Semua Pemindaian")
    print_bold("[Q] Keluar")

    choice = input("Pilih aksi (1-13, A, Q): ").strip().lower()

    if choice == "1":
        whois_lookup(website)
    elif choice == "2":
        geo_ip_lookup(website)
    elif choice == "3":
        dns_lookup(website)
    elif choice == "4":
        subdomain_scan(website)
    elif choice == "5":
        nmap_scan(website)
    elif choice == "6":
        sqli_scan(website)
    elif choice == "7":
        xss_scan(website)
    elif choice == "8":
        vulnerabilities_scan(website)
    elif choice == "9":
        email_harvester(website)
    elif choice == "10":
        reverse_dns_lookup(website)
    elif choice == "11":
        ssl_tls_info(website)
    elif choice == "12":
        http_headers(website)
    elif choice == "13":
        crawl_website(website)
    elif choice == "a":
        run_all_scans(website)
    elif choice == "q":
        print("\nKeluar dari The-Scanner.")
        exit()

def make_request(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print_red(f"[!] Terjadi kesalahan dengan status kode: {response.status_code}")
            return None
        return response.text
    except requests.exceptions.RequestException as e:
        print_red(f"[!] Terjadi kesalahan dalam permintaan API: {str(e)}")
        return None

def whois_lookup(website):
    print_bold(f"\n[+] Melakukan Whois Lookup untuk {website}\033[1;32m")
    command = f"whois {website}"
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if result.returncode == 0:
        print_white(result.stdout.decode())
    else:
        print_red("[!] Gagal mendapatkan informasi Whois.")

def geo_ip_lookup(website):
    print_bold(f"\n[+] Melakukan Geo-IP Lookup untuk {website}\033[1;32m")
    command = f"dig +short {website}"
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if result.returncode == 0:
        print_white(result.stdout.decode())
    else:
        print_red("[!] Gagal mendapatkan informasi Geo-IP.")

def dns_lookup(website):
    print_bold(f"\n[+] Melakukan DNS Lookup untuk {website}\033[1;32m")
    command = f"dig {website}"
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if result.returncode == 0:
        print_white(result.stdout.decode())
    else:
        print_red("[!] Gagal mendapatkan informasi DNS.")

def subdomain_scan(website):
    print_bold(f"\n[+] Melakukan Subdomain Scan untuk {website}\033[1;32m")
    url = f"https://crt.sh/?q=%.{website}&output=json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            subdomains = {entry['name_value'] for entry in data}
            if subdomains:
                print_green(f"\n[+] Subdomain ditemukan untuk {website}:")
                for sub in sorted(subdomains):
                    print_white(sub)
            else:
                print_red("[!] Tidak ada subdomain yang ditemukan.")
        else:
            print_red(f"[!] Gagal mengambil subdomain. Status kode: {response.status_code}")
    except Exception as e:
        print_red(f"[!] Error: {str(e)}")

def nmap_scan(website):
    print_bold(f"\n[+] Melakukan Nmap Port Scan untuk {website}")
    command = f"nmap {website}"
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if result.returncode == 0:
        print_white(result.stdout.decode())
    else:
        print_red("[!] Gagal melakukan pemindaian Nmap.")

def sqli_scan(website):
    print_bold(f"\n[+] Melakukan SQLi Scan untuk {website}")
    print_red("[!] SQLi scan membutuhkan pemeriksaan manual!")

def xss_scan(website):
    print_bold(f"\n[+] Melakukan XSS Scan untuk {website}")
    print_red("[!] XSS scan membutuhkan pemeriksaan manual!")

def vulnerabilities_scan(website):
    print_bold(f"\n[+] Melakukan Pemindaian Kerentanannya untuk {website}")
    print_red("[!] Kerentanannya harus diperiksa secara manual!")

def email_harvester(website):
    print_bold(f"\n[+] Melakukan Email Harvester untuk {website}")
    command = f"harvester -d {website} -b google"
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if result.returncode == 0:
        print_white(result.stdout.decode())
    else:
        print_red("[!] Gagal menemukan alamat email.")

def reverse_dns_lookup(website):
    print_bold(f"\n[+] Melakukan Reverse DNS Lookup untuk {website}")
    command = f"dig -x {website}"
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if result.returncode == 0:
        print_white(result.stdout.decode())
    else:
        print_red("[!] Gagal melakukan Reverse DNS Lookup.")

def ssl_tls_info(website):
    print_bold(f"\n[+] Melakukan Informasi SSL/TLS untuk {website}")
    command = f"echo | openssl s_client -connect {website}:443"
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if result.returncode == 0:
        print_white(result.stdout.decode())
    else:
        print_red("[!] Gagal mendapatkan informasi SSL/TLS.")

def http_headers(website):
    print_bold(f"\n[+] Melakukan HTTP Headers Scan untuk {website}")
    command = f"curl -I {website}"
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if result.returncode == 0:
        print_white(result.stdout.decode())
    else:
        print_red("[!] Gagal mendapatkan HTTP Headers.")

def crawl_website(website):
    print_bold(f"\n[+] Memulai Crawl Website untuk {website}")
    command = f"wget --spider --recursive --no"
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if result.returncode == 0:
        print_white(result.stdout.decode())
    else:
        print_red("[!] Gagal melakukan crawl website.")

def run_all_scans(website):
    print_bold(f"\n[+] Menjalankan semua pemindaian untuk {website}...\n")
    whois_lookup(website)
    geo_ip_lookup(website)
    dns_lookup(website)
    subdomain_scan(website)
    nmap_scan(website)
    sqli_scan(website)
    xss_scan(website)
    vulnerabilities_scan(website)
    email_harvester(website)
    reverse_dns_lookup(website)
    ssl_tls_info(website)
    http_headers(website)
    crawl_website(website)

def main():
    clear_screen()
    print_bold("[+] The-Scanner - Pemindai Website oleh MR P3T0K [+]")
    print_green("""
___       ___     __   __                  ___  __  
 |  |__| |__  __ /__` /  `  /\  |\ | |\ | |__  |__) 
 |  |  | |___    .__/ \__, /~~\ | \| | \| |___ |  \ 
""")                                                    
    check_dependencies()

    while True:
        print_white("\nMasukkan Website yang ingin Anda pindai (tanpa http/https):")
        website = input("URL: ").strip()

        if website == "help":
            show_help()
        elif website == "fix":
            fix_modules()
        elif website == "update":
            update()
        elif website == "q":
            print("\nKeluar dari The-Scanner.")
            break
        elif website == "all":
            run_all_scans(website)
        else:
            if not check_hostalive(website):
                print_red(f"[!] Website {website} tidak dapat dijangkau. Cek koneksi internet atau pastikan website valid.")
            else:
                action_menu(website)

if __name__ == "__main__":
    main()
