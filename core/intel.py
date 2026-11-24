import requests

KNOWN_VPN_ASNs = {
    "AS9009", "AS20473", "AS14618", "AS16509", "AS15169", "AS8100",
    "AS60068", "AS396507", "AS205100", "AS212238", "AS63023", "AS13213",
    "AS60781", "AS24940", "AS51167",
}

KNOWN_VPN_KEYWORDS = [
    "vpn", "nordvpn", "expressvpn", "surfshark", "mullvad", "protonvpn",
    "ipvanish", "cyberghost", "privateinternetaccess", "pia", "hide.me",
    "tunnelbear", "windscribe", "hotspot shield", "astrill", "purevpn",
    "tor", "exit node", "relay", "anonymous", "privacy", "datacenter",
    "hosting", "colocation", "cloud", "linode", "digitalocean", "vultr",
    "hetzner", "ovh", "choopa", "peg tech", "m247", "quadranet",
]


def get_ip_intel(ip: str) -> dict:
    try:
        r = requests.get(
            f"http://ip-api.com/json/{ip}?fields=status,country,regionName,"
            f"city,zip,lat,lon,timezone,isp,org,as,proxy,hosting,query",
            timeout=5,
        )
        return r.json() if r.status_code == 200 else {}
    except Exception:
        return {}


def detect_vpn(intel: dict) -> tuple[bool, str]:
    reasons = []
    if intel.get("proxy"):
        reasons.append("ip-api proxy flag")
    if intel.get("hosting"):
        reasons.append("ip-api hosting flag")
    asn = intel.get("as", "").split(" ")[0].upper()
    if asn in KNOWN_VPN_ASNs:
        reasons.append(f"VPN/cloud ASN ({asn})")
    org_text = (intel.get("org", "") + " " + intel.get("isp", "")).lower()
    for kw in KNOWN_VPN_KEYWORDS:
        if kw in org_text:
            reasons.append(f"org keyword: '{kw}'")
            break
    return bool(reasons), "; ".join(reasons) if reasons else "none"
