import os
import sys
import subprocess
from colorama import Fore, init

init(autoreset=True)

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    print(Fore.GREEN + r"""
	    ▌     ▗                          
	▛▌▛▌▛▌▌▌▛▘▜▘█▌▛▘                     
	▙▌▙▌▙▌▙▌▄▌▐▖▙▖▌                      
	▄▌                                   
              ▌   ▜ ▘  ▗     ▜ ▌     
              ▙▘▀▌▐ ▌  ▜▘▛▌▛▌▐ ▛▌▛▌▚▘
              ▛▖█▌▐▖▌  ▐▖▙▌▙▌▐▖▙▌▙▌▞▖
                                     
	▄▖▖▖▄▖▖▖▄▖                           
	▌ ▙▌▛▌▙▌▌                            
	▙▖ ▌█▌ ▌▙▖ 
    """)
    print(Fore.RED + "          GOBUSTER AUTOMATION TOOL  |  by C404C")
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

def get_wordlist():
    while True:
        wl = ask_required("Wordlist (-w)  (ex: /usr/share/wordlists/dirb/common.txt)")
        if check_file(wl):
            return wl
        if ask_yn("Continuer quand même"):
            return wl

def get_mode():
    section("1/4 — MODE D'ÉNUMÉRATION")
    line("[1]  dir    — Enumération de répertoires et fichiers  ← le plus utilisé")
    line("             Bruteforce de chemins sur un serveur web")
    line("[2]  vhost  — Enumération de virtual hosts")
    line("             Découvre des sous-domaines via Host header")
    line("[3]  dns    — Enumération de sous-domaines DNS")
    line("             Résolution DNS de sous-domaines")
    line("[4]  fuzz   — Mode fuzzing")
    line("             Remplace le mot-clé FUZZ dans l'URL/headers/body")
    line("[5]  s3     — Enumération de buckets AWS S3")
    line("[6]  gcs    — Enumération de buckets Google Cloud Storage")
    line("[7]  tftp   — Enumération de fichiers TFTP")
    sep()
    while True:
        choice = ask("Votre choix (1-7)")
        if choice in [str(i) for i in range(1, 8)]:
            mode_map = {
                "1": "dir", "2": "vhost", "3": "dns",
                "4": "fuzz", "5": "s3", "6": "gcs", "7": "tftp"
            }
            return mode_map[choice]
        print(Fore.RED + "  [-] Choix invalide.")

def get_dir_options():
    section("2/4 — OPTIONS DIR")
    flags = []

    url = ask_required("URL cible (-u)  (ex: http://192.168.1.1)")
    flags += ["-u", url]

    wl = get_wordlist()
    flags += ["-w", wl]

    if ask_yn("Extensions de fichiers à tester (-x)  [ex: php,html,txt,bak]"):
        ext = ask_required("Extensions séparées par virgule (ex: php,html,txt)")
        flags += ["-x", ext]

    if ask_yn("Afficher les codes de statut spécifiques (-s)  [ex: 200,301,302]"):
        codes = ask_required("Codes séparés par virgule (ex: 200,204,301,302,307)")
        flags += ["-s", codes]

    if ask_yn("Exclure certains codes de statut (--exclude-length ou -b)"):
        ecodes = ask_required("Codes à exclure (ex: 404,403)")
        flags += ["-b", ecodes]

    if ask_yn("Ajouter un slash final à chaque requête (-f / --add-slash)"):
        flags.append("--add-slash")

    if ask_yn("Suivre les redirections (-r)"):
        flags.append("-r")

    if ask_yn("Chercher aussi dans les sous-répertoires (--discover-backup)"):
        flags.append("--discover-backup")

    return flags

def get_vhost_options():
    section("2/4 — OPTIONS VHOST")
    flags = []

    url = ask_required("URL/IP cible (-u)  (ex: http://10.10.10.10)")
    flags += ["-u", url]

    wl = get_wordlist()
    flags += ["-w", wl]

    if ask_yn("Ajouter un domaine base aux entrées (--domain)  [ex: exemple.com]"):
        domain = ask_required("Domaine de base (ex: exemple.com)")
        flags += ["--domain", domain]

    if ask_yn("Appliquer les résultats avec --append-domain"):
        flags.append("--append-domain")

    if ask_yn("Exclure certains codes de statut (-b)  [ex: 404,302]"):
        ecodes = ask_required("Codes à exclure")
        flags += ["-b", ecodes]

    return flags

def get_dns_options():
    section("2/4 — OPTIONS DNS")
    flags = []

    domain = ask_required("Domaine cible (-d)  (ex: exemple.com)")
    flags += ["-d", domain]

    wl = get_wordlist()
    flags += ["-w", wl]

    if ask_yn("Résolveur DNS personnalisé (-r)  [ex: 8.8.8.8]"):
        resolver = ask_required("Adresse du résolveur DNS")
        flags += ["-r", resolver]

    if ask_yn("Afficher les IPs des sous-domaines trouvés (--show-ips)"):
        flags.append("--show-ips")

    if ask_yn("Vérifier si le domaine existe avant de lancer (--wildcard)"):
        flags.append("--wildcard")

    return flags

def get_fuzz_options():
    section("2/4 — OPTIONS FUZZ")
    line("Le mot-clé FUZZ sera remplacé par chaque entrée de la wordlist.")
    line("Ex URL : http://site.com/FUZZ  ou  http://site.com/?id=FUZZ")
    sep()
    flags = []

    url = ask_required("URL cible avec FUZZ (-u)  (ex: http://site.com/FUZZ)")
    flags += ["-u", url]

    wl = get_wordlist()
    flags += ["-w", wl]

    if ask_yn("Exclure des codes de statut (-b)  [ex: 404,400]"):
        ecodes = ask_required("Codes à exclure")
        flags += ["-b", ecodes]

    if ask_yn("Exclure des réponses par longueur (--exclude-length)"):
        length = ask_required("Longueur(s) à exclure (ex: 1234 ou 1234,5678)")
        flags += ["--exclude-length", length]

    return flags

def get_simple_options(mode):
    section(f"2/4 — OPTIONS {mode.upper()}")
    flags = []

    if mode == "tftp":
        host = ask_required("Hôte TFTP (-u)  (ex: 192.168.1.1)")
        flags += ["-u", host]
    else:
        print(Fore.WHITE + f"  Enumère des buckets {'AWS S3' if mode == 's3' else 'Google Cloud Storage'}.")
        print(Fore.WHITE + f"  La wordlist fournit les noms de buckets à tester.\n")

    wl = get_wordlist()
    flags += ["-w", wl]

    return flags

def get_common_options(mode):
    section("3/4 — OPTIONS HTTP & COMMUNES")
    flags = []

    if ask_yn("Ajouter des headers HTTP (-H)  [ex: 'Authorization: Bearer token']"):
        while True:
            h = ask_required("Header (format: 'Nom: Valeur')")
            flags += ["-H", h]
            if not ask_yn("Ajouter un autre header"):
                break

    if ask_yn("Utiliser des cookies (-c)  [ex: session=abc123]"):
        cookies = ask_required("Cookies (ex: PHPSESSID=abc; token=xyz)")
        flags += ["-c", cookies]

    if ask_yn("User-agent personnalisé (-a)"):
        ua = ask_required("User-agent (ex: Mozilla/5.0 ...)")
        flags += ["-a", ua]

    if ask_yn("Utiliser un proxy (-p)  [ex: http://127.0.0.1:8080]"):
        proxy = ask_required("URL du proxy")
        flags += ["-p", proxy]

    if ask_yn("Authentification HTTP basique (-U / -P)"):
        user = ask_required("Username")
        pw   = ask_required("Password")
        flags += ["-U", user, "-P", pw]

    if ask_yn("Timeout des requêtes (--timeout)  [défaut: 10s]"):
        t = ask_int("Timeout en secondes", min_val=1)
        flags += ["--timeout", t + "s"]

    if ask_yn("Nombre de threads (-t)  [défaut: 10]"):
        t = ask_int("Threads (ex: 20, 50)", min_val=1, max_val=200)
        flags += ["-t", t]

    if ask_yn("Ignorer les erreurs de certificat TLS (-k)"):
        flags.append("-k")

    return flags

def get_output():
    section("4/4 — OUTPUT & VERBOSITÉ")
    flags = []

    if ask_yn("Sauvegarder les résultats dans un fichier (-o)"):
        f = ask_required("Chemin du fichier de sortie (ex: /root/gobuster.txt)")
        flags += ["-o", f]

    if ask_yn("Mode verbose (-v)  [affiche aussi les éléments non trouvés]"):
        flags.append("-v")

    if ask_yn("Mode silencieux (-q)  [affiche uniquement les résultats]"):
        flags.append("-q")

    if ask_yn("Désactiver la barre de progression (--no-progress)"):
        flags.append("--no-progress")

    if ask_yn("Désactiver les erreurs (--no-error)"):
        flags.append("--no-error")

    return flags

def main():
    clear()
    banner()

    mode = get_mode()

    if mode == "dir":
        mode_flags = get_dir_options()
    elif mode == "vhost":
        mode_flags = get_vhost_options()
    elif mode == "dns":
        mode_flags = get_dns_options()
    elif mode == "fuzz":
        mode_flags = get_fuzz_options()
    else:
        mode_flags = get_simple_options(mode)

    common_flags = []
    if mode in ("dir", "vhost", "fuzz"):
        common_flags = get_common_options(mode)

    output_flags = get_output()

    cmd = ["gobuster", mode]
    cmd += mode_flags
    cmd += common_flags
    cmd += output_flags

    print(Fore.RED + "\n  ╔══ CONFIGURATION FINALE " + "═" * 31 + "╗")
    print(Fore.RED + "  ║  Mode    : " + Fore.WHITE + mode.upper())
    print(Fore.RED + "  ║  Options : " + Fore.WHITE + f"{' '.join(mode_flags)}")
    print(Fore.RED + "  ║  HTTP    : " + Fore.WHITE + f"{' '.join(common_flags) or 'défaut'}")
    print(Fore.RED + "  ║  Output  : " + Fore.WHITE + f"{' '.join(output_flags) or 'terminal'}")
    print(Fore.RED + "  ╚" + "═" * 55)

    print(Fore.GREEN + f"\n  [+] Commande : " + Fore.WHITE + f"{' '.join(cmd)}\n")

    confirm = input(Fore.GREEN + "  [?] Lancer gobuster ? (o/n) : ").strip().lower()
    if confirm not in ("o", "oui", "y", "yes"):
        print(Fore.GREEN + "\n  [-] Annulé.")
        sys.exit(0)

    print(Fore.GREEN + "\n  " + "─" * 56 + "\n")

    try:
        subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n  [!] Interrompu par l'utilisateur.")
    except FileNotFoundError:
        print(Fore.RED + "  [-] Gobuster introuvable. Est-il installé et dans le PATH ?")

if __name__ == "__main__":
    main()
