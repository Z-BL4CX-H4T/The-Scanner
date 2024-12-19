# The-Scanner
"The-Scanner" is a Python-based tool designed to perform scanning and information gathering on a website. Its functions include various types of security scanning, information retrieval, and identifying potential vulnerabilities. Below is a brief explanation of its capabilities:

# 1. Whois Lookup
Retrieves detailed information about domain registration, such as registrar, creation date, expiration date, and name servers.
# 2. Geo-IP Lookup
Determines the geographical location of the server based on the target domain's IP address.
# 3. DNS Lookup
Displays DNS information of the domain, such as IP address, MX (Mail Exchange) records, and more.
# 4. Subdomain Scanner
Detects subdomains associated with the target domain, helping to uncover potential attack points.
# 5. Nmap Port Scan
Performs port scanning using Nmap to identify services running on the server.
# 6. SQLi Scanner
Examines the target website for potential SQL Injection vulnerabilities (manual validation required).
# 7. XSS Scanner
Scans for potential Cross-Site Scripting (XSS) vulnerabilities in the target web application (manual validation required).
# 8. Vulnerabilities Scan
Assesses common vulnerabilities on the server or web application (manual validation required).
# 9. Email Harvester
Collects email addresses associated with the target domain.
# 10. Reverse DNS Lookup
Retrieves domain names associated with a specific IP address.
# 11. SSL/TLS Certificate Info
Analyzes the SSL/TLS certificate used to determine its security.
# 12. HTTP Headers
Retrieves HTTP headers to examine server security and configuration information.
# 13. Crawl Website (Link Finder)
Crawls and analyzes links on the target website to identify its structure.
# 14. Run All Scans
Executes all the scans listed above simultaneously, providing a comprehensive report.

# Advantages
# Comprehensive Scanning:
Covers general and technical scanning capabilities.
# Simple and Modular: 
Each function can be run individually or all at once.
# Interactive Output:
Uses color coding to differentiate between positive, negative, or error results.

# Disadvantages
# Some Manual Scanning:
SQLi and XSS scans require manual validation.
# Dependency on External Tools:
Some functions rely on external tools like whois, nmap, and openssl.

# Note:

Ensure that all dependencies such as requests, subprocess, and external tools (e.g., nmap) are installed on the system before running this tool.
