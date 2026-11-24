import requests
import threading
from core.display import section, divider, clear, banner
from colorama import Fore, Style

# Platforms to check — url must contain {} for the username
PLATFORMS = {
    "GitHub":          "https://github.com/{}",
    "Twitter/X":       "https://twitter.com/{}",
    "Instagram":       "https://www.instagram.com/{}",
    "TikTok":          "https://www.tiktok.com/@{}",
    "Reddit":          "https://www.reddit.com/user/{}",
    "Twitch":          "https://www.twitch.tv/{}",
    "YouTube":         "https://www.youtube.com/@{}",
    "Pinterest":       "https://www.pinterest.com/{}",
    "Snapchat":        "https://www.snapchat.com/add/{}",
    "Telegram":        "https://t.me/{}",
    "Steam":           "https://steamcommunity.com/id/{}",
    "Pastebin":        "https://pastebin.com/u/{}",
    "Replit":          "https://replit.com/@{}",
    "GitLab":          "https://gitlab.com/{}",
    "Linktree":        "https://linktr.ee/{}",
    "Cashapp":         "https://cash.app/${}",
    "Roblox":          "https://www.roblox.com/user.aspx?username={}",
    "Chess.com":       "https://www.chess.com/member/{}",
    "Duolingo":        "https://www.duolingo.com/profile/{}",
    "Spotify":         "https://open.spotify.com/user/{}",
    "SoundCloud":      "https://soundcloud.com/{}",
    "Kick":            "https://kick.com/{}",
    "Rumble":          "https://rumble.com/user/{}",
    "Trello":          "https://trello.com/{}",
    "Keybase":         "https://keybase.io/{}",
    "HackerNews":      "https://news.ycombinator.com/user?id={}",
    "ProductHunt":     "https://www.producthunt.com/@{}",
    "Medium":          "https://medium.com/@{}",
    "Dev.to":          "https://dev.to/{}",
    "Codecademy":      "https://www.codecademy.com/profiles/{}",
}

results = {}
lock = threading.Lock()


def _check(platform: str, url: str, username: str):
    target = url.format(username)
    try:
        r = requests.get(
            target,
            timeout=6,
            headers={"User-Agent": "Mozilla/5.0"},
            allow_redirects=True,
        )
        found = r.status_code == 200 and username.lower() in r.text.lower()
        with lock:
            results[platform] = (found, target)
    except Exception:
        with lock:
            results[platform] = (False, target)


def run():
    global results
    results = {}

    clear()
    banner()
    section("USERNAME LOOKUP")

    username = input(Fore.WHITE + "\n  → Username: ").strip()
    if not username:
        print(Fore.RED + "  [!] No username entered.")
        input("\n  Press Enter to return...")
        return

    print(Fore.RED + f"\n  [*] Scanning {len(PLATFORMS)} platforms for '{username}'...\n")

    threads = []
    for platform, url in PLATFORMS.items():
        t = threading.Thread(target=_check, args=(platform, url, username))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    found_list   = [(p, u) for p, (f, u) in sorted(results.items()) if f]
    missing_list = [(p, u) for p, (f, u) in sorted(results.items()) if not f]

    divider()
    print(Fore.GREEN + Style.BRIGHT + f"  FOUND ({len(found_list)})")
    divider()
    for platform, url in found_list:
        print(Fore.GREEN + f"  [+] {platform:<20} {Fore.WHITE}{url}")

    if not found_list:
        print(Fore.WHITE + "  None found.")

    print()
    divider()
    print(Fore.RED + Style.BRIGHT + f"  NOT FOUND ({len(missing_list)})")
    divider()
    for platform, url in missing_list:
        print(Fore.RED + f"  [-] {platform:<20} {Fore.WHITE}{url}")

    divider()
    input(Fore.WHITE + "\n  Press Enter to return...")
