from core.display import section, result_line, divider, clear, banner
from colorama import Fore

try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone as pn_timezone
    HAS_PHONENUMBERS = True
except ImportError:
    HAS_PHONENUMBERS = False


def run():
    clear()
    banner()
    section("PHONE LOOKUP")

    if not HAS_PHONENUMBERS:
        print(Fore.RED + "  [!] phonenumbers not installed. Run setup.bat.")
        input("\n  Press Enter to return...")
        return

    print(Fore.WHITE + "\n  Enter phone number in international format.")
    print(Fore.WHITE + "  Example: +12025551234  or  +447911123456\n")
    raw = input(Fore.WHITE + "  → Phone number: ").strip()

    try:
        parsed = phonenumbers.parse(raw)
    except Exception as e:
        print(Fore.RED + f"\n  [!] Could not parse number: {e}")
        input("\n  Press Enter to return...")
        return

    valid   = phonenumbers.is_valid_number(parsed)
    possible = phonenumbers.is_possible_number(parsed)

    region      = geocoder.description_for_number(parsed, "en")
    carrier_name = carrier.name_for_number(parsed, "en")
    timezones   = pn_timezone.time_zones_for_number(parsed)
    num_type    = phonenumbers.number_type(parsed)
    formatted_e164   = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    formatted_intl   = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    formatted_natl   = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
    country_code = parsed.country_code
    national_num = parsed.national_number

    type_map = {
        0: "FIXED_LINE",
        1: "MOBILE",
        2: "FIXED_LINE_OR_MOBILE",
        3: "TOLL_FREE",
        4: "PREMIUM_RATE",
        5: "SHARED_COST",
        6: "VOIP",
        7: "PERSONAL_NUMBER",
        8: "PAGER",
        9: "UAN",
        10: "VOICEMAIL",
        99: "UNKNOWN",
    }
    type_str = type_map.get(num_type, "UNKNOWN")

    divider()
    result_line("Input",        raw)
    result_line("E164",         formatted_e164)
    result_line("International",formatted_intl)
    result_line("National",     formatted_natl)
    result_line("Country Code", f"+{country_code}")
    result_line("National Num", str(national_num))
    result_line("Valid",        Fore.GREEN + "YES" if valid else Fore.RED + "NO")
    result_line("Possible",     Fore.GREEN + "YES" if possible else Fore.RED + "NO")
    result_line("Type",         type_str)
    result_line("Region",       region if region else "Unknown")
    result_line("Carrier",      carrier_name if carrier_name else "Unknown")
    result_line("Timezones",    ", ".join(timezones) if timezones else "Unknown")
    divider()

    input(Fore.WHITE + "\n  Press Enter to return...")
