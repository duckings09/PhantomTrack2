import sys
import time
from colorama import Fore
from core.display import menu, clear


def main():
    while True:
        choice = menu()

        if choice == "1":
            from core.modules import ip_lookup
            ip_lookup.run()

        elif choice == "2":
            from core.modules import link_gen
            link_gen.run()

        elif choice == "3":
            from core.modules import phone_lookup
            phone_lookup.run()

        elif choice == "4":
            from core.modules import username_lookup
            username_lookup.run()

        elif choice == "0":
            clear()
            print(Fore.RED + "\n  Exiting PhantomTrack.\n")
            sys.exit(0)

        else:
            print(Fore.RED + "  [!] Invalid option.")
            time.sleep(1)


if __name__ == "__main__":
    main()
