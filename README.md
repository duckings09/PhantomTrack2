<div align="center">

# PhantomTrack

**OSINT multi-tool · Windows 11 · Terminal-based · No accounts · No config**

![Python](https://img.shields.io/badge/Python-3.11+-red?style=flat-square&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%2011-red?style=flat-square&logo=windows&logoColor=white)
![Cloudflare](https://img.shields.io/badge/Tunnel-Cloudflare-red?style=flat-square&logo=cloudflare&logoColor=white)

</div>

---

## Tools

| # | Tool | What it does |
|---|---|---|
| 1 | IP Lookup | Geo, VPN detection, ISP, ASN, coordinates |
| 2 | Link Generator | Cloudflare grab link — logs full fingerprint on click |
| 3 | Phone Lookup | Carrier, region, type, timezones from any number |
| 4 | Username Lookup | Checks 30+ platforms simultaneously |

---

## Requirements

- **Windows 11**
- **Python 3.11+** — https://www.python.org/downloads/
  - Tick **"Add Python to PATH"** during install

---

## Install

```bash
git clone https://github.com/duckings09/phantomtrack
cd phantomtrack
.\setup.bat
```

`setup.bat` automatically installs all dependencies and downloads `cloudflared.exe`.

---

## Run

```bash
.\run.bat
```

---

## Tool Details

### [1] IP Lookup
Enter any IP address. Returns full geo, VPN/proxy detection, ISP, org, ASN.

### [2] Link Generator
Generates a Cloudflare tracking link. When someone clicks it you get:

| Field | Detail |
|---|---|
| IP | Real IP via Cloudflare header |
| VPN | Detected / Not Detected + reason |
| Location | City, region, country, ZIP |
| Coordinates | Lat / Lon |
| Timezone | Full string |
| ISP & ASN | Provider + network ID |
| OS | Windows / Android / iOS / macOS |
| Browser | Chrome / Firefox / Safari / Edge |
| Device | Desktop / Mobile / Tablet |
| Language | Accept-Language header |
| Referer | Where they clicked from |

Hits print live and save to `hits.json`.

### [3] Phone Lookup
Enter any number in international format e.g. `+12025551234`. Returns carrier, region, line type, timezones, validity.

### [4] Username Lookup
Enter a username. Checks 30+ platforms simultaneously including GitHub, Instagram, TikTok, Reddit, Twitch, Steam, Telegram, Roblox and more.

---

## File Structure

```
phantomtrack/
├── README.md
├── requirements.txt
├── setup.bat                  <- run once
├── run.bat                    <- run every time
└── core/
    ├── main.py                <- menu + router
    ├── display.py             <- terminal UI
    ├── intel.py               <- IP geo + VPN engine
    ├── grabber.py             <- Flask tracker
    ├── tunnel.py              <- Cloudflare tunnel
    └── modules/
        ├── ip_lookup.py
        ├── link_gen.py
        ├── phone_lookup.py
        └── username_lookup.py
```

---

## Notes

- Cloudflare tunnel URL changes every session
- Hits save to `hits.json` automatically
- `cloudflared.exe` and `hits.json` are gitignored
