import subprocess
import re
import os
from colorama import Fore


def start_cloudflare_tunnel(port: int) -> str:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    local = os.path.join(root, "cloudflared.exe")
    cf_binary = local if os.path.exists(local) else "cloudflared"

    print(Fore.RED + "  [*] Starting Cloudflare tunnel...")

    proc = subprocess.Popen(
        [cf_binary, "tunnel", "--url", f"http://localhost:{port}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    for line in iter(proc.stdout.readline, ""):
        match = re.search(r"https://[a-zA-Z0-9\-]+\.trycloudflare\.com", line)
        if match:
            return match.group(0)

    return "tunnel_failed"
