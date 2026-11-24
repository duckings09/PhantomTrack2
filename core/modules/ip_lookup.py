from core.intel import get_ip_intel, detect_vpn
from core.display import section, result_line, divider, clear, banner
from colorama import Fore


def run():
    clear()
    banner()
    section("IP LOOKUP")

    target = input(Fore.WHITE + "\n  → Enter IP address: ").strip()
    if not target:
        print(Fore.RED + "  [!] No IP entered.")
        input("\n  Press Enter to return...")
        return

    print(Fore.RED + "\n  [*] Querying...")
    intel = get_ip_intel(target)

    if not intel or intel.get("status") == "fail":
        print(Fore.RED + "  [!] Lookup failed. Check the IP and try again.")
        input("\n  Press Enter to return...")
        return

    vpn_detected, vpn_reason = detect_vpn(intel)
    vpn_label = (
        Fore.RED + f"DETECTED — {vpn_reason}"
        if vpn_detected
        else Fore.GREEN + "NOT DETECTED"
    )

    divider()
    result_line("IP",        target)
    result_line("VPN",       vpn_label)
    result_line("City",      f"{intel.get('city','?')}, {intel.get('regionName','?')}, {intel.get('country','?')}")
    result_line("ZIP",       intel.get("zip", "?"))
    result_line("Lat / Lon", f"{intel.get('lat','?')} / {intel.get('lon','?')}")
    result_line("Timezone",  intel.get("timezone", "?"))
    result_line("ISP",       intel.get("isp", "?"))
    result_line("Org",       intel.get("org", "?"))
    result_line("ASN",       intel.get("as", "?"))
    divider()

    input(Fore.WHITE + "\n  Press Enter to return...")
