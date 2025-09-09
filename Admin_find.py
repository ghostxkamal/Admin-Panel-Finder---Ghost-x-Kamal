#!/usr/bin/env python3
import requests
from urllib.parse import urljoin
from colorama import Fore, Style, init
import os
import shutil
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialize colorama
init(autoreset=True)

# Get terminal width
def get_terminal_width(default=80):
    try:
        return shutil.get_terminal_size().columns
    except:
        return default

# Centered print
def cprint(text, color=Fore.GREEN, bold=True):
    width = get_terminal_width()
    lines = text.split("\n")
    for line in lines:
        line_stripped = line.strip()
        if bold:
            print(color + Style.BRIGHT + line_stripped.center(width))
        else:
            print(color + line_stripped.center(width))

# Banner function
def banner():
    banner_lines = [
        "="*80,
        "𝓖𝓗𝓞𝓢𝓣 𝔁 𝓚𝓐𝓜𝓐𝓛",
        "-"*80,
        "Tool Name : Admin Panel Finder",
        "Tool Creator : Ghost x KAMAL",
        "="*80,
    ]
    cprint("\n".join(banner_lines), Fore.GREEN, bold=True)

# Default admin panel paths (simulate 1k+ entries)
default_paths = [
    "admin/", "administrator/", "admin1/", "admin2/", "admin3/", "admin/login.php",
    "admin/index.php", "adminpanel/", "cpanel/", "controlpanel/", "adm/", "admin_area/",
    "admin/login", "admin/index", "wp-admin/", "user/", "dashboard/", "login/", "manage/",
    "backend/", "cms/", "auth/", "secure/", "panel/", "system/", "root/", "administrator/login.php",
    "administrator/index.php", "admin/account.php", "admin/home.php", "admincp/", "memberadmin/",
    "members/", "staff/", "userpanel/", "moderator/", "moderatorcp/", "login_admin/", "loginpanel/",
    "webadmin/", "control/", "adminportal/", "portal/", "adminconsole/", "adminconfig/",
    "adminmanage/", "adminlogin/", "siteadmin/", "paneladmin/", "dashboard/login/",
    "dashboard/admin/", "backend/login/", "cpanel/login/", "secure/login/",
]

# Add pattern variations to simulate 1k+ entries
for i in range(0, 1000):
    default_paths.append(f"admin{i}/")
    default_paths.append(f"administrator{i}/")
    default_paths.append(f"login{i}/")
    default_paths.append(f"cpanel{i}/")
    default_paths.append(f"adm{i}/")
    default_paths.append(f"dashboard{i}/")
    default_paths.append(f"panel{i}/")

# URL normalization
def normalize_url(site: str) -> str:
    if not site.startswith("http://") and not site.startswith("https://"):
        site = "https://" + site
    if not site.endswith("/"):
        site += "/"
    return site

# HEAD first, fallback GET (SSL verify=False)
def check_url(url: str, headers: dict, timeout: int = 8):
    try:
        r = requests.head(url, headers=headers, timeout=timeout, allow_redirects=False, verify=False)
        return r.status_code
    except requests.RequestException:
        try:
            r = requests.get(url, headers=headers, timeout=timeout, allow_redirects=False, verify=False)
            return r.status_code
        except requests.RequestException:
            return None

# Main scanning function
def find_admin_panel(site, paths):
    site = normalize_url(site)
    print(Fore.CYAN + f"\n[*] Scanning for admin panel at: {site}\n")
    headers = {"User-Agent": "AdminPanelFinder/2.0 (safe for bug bounty)"}

    for path in paths:
        url = urljoin(site, path.strip())
        code = check_url(url, headers)

        if code:
            print(f"[*] Checking {url} --> {code}")
            if code in [200, 401, 403]:
                print(f"\n{Fore.GREEN}[!!!] Admin panel FOUND!{Style.RESET_ALL}")
                print(f"{Fore.GREEN}URL: {url}{Style.RESET_ALL}\n")
                return True
        else:
            print(f"{Fore.RED}[!] Error with {url}{Style.RESET_ALL}")

    print(f"\n{Fore.RED}[-] No admin panel found with the given paths.{Style.RESET_ALL}\n")
    return False

# Main
if __name__ == "__main__":
    banner()
    target = input(Fore.CYAN + "Enter target site (e.g. example.com): ").strip()
    mode = input(Fore.CYAN + "Do you want to use a wordlist? (y/n): ").strip().lower()

    if mode == "y":
        wordlist_path = input(Fore.CYAN + "Enter wordlist file path: ").strip()
        if os.path.exists(wordlist_path):
            with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
                wordlist_paths = [line.strip() for line in f if line.strip()]
            find_admin_panel(target, wordlist_paths)
        else:
            print(f"{Fore.RED}[!] Wordlist file not found. Exiting.{Style.RESET_ALL}")
    else:
        find_admin_panel(target, default_paths)
