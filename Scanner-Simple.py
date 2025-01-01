import socket
import requests
import asyncio
from rich.console import Console
from rich.table import Table
from colorama import Fore, init
from urllib.parse import urlparse

init(autoreset=True)
console = Console()

# ASCII logo Z-BL4CX-H4T
ascii_logo = """
████████ ██   ██ ███████     ███████  ██████  █████  ███    ██ ███    ██ ███████ ██████
   ██    ██   ██ ██          ██      ██      ██   ██ ████   ██ ████   ██ ██      ██   ██
   ██    ███████ █████ █████ ███████ ██      ███████ ██ ██  ██ ██ ██  ██ █████   ██████
   ██    ██   ██ ██               ██ ██      ██   ██ ██  ██ ██ ██  ██ ██ ██      ██   ██
   ██    ██   ██ ███████     ███████  ██████ ██   ██ ██   ████ ██   ████ ███████ ██   ██
    V.0.6 Created By: Mr.Petok Team:Z-BL4CX-H4T
"""

# Fungsi untuk mendapatkan subdomain
def find_subdomains(domain):
    subdomains = []
    try:
        response = requests.get(f"https://crt.sh/?q={domain}&output=json", timeout=5)
        if response.status_code == 200:
            data = response.json()
            subdomains = list(set(item['name_value'] for item in data))
            subdomains = [sub.replace('*.', '').encode('ascii', 'ignore').decode() for sub in subdomains]
    except Exception:
        pass
    return subdomains if subdomains else ["No subdomains found"]

# Pemindaian port paralel
async def scan_port(ip, port):
    try:
        reader, writer = await asyncio.open_connection(ip, port)
        writer.close()
        await writer.wait_closed()
        return port
    except:
        return None

async def check_ports(ip, ports):
    tasks = [scan_port(ip, port) for port in ports]
    results = await asyncio.gather(*tasks)
    return [port for port in results if port]

# Fungsi untuk mendeteksi WAF, CDN, CAPTCHA, dan Cloudflare
def check_security(domain):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        response = requests.get(f"http://{domain}", headers=headers, timeout=5)
        waf, cdn, captcha, cloudflare = "No WAF detected", "No CDN detected", "No CAPTCHA detected", "No Cloudflare Protection"

        # Deteksi WAF
        if "cf-ray" in response.headers:
            waf = "Cloudflare WAF detected"
        elif "x-sucuri-id" in response.headers:
            waf = "Sucuri WAF detected"

        # Deteksi CDN
        if "cf-cache-status" in response.headers:
            cdn = "Cloudflare CDN detected"
        elif "x-akamai-request-id" in response.headers:
            cdn = "Akamai CDN detected"

        # Deteksi CAPTCHA
        if "captcha" in response.text.lower():
            captcha = "CAPTCHA detected"

        # Deteksi Cloudflare Protection
        if "cf-ray" in response.headers or "Server" in response.headers and "cloudflare" in response.headers["Server"].lower():
            cloudflare = "Cloudflare Protection detected"

        return waf, cdn, captcha, cloudflare
    except Exception:
        return "Error detecting WAF", "Error detecting CDN", "Error detecting CAPTCHA", "Error detecting Cloudflare"

# Fungsi untuk mendapatkan informasi DNS
def get_dns_info(domain):
    try:
        parsed_url = urlparse(f"http://{domain}")
        host = parsed_url.netloc or parsed_url.path
        dns_info = socket.gethostbyname_ex(host)
        return dns_info[2]
    except:
        return ["Error resolving DNS"]

# Fungsi utama
def main():
    # Tampilkan ASCII logo alat
    console.print(Fore.CYAN + ascii_logo)

    # Input target dari pengguna
    domain = input(Fore.YELLOW + "Masukkan TARGET (contoh: www.example.com): ").strip()
    console.print("\nMengambil informasi...", style="cyan")

    # Resolusi DNS
    try:
        ip = socket.gethostbyname(domain)
    except:
        console.print("[bold red]Gagal menemukan IP untuk target[/]")
        return

    # Pemindaian port
    ports = asyncio.run(check_ports(ip, [80, 443]))

    # Enumerasi subdomain
    subdomains = find_subdomains(domain)

    # Deteksi WAF, CDN, CAPTCHA, dan Cloudflare
    waf, cdn, captcha, cloudflare = check_security(domain)

    # Informasi DNS tambahan
    dns_records = get_dns_info(domain)

    # Tampilkan hasil
    data = {
        "TARGET": domain,
        "IP": ip,
        "Ports": " | ".join(map(str, ports)) if ports else "No open ports detected",
        "WAF": waf,
        "CDN": cdn,
        "CAPTCHA": captcha,
        "Cloudflare": cloudflare,
        "Subdomains": ", ".join(subdomains),
        "DNS Records": ", ".join(dns_records),
    }

    # Menampilkan data dalam format tabel
    table = Table(title="Target Information")
    table.add_column("Key", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")
    for key, value in data.items():
        table.add_row(key, value)
    console.print(table)

if __name__ == "__main__":
    main()
