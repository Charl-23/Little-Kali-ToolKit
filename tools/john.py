import os
import sys
import subprocess
from colorama import Fore, init

init(autoreset=True)

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    print(Fore.GREEN + r"""
	 ▘  ▌     ▗ ▌       ▘                        
	 ▌▛▌▛▌▛▌  ▜▘▛▌█▌  ▛▘▌▛▌▛▌█▌▛▘                
	 ▌▙▌▌▌▌▌  ▐▖▌▌▙▖  ▌ ▌▙▌▙▌▙▖▌                 
	▙▌                   ▌ ▌                     
                      ▌   ▜ ▘  ▗     ▜ ▌     
                      ▙▘▀▌▐ ▌  ▜▘▛▌▛▌▐ ▛▌▛▌▚▘
                      ▛▖█▌▐▖▌  ▐▖▙▌▙▌▐▖▙▌▙▌▞▖
                                             
	▄▖▖▖▄▖▖▖▄▖                                   
	▌ ▙▌▛▌▙▌▌                                    
	▙▖ ▌█▌ ▌▙▖
    """)
    print(Fore.RED + "       JOHN THE RIPPER AUTOMATION TOOL  |  by C404C")
    print(Fore.RED + "                https://github.com/Charl-23\n")
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

def check_file(path):
    if os.path.isfile(path):
        print(Fore.GREEN + f"  [+] Fichier trouvé.")
        return True
    print(Fore.RED + f"  [-] Fichier introuvable : {path}")
    return False

def get_password_file():
    section("1/6 — FICHIER DE HASHES")
    line("Fichier contenant les hashes à cracker")
    line("Ex: /etc/shadow  |  hashes.txt  |  dump.txt")
    line("")
    line("Besoin de convertir ? Utilise un helper :")
    line("  ssh2john id_rsa > hash.txt")
    line("  zip2john archive.zip > hash.txt")
    line("  pdf2john fichier.pdf > hash.txt")
    line("  keepass2john db.kdbx > hash.txt")
    sep()
    while True:
        f = ask_required("Chemin du fichier de hashes")
        if check_file(f):
            return f
        if ask_yn("Continuer quand même"):
            return f

def get_format():
    section("2/6 — FORMAT DU HASH (--format)")
    line("Formats courants :")
    line("  [1]  md5crypt    — Linux MD5  ($1$)")
    line("  [2]  sha512crypt — Linux SHA-512  ($6$)  ← /etc/shadow")
    line("  [3]  sha256crypt — Linux SHA-256  ($5$)")
    line("  [4]  bcrypt      — bcrypt  ($2a$, $2b$)")
    line("  [5]  NT          — Hash Windows NTLM")
    line("  [6]  LM          — Hash Windows LM (ancien)")
    line("  [7]  Raw-MD5     — MD5 brut (pas salé)")
    line("  [8]  Raw-SHA1    — SHA1 brut")
    line("  [9]  Raw-SHA256  — SHA256 brut")
    line("  [10] zip         — Archive ZIP chiffrée")
    line("  [11] rar5        — Archive RAR5")
    line("  [12] SSH         — Clé SSH protégée")
    line("  [13] KeePass     — Base KeePass")
    line("  [14] PDF         — PDF protégé")
    line("  [15] Personnalisé — Entrer manuellement")
    line("  [0]  Auto-detect (john détecte tout seul)")
    sep()
    fmt_map = {
        "1": "md5crypt", "2": "sha512crypt", "3": "sha256crypt",
        "4": "bcrypt",   "5": "NT",          "6": "LM",
        "7": "Raw-MD5",  "8": "Raw-SHA1",    "9": "Raw-SHA256",
        "10": "zip",     "11": "rar5",        "12": "ssh",
        "13": "keepass", "14": "pdf",
    }
    choice = ask("Votre choix")
    if choice in fmt_map:
        return ["--format=" + fmt_map[choice]]
    elif choice == "15":
        fmt = ask_required("Nom du format (voir --list=formats)")
        return ["--format=" + fmt]
    return []

def get_attack_mode():
    section("3/6 — MODE D'ATTAQUE")
    line("[1]  Wordlist      — Attaque par dictionnaire  ← recommandé")
    line("                     + rules pour muter les mots")
    line("[2]  Single crack  — Utilise les infos du compte (login, GECOS...)")
    line("                     Très rapide, à tenter en premier")
    line("[3]  Incremental   — Bruteforce par incrément de caractères")
    line("                     Lent mais exhaustif")
    line("[4]  Mask          — Bruteforce avec masque  (ex: ?u?l?l?d?d)")
    line("                     ?u=MAJ  ?l=min  ?d=chiffre  ?s=spécial")
    line("[5]  Prince        — Combinaisons intelligentes depuis wordlist")
    line("[6]  Loopback      — Réutilise les mots du fichier .pot")
    sep()
    flags = []
    while True:
        choice = ask("Votre choix (1-6)")
        if choice == "1":
            while True:
                wl = ask_required("Chemin wordlist (ex: /usr/share/wordlists/rockyou.txt)")
                if check_file(wl):
                    break
                if ask_yn("Continuer quand même"):
                    break
            flags = ["--wordlist=" + wl]

            if ask_yn("Activer les règles de mutation (--rules)  [ex: Jumbo, KoreLogic]"):
                print(Fore.WHITE + "  Règles courantes : All, Jumbo, KoreLogic, best64, d3ad0ne")
                rule = ask("Nom de la règle (Entrée = règles par défaut)", "default")
                if rule and rule != "default":
                    flags.append("--rules=" + rule)
                else:
                    flags.append("--rules")
            break

        elif choice == "2":
            flags = ["--single"]
            if ask_yn("Ajouter des mots graines statiques (--single-seed)"):
                seeds = ask_required("Mots séparés par virgule (ex: admin,john,password)")
                flags.append("--single-seed=" + seeds)
            break

        elif choice == "3":
            print(Fore.WHITE + "  Modes disponibles : ASCII, Alpha, Digits, Alnum, LowerNum, UpperNum")
            mode = ask("Mode incrémental (Entrée = ASCII par défaut)", "ASCII")
            if not mode:
                mode = "ASCII"
            flags = ["--incremental=" + mode]

            if ask_yn("Limiter la longueur des candidats"):
                mn = ask_int("  Longueur minimale", min_val=1)
                mx = ask_int("  Longueur maximale", min_val=int(mn))
                flags += ["--min-length=" + mn, "--max-length=" + mx]
            break

        elif choice == "4":
            line("")
            line("Symboles de masque :")
            line("  ?l = minuscules (a-z)      ?u = majuscules (A-Z)")
            line("  ?d = chiffres (0-9)        ?s = caractères spéciaux")
            line("  ?a = tous les caractères   ?h = hex (0-9a-f)")
            line("Ex: ?u?l?l?l?d?d  =  Mot de 6 chars type 'Admin42'")
            mask = ask_required("Masque")
            flags = ["--mask=" + mask]
            break

        elif choice == "5":
            while True:
                wl = ask_required("Chemin wordlist pour PRINCE")
                if check_file(wl):
                    break
                if ask_yn("Continuer quand même"):
                    break
            flags = ["--prince=" + wl]
            if ask_yn("Appliquer des règles aussi (--rules)"):
                flags.append("--rules")
            break

        elif choice == "6":
            pot = ask("Fichier .pot (Entrée = john.pot par défaut)", "")
            if pot:
                flags = ["--loopback=" + pot]
            else:
                flags = ["--loopback"]
            break

        else:
            print(Fore.RED + "  [-] Choix invalide, entrez 1 à 6.")

    return flags

def get_filters():
    section("4/6 — FILTRES  (optionnel)")
    flags = []

    if ask_yn("Cibler certains utilisateurs (--users)"):
        users = ask_required("Utilisateurs séparés par virgule (ex: root,admin)")
        flags.append("--users=" + users)

    if ask_yn("Limiter la longueur des candidats testés"):
        mn = ask_int("  Longueur minimale", min_val=1)
        mx = ask_int("  Longueur maximale", min_val=int(mn))
        flags += ["--min-length=" + mn, "--max-length=" + mx]

    if ask_yn("Arrêter après N candidats (--max-candidates)"):
        n = ask_int("  Nombre max de candidats", min_val=1)
        flags.append("--max-candidates=" + n)

    if ask_yn("Arrêter après N secondes (--max-run-time)"):
        n = ask_int("  Durée max en secondes", min_val=1)
        flags.append("--max-run-time=" + n)

    return flags

def get_performance():
    section("5/6 — PERFORMANCE")
    flags = []

    if ask_yn("Utiliser plusieurs processus (--fork)  [parallélisation]"):
        n = ask_int("  Nombre de processus (ex: 4)", min_val=2)
        flags.append("--fork=" + n)

    if ask_yn("Économiser la mémoire (--save-memory)  [1=léger 3=max]"):
        lvl = ask_int("  Niveau (1-3)", min_val=1, max_val=3)
        flags.append("--save-memory=" + lvl)

    if ask_yn("Changer la verbosité (--verbosity)  [1-5, défaut=3]"):
        v = ask_int("  Niveau (1-5)", min_val=1, max_val=5)
        flags.append("--verbosity=" + v)

    return flags

def get_session():
    section("6/6 — SESSION & AFFICHAGE")
    flags = []

    if ask_yn("Nommer cette session (--session)  [pour la reprendre plus tard]"):
        name = ask_required("Nom de la session (ex: crack_admin)")
        flags.append("--session=" + name)

    if ask_yn("Reprendre une session existante (--restore)"):
        name = ask_required("Nom de la session à reprendre")
        return ["--restore=" + name], True

    if ask_yn("Afficher les mots de passe déjà crackés (--show)"):
        flags.append("--show")

    if ask_yn("Log dans le terminal plutôt que dans un fichier (--log-stderr)"):
        flags.append("--log-stderr")

    if ask_yn("Émettre un status à chaque crack (--crack-status)"):
        flags.append("--crack-status")

    if ask_yn("Émettre un status toutes les N secondes (--progress-every)"):
        n = ask_int("  Intervalle en secondes", min_val=1)
        flags.append("--progress-every=" + n)

    return flags, False

def main():
    clear()
    banner()

    pw_file      = get_password_file()
    fmt_flags    = get_format()
    attack_flags = get_attack_mode()
    filter_flags = get_filters()
    perf_flags   = get_performance()
    session_flags, restore_mode = get_session()

    if restore_mode:
        cmd = ["john"] + session_flags
    else:
        cmd = ["john"]
        cmd += fmt_flags
        cmd += attack_flags
        cmd += filter_flags
        cmd += perf_flags
        cmd += session_flags
        cmd.append(pw_file)

    print(Fore.RED + "\n  ╔══ CONFIGURATION FINALE " + "═" * 31 + "╗")
    print(Fore.RED + "  ║  Fichier  : " + Fore.WHITE + pw_file)
    print(Fore.RED + "  ║  Format   : " + Fore.WHITE + f"{' '.join(fmt_flags) or 'auto-detect'}")
    print(Fore.RED + "  ║  Attaque  : " + Fore.WHITE + f"{' '.join(attack_flags)}")
    print(Fore.RED + "  ║  Filtres  : " + Fore.WHITE + f"{' '.join(filter_flags) or 'aucun'}")
    print(Fore.RED + "  ║  Perf     : " + Fore.WHITE + f"{' '.join(perf_flags) or 'défaut'}")
    print(Fore.RED + "  ║  Session  : " + Fore.WHITE + f"{' '.join(session_flags) or 'aucune'}")
    print(Fore.RED + "  ╚" + "═" * 55)

    print(Fore.GREEN + f"\n  [+] Commande : " + Fore.WHITE + f"{' '.join(cmd)}\n")

    confirm = input(Fore.GREEN + "  [?] Lancer john ? (o/n) : ").strip().lower()
    if confirm not in ("o", "oui", "y", "yes"):
        print(Fore.GREEN + "\n  [-] Annulé.")
        sys.exit(0)

    print(Fore.GREEN + "\n  " + "─" * 56 + "\n")

    try:
        subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n  [!] Interrompu par l'utilisateur.")
    except FileNotFoundError:
        print(Fore.RED + "  [-] John introuvable. Est-il installé et dans le PATH ?")

if __name__ == "__main__":
    main()
