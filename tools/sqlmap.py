import os
import sys
import subprocess
from colorama import Fore, init

init(autoreset=True)

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    print(Fore.GREEN + r"""
	▄▖▄▖▖                                      
	▚ ▌▌▌ ▛▛▌▀▌▛▌                              
	▄▌█▌▙▖▌▌▌█▌▙▌                              
	   ▘       ▌                               
                    ▌   ▜ ▘  ▗     ▜ ▌     
                    ▙▘▀▌▐ ▌▄▖▜▘▛▌▛▌▐ ▛▌▛▌▚▘
                    ▛▖█▌▐▖▌  ▐▖▙▌▙▌▐▖▙▌▙▌▞▖
                                           
	▄▖▖▖▄▖▖▖▄▖                                 
	▌ ▙▌▛▌▙▌▌                                  
	▙▖ ▌█▌ ▌▙
    """)
    print(Fore.RED + "           SQLMAP AUTOMATION TOOL  |  by C404C")
    print(Fore.RED + "              https://github.com/Charl-23\n")
    print(Fore.RED + "  " + "─" * 54 + "\n")

def get_level():
    print(Fore.GREEN + "[?] Choisir le niveau de détection (--level) :")
    print(Fore.WHITE + "    [1] Level 1 — Standard  (requêtes basiques)")
    print(Fore.WHITE + "    [2] Level 2 — Approfondi (cookies, user-agent)")
    print(Fore.WHITE + "    [3] Level 3 — Agressif   (tous les vecteurs)")
    while True:
        choice = input(Fore.GREEN + "\n[>] Votre choix (1/2/3) : ").strip()
        if choice in ("1", "2", "3"):
            return choice
        print(Fore.RED + "[-] Choix invalide, entrez 1, 2 ou 3.")

def get_enumeration():
    print(Fore.GREEN + "\n[?] Choisir l'énumération (--banner activé) :")
    print(Fore.WHITE + "    [1] Enum 1 — Basique   (--dbs)")
    print(Fore.WHITE + "    [2] Enum 2 — Étendue   (--dbs --tables --columns)")
    print(Fore.WHITE + "    [3] Enum 3 — Complète  (--dbs --tables --columns --dump)")
    enum_flags = {
        "1": ["--dbs"],
        "2": ["--dbs", "--tables", "--columns"],
        "3": ["--dbs", "--tables", "--columns", "--dump"],
    }
    while True:
        choice = input(Fore.GREEN + "\n[>] Votre choix (1/2/3) : ").strip()
        if choice in ("1", "2", "3"):
            return enum_flags[choice]
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

    enum_flags = []
    if level in ("2", "3"):
        enum_flags = get_enumeration()

    cmd = ["sqlmap", "-u", url, f"--level={level}"]
    if level in ("2", "3"):
        cmd += ["--banner"] + enum_flags

    print(Fore.RED + "\n  ┌─ CONFIGURATION ──────────────────────────────┐")
    print(Fore.RED + f"  │  URL    : " + Fore.WHITE + f"{url}")
    print(Fore.RED + f"  │  Level  : " + Fore.WHITE + f"{level}")
    if level in ("2", "3"):
        print(Fore.RED + f"  │  Enum   : " + Fore.WHITE + f"--banner {' '.join(enum_flags)}")
    else:
        print(Fore.RED + f"  │  Enum   : " + Fore.WHITE + "désactivée (level 1)")
    print(Fore.RED + "  └──────────────────────────────────────────────┘")

    print(Fore.GREEN + f"\n[+] Commande : {' '.join(cmd)}\n")

    confirm = input(Fore.GREEN + "[?] Lancer sqlmap ? (o/n) : ").strip().lower()
    if confirm not in ("o", "oui", "y", "yes"):
        print(Fore.RED + "\n[-] Annulé.")
        sys.exit(0)

    print(Fore.RED + "\n  " + "─" * 54 + "\n")

    try:
        subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n[!] Interrompu par l'utilisateur.")
    except FileNotFoundError:
        print(Fore.RED + "[-] SQLMap introuvable. Est-il installé et dans le PATH ?")

if __name__ == "__main__":
    main()
