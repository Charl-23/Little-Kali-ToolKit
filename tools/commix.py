import os
import sys
import subprocess
from colorama import Fore, init

init(autoreset=True)

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    print(Fore.GREEN + r"""  

        	  ▘                                
	▛▘▛▌▛▛▌▛▛▌▌▚▘                              
	▙▖▙▌▌▌▌▌▌▌▌▞▖                              
                                           
                    ▌   ▜ ▘  ▗     ▜ ▌     
                    ▙▘▀▌▐ ▌▄▖▜▘▛▌▛▌▐ ▛▌▛▌▚▘
                    ▛▖█▌▐▖▌  ▐▖▙▌▙▌▐▖▙▌▙▌▞▖
                                           
	▄▖▖▖▄▖▖▖▄▖                                 
	▌ ▙▌▛▌▙▌▌                                  
	▙▖ ▌█▌ ▌▙▖

    """)
    print(Fore.RED + "        COMMIX AUTOMATION TOOL  |  by C404C")
    print(Fore.RED + "           https://github.com/Charl-23\n")
    print(Fore.RED + "  " + "─" * 52 + "\n")

def get_level():
    print(Fore.GREEN + "[?] Choisir le niveau d'injection (--level) :")
    print(Fore.WHITE + "    [1] Level 1 — Standard")
    print(Fore.WHITE + "    [2] Level 2 — Approfondi")
    print(Fore.WHITE + "    [3] Level 3 — Agressif")
    while True:
        choice = input(Fore.CYAN + "\n[>] Votre choix (1/2/3) : ").strip()
        if choice in ("1", "2", "3"):
            return choice
        print(Fore.RED + "[-] Choix invalide, entrez 1, 2 ou 3.")

def main():
    clear()
    banner()

    url = input(Fore.GREEN + "[?] Entrez l'URL cible : ").strip()
    if not url:
        print(Fore.RED + "[-] L'URL ne peut pas être vide.")
        sys.exit(1)

    print()

    level = get_level()

    print(Fore.RED + "\n  ┌─ CONFIGURATION ────────────────────────────┐")
    print(Fore.RED + f"  │  URL   : " + Fore.WHITE + f"{url}")
    print(Fore.RED + f"  │  Level : " + Fore.WHITE + f"{level}")
    print(Fore.RED + "  └────────────────────────────────────────────┘\n")

    confirm = input(Fore.GREEN + "[?] Lancer commix ? (o/n) : ").strip().lower()
    if confirm not in ("o", "oui", "y", "yes"):
        print(Fore.RED + "\n[-] Annulé.")
        sys.exit(0)

    cmd = ["commix", "-u", url, "--level", level]

    print(Fore.GREEN + f"\n[+] Exécution : commix -u {url} --level {level}\n")
    print(Fore.RED + "  " + "─" * 52 + "\n")

    try:
        subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n[!] Interrompu par l'utilisateur.")
    except FileNotFoundError:
        print(Fore.RED + "[-] Commix introuvable. Est-il installé et dans le PATH ?")

if __name__ == "__main__":
    main()
