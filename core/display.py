from colorama import Fore, Style, init
import os

init(autoreset=True)


def clear():
    os.system("cls")


def banner():
    clear()
    print(Fore.RED + Style.BRIGHT + r"""
    ____  __                 __              ______                    __  
   / __ \/ /_  ____ _____  / /_____  ____ _/_  __/________ ______  __/ /__
  / /_/ / __ \/ __ `/ __ \/ __/ __ \/ __ `/ / / / ___/ __ `/ ___/ / / //_/
 / ____/ / / / /_/ / / / / /_/ /_/ / /_/ / / / / /  / /_/ / /__  / / ,<   
/_/   /_/ /_/\__,_/_/ /_/\__/\____/\__, / /_/ /_/   \__,_/\___/_/ /_/|_|  
                                   /____/                                   
    """ + Style.RESET_ALL)
    print(Fore.WHITE + "  ┌──────────────────────────────────────────────┐")
    print(Fore.WHITE + "  │           OSINT Multi-Tool  v1.0             │")
    print(Fore.WHITE + "  │         github.com/duckings09/phantomtrack    │")
    print(Fore.WHITE + "  └──────────────────────────────────────────────┘\n")


def menu():
    banner()
    print(Fore.RED    + "  ── TRACKING ─────────────────────────────────")
    print(Fore.WHITE  + "  [1]  IP Lookup          — geo + VPN + ISP info")
    print(Fore.WHITE  + "  [2]  Link Generator      — Cloudflare grab link")
    print(Fore.RED    + "\n  ── OSINT ─────────────────────────────────────")
    print(Fore.WHITE  + "  [3]  Phone Lookup        — carrier + region + type")
    print(Fore.WHITE  + "  [4]  Username Lookup     — check across platforms")
    print(Fore.RED    + "\n  ── SYSTEM ────────────────────────────────────")
    print(Fore.WHITE  + "  [0]  Exit\n")
    return input(Fore.WHITE + "  → Select: ").strip()


def section(title: str):
    print(Fore.RED + Style.BRIGHT + f"\n  ── {title} " + "─" * (48 - len(title)))


def result_line(label: str, value: str, color=Fore.WHITE):
    print(f"  {Fore.RED}{label:<18}{color}{value}")


def divider():
    print(Fore.RED + "  " + "═" * 54)


def hit_header(timestamp: str):
    divider()
    print(Fore.RED + Style.BRIGHT + f"  HIT @ {timestamp}")
    divider()
