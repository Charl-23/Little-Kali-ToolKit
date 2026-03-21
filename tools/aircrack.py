import os
import sys
import subprocess
from colorama import Fore, init

init(autoreset=True)

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    print(Fore.GREEN + r"""
	  ▘          ▌                               
	▀▌▌▛▘▛▘▛▘▀▌▛▘▙▘▄▖▛▌▛▌                        
	█▌▌▌ ▙▖▌ █▌▙▖▛▖  ▌▌▙▌                        
	                   ▄▌                        
                      ▌   ▜ ▘  ▗     ▜ ▌     
                      ▙▘▀▌▐ ▌  ▜▘▛▌▛▌▐ ▛▌▛▌▚▘
                      ▛▖█▌▐▖▌  ▐▖▙▌▙▌▐▖▙▌▙▌▞▖
                                             
	▄▖▖▖▄▖▖▖▄▖                                   
	▌ ▙▌▛▌▙▌▌                                    
	▙▖ ▌█▌ ▌▙▖  
    """)
    print(Fore.RED + "         AIRCRACK-NG AUTOMATION TOOL  |  by C404C")
    print(Fore.RED + "              https://github.com/Charl-23\n")
    print(Fore.GREEN + "  " + "─" * 56 + "\n")

def section(title):
    print(Fore.GREEN + f"\n  ╔══ {title} " + "═" * (46 - len(title)) + "╗")

def line(text):
    print(Fore.WHITE + f"  ║  {text}")

def sep():
    print(Fore.GREEN + "  ╚" + "═" * 55)

def ask(question, default=None):
    suffix = Fore.WHITE + f" [{default}]" if default else ""
    return input(Fore.GREEN + f"  [?] {question}{suffix} : " + Fore.WHITE).strip()

def ask_yn(question):
    r = input(Fore.GREEN + f"  [?] {question} " + Fore.WHITE + "(o/n) : ").strip().lower()
    return r in ("o", "oui", "y", "yes")

def ask_required(question):
    while True:
        val = input(Fore.GREEN + f"  [?] {question} : " + Fore.WHITE).strip()
        if val:
            return val
        print(Fore.RED + "  [-] Ce champ est obligatoire.")

def ask_int(question, min_val=None, max_val=None):
    while True:
        val = input(Fore.GREEN + f"  [?] {question} : " + Fore.WHITE).strip()
        if not val.isdigit():
            print(Fore.RED + "  [-] Entrez un nombre entier valide.")
            continue
        n = int(val)
        if min_val is not None and n < min_val:
            print(Fore.RED + f"  [-] Valeur minimale : {min_val}")
            continue
        if max_val is not None and n > max_val:
            print(Fore.RED + f"  [-] Valeur maximale : {max_val}")
            continue
        return val

def get_mode():
    section("1/5 — MODE D'ATTAQUE")
    line("[1]  WEP      — Chiffrement ancien, crackable par statistiques")
    line("[2]  WPA-PSK  — Chiffrement moderne, attaque par wordlist/PMKID")
    sep()
    while True:
        choice = ask("Votre choix (1/2)")
        if choice == "1":
            return "1", "WEP"
        elif choice == "2":
            return "2", "WPA-PSK"
        print(Fore.RED + "  [-] Choix invalide, entrez 1 ou 2.")

def get_input_file():
    section("2/5 — FICHIER DE CAPTURE")
    line("Fichier .cap / .ivs / .pcap capturé avec airodump-ng")
    line("Ex: capture.cap  ou  /home/user/captures/wpa.cap")
    sep()
    while True:
        f = ask_required("Chemin du fichier de capture")
        if os.path.isfile(f):
            print(Fore.GREEN + f"  [+] Fichier trouvé : {f}")
            return f
        print(Fore.RED + f"  [-] Fichier introuvable : {f}")
        if ask_yn("Continuer quand même"):
            return f

def get_target():
    section("3/5 — CIBLE")
    line("ESSID  = nom du réseau WiFi  (ex: MonWifi)")
    line("BSSID  = adresse MAC du routeur  (ex: AA:BB:CC:DD:EE:FF)")
    line("→ Utilise au moins l'un des deux pour cibler le bon réseau")
    sep()
    flags = []

    if ask_yn("Spécifier l'ESSID (-e)"):
        essid = ask_required("ESSID (nom du réseau)")
        flags += ["-e", essid]

    if ask_yn("Spécifier le BSSID (-b)"):
        bssid = ask_required("BSSID (MAC du point d'accès, ex: AA:BB:CC:11:22:33)")
        flags += ["-b", bssid]

    if not flags:
        print(Fore.RED + "  [!] Aucune cible spécifiée : aircrack-ng cherchera dans tous les réseaux du fichier.")

    return flags

def get_wep_options():
    section("4/5 — OPTIONS WEP")
    flags = []

    line("Longueur de la clé WEP :")
    line("  [1] 64 bits   (clé 40 bits)   — la plus courante")
    line("  [2] 128 bits  (clé 104 bits)  — plus longue")
    line("  [3] 152 bits")
    line("  [4] 256 bits")
    line("  [5] 512 bits")
    line("  [0] Laisser aircrack-ng décider")
    sep()
    nbits_map = {"1": "64", "2": "128", "3": "152", "4": "256", "5": "512"}
    choice = ask("Votre choix")
    if choice in nbits_map:
        flags += ["-n", nbits_map[choice]]

    print()
    line("Type de clé recherché :")
    line("  [1] Alphanumérique uniquement (-c)")
    line("  [2] BCD (Binary Coded Decimal) (-t)")
    line("  [3] Numérique Fritz!BOX (-h)")
    line("  [0] Tous les caractères (par défaut)")
    sep()
    ktype = ask("Votre choix")
    if ktype == "1":   flags.append("-c")
    elif ktype == "2": flags.append("-t")
    elif ktype == "3": flags.append("-h")

    if ask_yn("Afficher la clé en ASCII pendant le cracking (-s)"):
        flags.append("-s")

    if ask_yn("Spécifier l'index de la clé WEP (-i)  [1 à 4]"):
        idx = ask_int("Index (1-4)", min_val=1, max_val=4)
        flags += ["-i", idx]

    if ask_yn("Activer le WEP decloak (-D)  [ignore les keystreams cassés]"):
        flags.append("-D")

    if ask_yn("Spécifier le nombre max d'IVs à utiliser (-M)"):
        m = ask_int("Nombre max d'IVs (ex: 100000)", min_val=1)
        flags += ["-M", m]

    if ask_yn("Filtrer par adresse MAC (-m)  [ne garder que ses paquets]"):
        mac = ask_required("Adresse MAC à filtrer (ex: AA:BB:CC:DD:EE:FF)")
        flags += ["-m", mac]

    if ask_yn("Activer le bruteforce des 2 derniers keybytes (-x2)"):
        flags.append("-x2")

    return flags

def get_wpa_options():
    section("4/5 — OPTIONS WPA-PSK")
    flags = []

    line("Méthode d'attaque :")
    line("  [1] Wordlist classique   (-w)  ← recommandé")
    line("  [2] Base de données airolib-ng (-r)  [PMK précalculées]")
    line("  [3] PMKID string pour hashcat (-I)")
    sep()
    while True:
        method = ask("Votre choix (1/2/3)")
        if method == "1":
            while True:
                wl = ask_required("Chemin wordlist (ex: /usr/share/wordlists/rockyou.txt)")
                if os.path.isfile(wl):
                    print(Fore.GREEN + f"  [+] Wordlist trouvée.")
                    break
                print(Fore.RED + f"  [-] Fichier introuvable.")
                if ask_yn("Continuer quand même"):
                    break
            flags += ["-w", wl]
            break
        elif method == "2":
            db = ask_required("Chemin base airolib-ng (ex: /root/pmk.db)")
            flags += ["-r", db]
            break
        elif method == "3":
            pmkid = ask_required("PMKID string (format hashcat -m 16800)")
            flags += ["-I", pmkid]
            break
        else:
            print(Fore.RED + "  [-] Choix invalide.")

    if ask_yn("Créer un fichier Hashcat HCCAPX (-j)  [hashcat -m 2500]"):
        hf = ask_required("Nom du fichier de sortie (ex: output.hccapx)")
        flags += ["-j", hf]

    if ask_yn("Test de vitesse WPA (-S)"):
        flags.append("-S")

    return flags

def get_common_options():
    section("5/5 — OPTIONS COMMUNES")
    flags = []

    if ask_yn("Écrire la clé trouvée dans un fichier (-l)"):
        lf = ask_required("Chemin du fichier de sortie (ex: /root/key.txt)")
        flags += ["-l", lf]

    if ask_yn("Limiter le nombre de CPUs (-p)  [par défaut : tous]"):
        cpu = ask_int("Nombre de CPUs à utiliser", min_val=1)
        flags += ["-p", cpu]

    if ask_yn("Mode silencieux (-q)  [pas de status output]"):
        flags.append("-q")

    return flags

def main():
    clear()
    banner()

    mode_val, mode_label = get_mode()
    input_file           = get_input_file()
    target_flags         = get_target()

    if mode_val == "1":
        mode_flags = get_wep_options()
    else:
        mode_flags = get_wpa_options()

    common_flags = get_common_options()

    cmd = ["aircrack-ng"]
    cmd += ["-a", mode_val]
    cmd += target_flags
    cmd += mode_flags
    cmd += common_flags
    cmd.append(input_file)

    print(Fore.RED + "\n  ╔══ CONFIGURATION FINALE " + "═" * 31 + "╗")
    print(Fore.RED + "  ║  Mode     : " + Fore.WHITE + mode_label)
    print(Fore.RED + "  ║  Fichier  : " + Fore.WHITE + input_file)
    print(Fore.RED + "  ║  Cible    : " + Fore.WHITE + f"{' '.join(target_flags) or 'tous les réseaux du fichier'}")
    print(Fore.RED + "  ║  Options  : " + Fore.WHITE + f"{' '.join(mode_flags) or 'aucune'}")
    print(Fore.RED + "  ║  Commun   : " + Fore.WHITE + f"{' '.join(common_flags) or 'aucune'}")
    print(Fore.RED + "  ╚" + "═" * 55)

    print(Fore.GREEN + f"\n  [+] Commande : " + Fore.WHITE + f"{' '.join(cmd)}\n")

    confirm = input(Fore.GREEN + "  [?] Lancer aircrack-ng ? (o/n) : ").strip().lower()
    if confirm not in ("o", "oui", "y", "yes"):
        print(Fore.GREEN + "\n  [-] Annulé.")
        sys.exit(0)

    print(Fore.GREEN + "\n  " + "─" * 56 + "\n")

    try:
        subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n  [!] Interrompu par l'utilisateur.")
    except FileNotFoundError:
        print(Fore.RED + "  [-] aircrack-ng introuvable. Est-il installé et dans le PATH ?")

if __name__ == "__main__":
    main()
