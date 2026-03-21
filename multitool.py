import os
import sys
import subprocess
from colorama import Fore, init

init(autoreset=True)

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(BASE_DIR, "tools")

TOOLS = {
    "1":  {"name": "Nmap",        "file": "nmap.py",       "desc": "Network Scanner & Port Discovery"},
    "2":  {"name": "SQLMap",      "file": "sqlmap.py",     "desc": "SQL Injection Automation"},
    "3":  {"name": "Commix",      "file": "commix.py",     "desc": "Command Injection Automation"},
    "4":  {"name": "Wifite",      "file": "wifite.py",     "desc": "Wifi Attack Automation"},
    "5":  {"name": "SEToolkit",   "file": "setoolkit.py",  "desc": "Social Engineering Toolkit"},
    "6":  {"name": "Aircrack-ng", "file": "aircrack.py",   "desc": "WiFi Password Cracking"},
    "7":  {"name": "John",        "file": "john.py",       "desc": "Password Hash Cracker"},
    "8":  {"name": "Hashcat",     "file": "hashcat.py",    "desc": "GPU Hash Cracker"},
    "9":  {"name": "Hydra",       "file": "hydra.py",      "desc": "Login Brute-Force Tool"},
    "10": {"name": "Nikto",       "file": "nikto.py",      "desc": "Web Server Vulnerability Scanner"},
    "11": {"name": "Gobuster",    "file": "gobuster.py",   "desc": "Directory & DNS Enumeration"},
    "12": {"name": "Dirb",        "file": "dirb.py",       "desc": "Web Content Scanner"},
    "13": {"name": "Netcat",      "file": "netcat.py",     "desc": "Network Swiss Army Knife"},
    "14": {"name": "Tcpdump",     "file": "tcpdump.py",    "desc": "Network Packet Analyzer"},
}

CATEGORIES = {
    "RÉSEAU & SCAN":          ["1", "13", "14"],
    "INJECTION & WEB":        ["2", "3", "10", "11", "12"],
    "MOT DE PASSE & CRACK":   ["7", "8", "9"],
    "WIFI":                   ["4", "6"],
    "SOCIAL ENGINEERING":     ["5"],
}

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    print(Fore.GREEN + r"""

 ██ ▄█▀    ▄▄▄          ██▓        ██▓                                      
 ██▄█▒    ▒████▄       ▓██▒       ▓██▒                                      
▓███▄░    ▒██  ▀█▄     ▒██░       ▒██▒                                      
▓██ █▄    ░██▄▄▄▄██    ▒██░       ░██░                                      
▒██▒ █▄    ▓█   ▓██▒   ░██████▒   ░██░                                      
▒ ▒▒ ▓▒    ▒▒   ▓▒█░   ░ ▒░▓  ░   ░▓                                        
░ ░▒ ▒░     ▒   ▒▒ ░   ░ ░ ▒  ░    ▒ ░                                      
░ ░░ ░      ░   ▒        ░ ░       ▒ ░                                      
░  ░            ░  ░       ░  ░    ░                                        
                                                                            
   ▄▄▄█████▓    ▒█████      ▒█████      ██▓        ██ ▄█▀    ██▓   ▄▄▄█████▓
   ▓  ██▒ ▓▒   ▒██▒  ██▒   ▒██▒  ██▒   ▓██▒        ██▄█▒    ▓██▒   ▓  ██▒ ▓▒
   ▒ ▓██░ ▒░   ▒██░  ██▒   ▒██░  ██▒   ▒██░       ▓███▄░    ▒██▒   ▒ ▓██░ ▒░
   ░ ▓██▓ ░    ▒██   ██░   ▒██   ██░   ▒██░       ▓██ █▄    ░██░   ░ ▓██▓ ░ 
     ▒██▒ ░    ░ ████▓▒░   ░ ████▓▒░   ░██████▒   ▒██▒ █▄   ░██░     ▒██▒ ░ 
     ▒ ░░      ░ ▒░▒░▒░    ░ ▒░▒░▒░    ░ ▒░▓  ░   ▒ ▒▒ ▓▒   ░▓       ▒ ░░   
       ░         ░ ▒ ▒░      ░ ▒ ▒░    ░ ░ ▒  ░   ░ ░▒ ▒░    ▒ ░       ░    
     ░         ░ ░ ░ ▒     ░ ░ ░ ▒       ░ ░      ░ ░░ ░     ▒ ░     ░      
                   ░ ░         ░ ░         ░  ░   ░  ░       ░              
                                                                            
    """)
    print(Fore.RED   + "              MULTI HACKING TOOL  |  by C404C")
    print(Fore.RED   + "                 https://github.com/Charl-23\n")
    print(Fore.GREEN + "  " + "─" * 62 + "\n")

def check_tools():
    status = {}
    for key, tool in TOOLS.items():
        path = os.path.join(TOOLS_DIR, tool["file"])
        status[key] = os.path.isfile(path)
    return status

def menu():
    clear()
    banner()

    status = check_tools()

    print(Fore.RED + "  ╔══ OUTILS DISPONIBLES " + "═" * 39 + "╗")

    for cat_title, keys in CATEGORIES.items():
        print(Fore.GREEN + "  ║")
        print(Fore.RED   + f"  ║  ── {cat_title} " + "─" * (48 - len(cat_title)))
        for key in keys:
            tool  = TOOLS[key]
            found = status[key]
            color = Fore.WHITE if found else Fore.RED
            badge = Fore.GREEN + "● OK" if found else Fore.RED + "✗ ABSENT"
            print(color + f"  ║  [{key:<2}] {tool['name']:<14} {tool['desc']:<36} " + badge)

    print(Fore.GREEN + "  ║")
    print(Fore.GREEN + "  ║  " + Fore.WHITE + "[0]   Quitter")
    print(Fore.RED   + "  ╚" + "═" * 61 + "\n")

    ok    = sum(1 for v in status.values() if v)
    total = len(TOOLS)
    print(Fore.GREEN + f"  Outils détectés : " + Fore.WHITE + f"{ok}/{total}  " +
          (Fore.GREEN + "✓ Tous présents" if ok == total else Fore.RED + f"✗ {total - ok} manquant(s)"))
    print(Fore.GREEN + f"  Dossier tools   : " + Fore.WHITE + TOOLS_DIR)
    print()

    return status

def launch(key, status):
    tool = TOOLS[key]
    if not status[key]:
        print(Fore.RED + f"\n  [-] '{tool['file']}' introuvable dans le dossier tools/")
        print(Fore.RED +  "  [-] Vérifie que le fichier existe bien :\n")
        print(Fore.WHITE + f"       {os.path.join(TOOLS_DIR, tool['file'])}\n")
        input(Fore.GREEN + "  [↵] Entrée pour revenir au menu...")
        return

    script_path = os.path.join(TOOLS_DIR, tool["file"])
    clear()
    print(Fore.GREEN + f"\n  [+] Lancement de " + Fore.WHITE + tool["name"] + Fore.GREEN + "...\n")
    print(Fore.GREEN + "  " + "─" * 62 + "\n")

    try:
        subprocess.run([sys.executable, script_path], check=False)
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n  [!] Interrompu par l'utilisateur.")

    print(Fore.GREEN + "\n  " + "─" * 62)
    input(Fore.GREEN + "  [↵] Entrée pour revenir au menu...")

def main():
    while True:
        status = menu()
        choice = input(Fore.GREEN + "  [>] Votre choix : " + Fore.WHITE).strip()

        if choice == "0":
            clear()
            print(Fore.GREEN + "\n  [!] À bientôt.\n")
            sys.exit(0)
        elif choice in TOOLS:
            launch(choice, status)
        else:
            print(Fore.RED + "\n  [-] Choix invalide.")
            import time; time.sleep(1)

if __name__ == "__main__":
    main()
