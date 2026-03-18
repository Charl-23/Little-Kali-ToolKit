import os
import sys
import subprocess
from colorama import Fore, init

init(autoreset=True)

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    print(Fore.GREEN + r"""

	▄▖▄▖▄▖▄▖▄▖▖ ▖▖▄▖▄▖                         
	▚ ▙▖▐ ▌▌▌▌▌ ▙▘▐ ▐                          
	▄▌▙▖▐ ▙▌▙▌▙▖▌▌▟▖▐                          
                                           
                    ▌   ▜ ▘  ▗     ▜ ▌     
                    ▙▘▀▌▐ ▌▄▖▜▘▛▌▛▌▐ ▛▌▛▌▚▘
                    ▛▖█▌▐▖▌  ▐▖▙▌▙▌▐▖▙▌▙▌▞▖
                                           
	▄▖▖▖▄▖▖▖▄▖                                 
	▌ ▙▌▛▌▙▌▌                                  
	▙▖ ▌█▌ ▌▙▖

    """)
    print(Fore.RED + "        SETOOLKIT AUTOMATION TOOL  |  by C404C")
    print(Fore.RED + "              https://github.com/Charl-23\n")
    print(Fore.RED + "  " + "─" * 54 + "\n")

def main():
    clear()
    banner()

    if os.geteuid() != 0:
        print(Fore.RED + "[!] Ce script doit être exécuté en tant que root (sudo).\n")
        sys.exit(1)

    print(Fore.GREEN + "[+] Commande : sudo setoolkit\n")

    confirm = input(Fore.GREEN + "[?] Lancer SET ? (o/n) : ").strip().lower()
    if confirm not in ("o", "oui", "y", "yes"):
        print(Fore.RED + "\n[-] Annulé.")
        sys.exit(0)

    print(Fore.RED + "\n  " + "─" * 54 + "\n")

    try:
        subprocess.run(["setoolkit"], check=False)
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n[!] Interrompu par l'utilisateur.")
    except FileNotFoundError:
        print(Fore.RED + "[-] SET introuvable. Est-il installé et dans le PATH ?")

if __name__ == "__main__":
    main()
