import os
import sys
import subprocess
from colorama import Fore, init

init(autoreset=True)

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    print(Fore.GREEN + r"""
	   ▘▐▘▘▗                                   
	▌▌▌▌▜▘▌▜▘█▌                                
	▚▚▘▌▐ ▌▐▖▙▖                                
                                           
                    ▌   ▜ ▘  ▗     ▜ ▌     
                    ▙▘▀▌▐ ▌▄▖▜▘▛▌▛▌▐ ▛▌▛▌▚▘
                    ▛▖█▌▐▖▌  ▐▖▙▌▙▌▐▖▙▌▙▌▞▖
                                           
	▄▖▖▖▄▖▖▖▄▖                                 
	▌ ▙▌▛▌▙▌▌                                  
	▙▖ ▌█▌ ▌▙▖ 
    """)
    print(Fore.RED + "           WIFITE AUTOMATION TOOL  |  by C404C")
    print(Fore.RED + "              https://github.com/Charl-23\n")
    print(Fore.RED + "  " + "─" * 54 + "\n")

def get_wordlist():
    print(Fore.GREEN + "[?] Entrez le chemin vers votre wordlist (--dict) :")
    print(Fore.WHITE + "    Exemple : /usr/share/wordlists/rockyou.txt")
    while True:
        path = input(Fore.GREEN + "\n[>] Chemin wordlist : ").strip()
        if not path:
            print(Fore.RED + "[-] Le chemin ne peut pas être vide.")
            continue
        if not os.path.isfile(path):
            print(Fore.RED + f"[!] Fichier introuvable : {path}")
            retry = input(Fore.GREEN + "[?] Continuer quand même ? (o/n) : ").strip().lower()
            if retry in ("o", "oui", "y", "yes"):
                return path
        else:
            print(Fore.GREEN + f"[+] Wordlist trouvée : {path}")
            return path

def main():
    clear()
    banner()

    if os.geteuid() != 0:
        print(Fore.RED + "[!] Ce script doit être exécuté en tant que root (sudo).\n")
        sys.exit(1)

    wordlist = get_wordlist()

    cmd = ["wifite", "--kill", "--dict", wordlist]

    print(Fore.RED + "\n  ┌─ CONFIGURATION ──────────────────────────────┐")
    print(Fore.RED + f"  │  Wordlist : " + Fore.WHITE + f"{wordlist}")
    print(Fore.RED + f"  │  Options  : " + Fore.WHITE + "--kill (tue les processus bloquants)")
    print(Fore.RED + "  └──────────────────────────────────────────────┘")

    print(Fore.GREEN + f"\n[+] Commande : sudo {' '.join(cmd)}\n")

    confirm = input(Fore.GREEN + "[?] Lancer wifite ? (o/n) : ").strip().lower()
    if confirm not in ("o", "oui", "y", "yes"):
        print(Fore.RED + "\n[-] Annulé.")
        sys.exit(0)

    print(Fore.RED + "\n  " + "─" * 54 + "\n")

    try:
        subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n[!] Interrompu par l'utilisateur.")
    except FileNotFoundError:
        print(Fore.RED + "[-] Wifite introuvable. Est-il installé et dans le PATH ?")

if __name__ == "__main__":
    main()
