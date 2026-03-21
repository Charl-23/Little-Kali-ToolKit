import os
import sys
import subprocess
from colorama import Fore, init

init(autoreset=True)

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    print(Fore.GREEN + r"""
	▌    ▌                               
	▛▌▌▌▛▌▛▘▀▌                           
	▌▌▙▌▙▌▌ █▌                           
	  ▄▌                                 
              ▌   ▜ ▘  ▗     ▜ ▌     
              ▙▘▀▌▐ ▌  ▜▘▛▌▛▌▐ ▛▌▛▌▚▘
              ▛▖█▌▐▖▌  ▐▖▙▌▙▌▐▖▙▌▙▌▞▖
                                     
	▄▖▖▖▄▖▖▖▄▖                           
	▌ ▙▌▛▌▙▌▌                            
	▙▖ ▌█▌ ▌▙
    """)
    print(Fore.RED + "           HYDRA AUTOMATION TOOL  |  by C404C")
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

def check_file(path):
    if os.path.isfile(path):
        print(Fore.GREEN + "  [+] Fichier trouvé.")
        return True
    print(Fore.RED + f"  [-] Fichier introuvable : {path}")
    return False

def get_target():
    section("1/6 — CIBLE")
    line("[1]  Cible unique   — IP ou domaine  (ex: 192.168.1.1)")
    line("[2]  Liste de cibles (-M)  — Fichier avec une cible par ligne")
    sep()
    while True:
        choice = ask("Votre choix (1/2)")
        if choice == "1":
            target = ask_required("IP ou domaine cible")
            return target, []
        elif choice == "2":
            while True:
                f = ask_required("Chemin du fichier de cibles")
                if check_file(f):
                    break
                if ask_yn("Continuer quand même"):
                    break
            return None, ["-M", f]
        print(Fore.RED + "  [-] Choix invalide.")

def get_service():
    section("2/6 — SERVICE / PROTOCOLE")
    line("[1]  ssh          — SSH (port 22)")
    line("[2]  ftp          — FTP (port 21)")
    line("[3]  ftps         — FTP over SSL")
    line("[4]  http-get     — HTTP GET basique")
    line("[5]  http-post-form— Formulaire HTTP POST (login web)")
    line("[6]  https-get    — HTTPS GET")
    line("[7]  https-post-form— Formulaire HTTPS POST")
    line("[8]  smb          — Partage Windows SMB")
    line("[9]  smb2         — SMB2")
    line("[10] rdp          — Bureau à distance RDP (port 3389)")
    line("[11] mysql        — MySQL (port 3306)")
    line("[12] mssql        — SQL Server")
    line("[13] postgres      — PostgreSQL (port 5432)")
    line("[14] pop3         — POP3 (port 110)")
    line("[15] imap         — IMAP (port 143)")
    line("[16] smtp         — SMTP (port 25)")
    line("[17] telnet       — Telnet")
    line("[18] vnc          — VNC")
    line("[19] ldap3        — LDAP")
    line("[20] redis        — Redis")
    line("[21] mongodb      — MongoDB")
    line("[22] snmp         — SNMP")
    line("[23] sip          — SIP (VoIP)")
    line("[24] Personnalisé — Entrer manuellement")
    sep()
    svc_map = {
        "1": "ssh",   "2": "ftp",    "3": "ftps",
        "4": "http-get", "5": "http-post-form", "6": "https-get",
        "7": "https-post-form", "8": "smb", "9": "smb2",
        "10": "rdp",  "11": "mysql", "12": "mssql",
        "13": "postgres","14": "pop3","15": "imap",
        "16": "smtp", "17": "telnet","18": "vnc",
        "19": "ldap3","20": "redis", "21": "mongodb",
        "22": "snmp", "23": "sip",
    }
    while True:
        choice = ask("Votre choix")
        if choice in svc_map:
            service = svc_map[choice]
            break
        elif choice == "24":
            service = ask_required("Nom du service (ex: rtsp, xmpp...)")
            break
        else:
            print(Fore.RED + "  [-] Choix invalide.")

    flags = []
    if ask_yn("Port non standard (-s)"):
        port = ask_int("Port", min_val=1, max_val=65535)
        flags += ["-s", port]

    module_opt = ""
    if "post-form" in service:
        print(Fore.GREEN + "\n  [!] Le formulaire POST nécessite un paramètre au format :")
        print(Fore.WHITE + '      "/chemin/login:user=^USER^&pass=^PASS^:message_erreur"')
        print(Fore.WHITE + '  Ex: "/login.php:username=^USER^&password=^PASS^:Invalid credentials"')
        module_opt = ask_required("Paramètre du formulaire")

    return service, flags, module_opt

def get_credentials():
    section("3/6 — IDENTIFIANTS (LOGIN / MOT DE PASSE)")
    flags = []

    line("Mode login :")
    line("  [1]  Login unique     (-l)  ex: admin")
    line("  [2]  Liste de logins  (-L)  ex: /usr/share/wordlists/users.txt")
    line("  [3]  Fichier combiné  (-C)  format login:password par ligne")
    sep()
    while True:
        lmode = ask("Votre choix (1/2/3)")
        if lmode == "1":
            login = ask_required("Login")
            flags += ["-l", login]
            break
        elif lmode == "2":
            while True:
                lf = ask_required("Chemin fichier logins")
                if check_file(lf):
                    break
                if ask_yn("Continuer quand même"):
                    break
            flags += ["-L", lf]
            break
        elif lmode == "3":
            while True:
                cf = ask_required("Chemin fichier login:pass")
                if check_file(cf):
                    break
                if ask_yn("Continuer quand même"):
                    break
            flags += ["-C", cf]
            return flags  
        else:
            print(Fore.RED + "  [-] Choix invalide.")

    print()
    line("Mode mot de passe :")
    line("  [1]  Mot de passe unique  (-p)  ex: password123")
    line("  [2]  Wordlist             (-P)  ex: /usr/share/wordlists/rockyou.txt")
    line("  [3]  Bruteforce           (-x)  ex: 4:8:aA1!")
    sep()
    while True:
        pmode = ask("Votre choix (1/2/3)")
        if pmode == "1":
            pw = ask_required("Mot de passe")
            flags += ["-p", pw]
            break
        elif pmode == "2":
            while True:
                pf = ask_required("Chemin wordlist")
                if check_file(pf):
                    break
                if ask_yn("Continuer quand même"):
                    break
            flags += ["-P", pf]
            break
        elif pmode == "3":
            print(Fore.WHITE + "  Format : MIN:MAX:CHARSET")
            print(Fore.WHITE + "  Charsets : a=minuscules  A=majuscules  1=chiffres  !=spéciaux")
            print(Fore.WHITE + "  Ex: 4:8:aA1  = entre 4 et 8 chars, lettres + chiffres")
            bf = ask_required("Paramètre bruteforce (ex: 4:8:aA1!)")
            flags += ["-x", bf]
            break
        else:
            print(Fore.RED + "  [-] Choix invalide.")

    if ask_yn("Tester aussi : pass vide, login=pass, login inversé (-e nsr)"):
        flags += ["-e", "nsr"]

    return flags

def get_performance():
    section("4/6 — PERFORMANCE & TIMING")
    flags = []

    if ask_yn(f"Modifier le nombre de threads par cible (-t)  [défaut: 16]"):
        t = ask_int("Threads par cible (ex: 4, 8, 16, 32)", min_val=1, max_val=64)
        flags += ["-t", t]

    if ask_yn("Attendre entre chaque tentative (-c)  [évite les bans]"):
        c = ask_int("Délai en secondes entre chaque tentative", min_val=1)
        flags += ["-c", c]

    if ask_yn("Délai de réponse max (-w)  [défaut: 32s]"):
        w = ask_int("Délai max en secondes", min_val=1)
        flags += ["-w", w]

    if ask_yn("Arrêter dès qu'un couple valide est trouvé (-f)"):
        flags.append("-f")

    if ask_yn("Utiliser IPv6 (-6)"):
        flags.append("-6")

    if ask_yn("Utiliser SSL (-S)"):
        flags.append("-S")

    return flags

def get_output():
    section("5/6 — OUTPUT & VERBOSITÉ")
    flags = []

    if ask_yn("Sauvegarder les résultats dans un fichier (-o)"):
        f = ask_required("Chemin du fichier de sortie (ex: /root/results.txt)")
        flags += ["-o", f]
        print(Fore.WHITE + "  Format : text / json / jsonv1")
        fmt = ask("Format", "text")
        if fmt in ("json", "jsonv1"):
            flags += ["-b", fmt]

    if ask_yn("Mode verbose (-v)  [affiche les tentatives]"):
        flags.append("-v")

    if ask_yn("Mode très verbose (-V)  [affiche login+pass à chaque essai]"):
        flags.append("-V")

    if ask_yn("Supprimer les erreurs de connexion (-q)"):
        flags.append("-q")

    return flags

def get_session():
    section("6/6 — SESSION")
    flags = []

    if ask_yn("Reprendre une session interrompue (-R)"):
        return ["-R"], True

    if ask_yn("Ignorer le fichier de restauration existant (-I)"):
        flags.append("-I")

    return flags, False

def main():
    clear()
    banner()

    target, target_flags       = get_target()
    service, svc_flags, module = get_service()
    cred_flags                 = get_credentials()
    perf_flags                 = get_performance()
    output_flags               = get_output()
    session_flags, restore     = get_session()

    if restore:
        cmd = ["hydra"] + session_flags
    else:
        cmd = ["hydra"]
        cmd += cred_flags
        cmd += perf_flags
        cmd += output_flags
        cmd += session_flags
        cmd += target_flags
        cmd += svc_flags

        if target:
            if module:
                cmd.append(f"{service}://{target}/{module}")
            else:
                cmd.append(f"{service}://{target}")
        elif target_flags:
            cmd.append(service)

    print(Fore.RED + "\n  ╔══ CONFIGURATION FINALE " + "═" * 31 + "╗")
    print(Fore.RED + "  ║  Cible    : " + Fore.WHITE + f"{target or 'liste : ' + str(target_flags)}")
    print(Fore.RED + "  ║  Service  : " + Fore.WHITE + service)
    print(Fore.RED + "  ║  Creds    : " + Fore.WHITE + f"{' '.join(cred_flags)}")
    print(Fore.RED + "  ║  Perf     : " + Fore.WHITE + f"{' '.join(perf_flags) or 'défaut'}")
    print(Fore.RED + "  ║  Output   : " + Fore.WHITE + f"{' '.join(output_flags) or 'aucun'}")
    print(Fore.RED + "  ╚" + "═" * 55)

    print(Fore.GREEN + f"\n  [+] Commande : " + Fore.WHITE + f"{' '.join(cmd)}\n")

    confirm = input(Fore.GREEN + "  [?] Lancer hydra ? (o/n) : ").strip().lower()
    if confirm not in ("o", "oui", "y", "yes"):
        print(Fore.GREEN + "\n  [-] Annulé.")
        sys.exit(0)

    print(Fore.GREEN + "\n  " + "─" * 56 + "\n")

    try:
        subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n  [!] Interrompu par l'utilisateur.")
    except FileNotFoundError:
        print(Fore.RED + "  [-] Hydra introuvable. Est-il installé et dans le PATH ?")

if __name__ == "__main__":
    main()
