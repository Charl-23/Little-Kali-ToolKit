import os
import sys
import subprocess
from colorama import Fore, init

init(autoreset=True)

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    print(Fore.GREEN + r"""
	 ▌▘  ▌                               
	▛▌▌▛▘▛▌                              
	▙▌▌▌ ▙▌                              
	                                     
              ▌   ▜ ▘  ▗     ▜ ▌     
              ▙▘▀▌▐ ▌  ▜▘▛▌▛▌▐ ▛▌▛▌▚▘
              ▛▖█▌▐▖▌  ▐▖▙▌▙▌▐▖▙▌▙▌▞▖
                                     
	▄▖▖▖▄▖▖▖▄▖                           
	▌ ▙▌▛▌▙▌▌                            
	▙▖ ▌█▌ ▌▙
    """)
    print(Fore.RED + "            DIRB AUTOMATION TOOL  |  by C404C")
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
    section("1/4 — CIBLE & WORDLIST")
    line("Ex URL : http://192.168.1.1/  |  https://site.com/répertoire/")
    sep()

    url = ask_required("URL cible")

    line("")
    line("Wordlists courantes sur Kali :")
    line("  /usr/share/dirb/wordlists/common.txt          ← par défaut")
    line("  /usr/share/dirb/wordlists/big.txt")
    line("  /usr/share/dirb/wordlists/vulns/apache.txt")
    line("  /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt")
    line("")
    line("  [0] Utiliser la wordlist par défaut de dirb")
    sep()

    wordlists = []
    wl_input = ask("Wordlist(s) séparées par virgule (ou 0 pour défaut)")
    if wl_input and wl_input != "0":
        for wl in wl_input.split(","):
            wl = wl.strip()
            if not check_file(wl):
                if not ask_yn(f"Continuer quand même avec '{wl}'"):
                    continue
            wordlists.append(wl)

    return url, ",".join(wordlists) if wordlists else ""

def get_extensions():
    section("2/4 — EXTENSIONS & RECHERCHE")
    flags = []

    if ask_yn("Ajouter des extensions à chaque mot testé (-X)"):
        line("")
        line("Ex: .php,.html,.txt,.bak,.old,.zip")
        sep()
        ext = ask_required("Extensions (ex: .php,.html,.txt)")
        exts = []
        for e in ext.split(","):
            e = e.strip()
            if e and not e.startswith("."):
                e = "." + e
            if e:
                exts.append(e)
        flags += ["-X", ",".join(exts)]

    elif ask_yn("Charger les extensions depuis un fichier (-x)"):
        while True:
            f = ask_required("Chemin du fichier d'extensions")
            if check_file(f):
                break
            if ask_yn("Continuer quand même"):
                break
        flags += ["-x", f]

    if ask_yn("Recherche insensible à la casse (-i)"):
        flags.append("-i")

    if ask_yn("Utiliser le chemin tel quel sans modification (-b)"):
        flags.append("-b")

    if ask_yn("Ne pas forcer le slash final sur les URLs (-t)"):
        flags.append("-t")

    return flags

def get_http_options():
    section("3/4 — HTTP, AUTH & PROXY")
    flags = []

    if ask_yn("Authentification HTTP basique (-u)"):
        auth = ask_required("Identifiants (format: username:password)")
        flags += ["-u", auth]

    if ask_yn("Ajouter un cookie (-c)"):
        cookie = ask_required("Cookie (ex: PHPSESSID=abc123; token=xyz)")
        flags += ["-c", cookie]

    if ask_yn("Ajouter un header HTTP personnalisé (-H)"):
        while True:
            h = ask_required("Header (ex: Authorization: Bearer token)")
            flags += ["-H", h]
            if not ask_yn("Ajouter un autre header"):
                break

    if ask_yn("User-agent personnalisé (-a)"):
        ua = ask_required("User-agent (ex: Mozilla/5.0 ...)")
        flags += ["-a", ua]

    if ask_yn("Utiliser un proxy (-p)"):
        proxy = ask_required("Proxy (ex: http://127.0.0.1:8080 ou IP:port)")
        flags += ["-p", proxy]
        if ask_yn("Authentification proxy (-P)"):
            pauth = ask_required("Identifiants proxy (format: user:password)")
            flags += ["-P", pauth]

    if ask_yn("Certificat client (-E)"):
        while True:
            cert = ask_required("Chemin du certificat")
            if check_file(cert):
                break
            if ask_yn("Continuer quand même"):
                break
        flags += ["-E", cert]

    if ask_yn("Ignorer un code HTTP spécifique (-N)  [ex: 302, 403]"):
        code = ask_int("Code HTTP à ignorer", min_val=100, max_val=599)
        flags += ["-N", code]

    if ask_yn("Délai entre les requêtes (-z)  [évite le flood]"):
        delay = ask_int("Délai en millisecondes (ex: 200)", min_val=1)
        flags += ["-z", delay]

    return flags

def get_output_options():
    section("4/4 — RÉCURSION, OUTPUT & AFFICHAGE")
    flags = []

    line("Mode de récursion :")
    line("  [1]  Récursion automatique (défaut dirb)")
    line("  [2]  Pas de récursion (-r)")
    line("  [3]  Récursion interactive (-R)  [demande à chaque répertoire]")
    sep()
    rec = ask("Votre choix (1/2/3)", "1")
    if rec == "2":
        flags.append("-r")
    elif rec == "3":
        flags.append("-R")

    if ask_yn("Sauvegarder les résultats dans un fichier (-o)"):
        f = ask_required("Chemin du fichier de sortie (ex: /root/dirb_result.txt)")
        flags += ["-o", f]

    if ask_yn("Afficher aussi les pages NOT FOUND (-v)"):
        flags.append("-v")

    if ask_yn("Afficher le header Location quand trouvé (-l)"):
        flags.append("-l")

    if ask_yn("Mode silencieux (-S)  [n'affiche pas les mots testés]"):
        flags.append("-S")

    if ask_yn("Fine tuning de détection des 404 (-f)  [plus précis]"):
        flags.append("-f")

    if ask_yn("Ne pas s'arrêter sur les warnings (-w)"):
        flags.append("-w")

    if ask_yn("Reprendre une session précédente (-resume)"):
        flags.append("-resume")

    return flags

def main():
    clear()
    banner()

    url, wordlists   = get_target()
    ext_flags        = get_extensions()
    http_flags       = get_http_options()
    output_flags     = get_output_options()

    cmd = ["dirb", url]
    if wordlists:
        cmd.append(wordlists)
    cmd += ext_flags
    cmd += http_flags
    cmd += output_flags

    print(Fore.RED + "\n  ╔══ CONFIGURATION FINALE " + "═" * 31 + "╗")
    print(Fore.RED + "  ║  URL       : " + Fore.WHITE + url)
    print(Fore.RED + "  ║  Wordlist  : " + Fore.WHITE + (wordlists or "défaut dirb"))
    print(Fore.RED + "  ║  Exts      : " + Fore.WHITE + f"{' '.join(ext_flags) or 'aucune'}")
    print(Fore.RED + "  ║  HTTP      : " + Fore.WHITE + f"{' '.join(http_flags) or 'défaut'}")
    print(Fore.RED + "  ║  Output    : " + Fore.WHITE + f"{' '.join(output_flags) or 'terminal'}")
    print(Fore.RED + "  ╚" + "═" * 55)

    print(Fore.GREEN + f"\n  [+] Commande : " + Fore.WHITE + f"{' '.join(cmd)}\n")

    print(Fore.GREEN + "  Raccourcis pendant le scan :")
    print(Fore.WHITE + "    n → répertoire suivant  |  q → stopper  |  r → stats restantes\n")

    confirm = input(Fore.GREEN + "  [?] Lancer dirb ? (o/n) : ").strip().lower()
    if confirm not in ("o", "oui", "y", "yes"):
        print(Fore.GREEN + "\n  [-] Annulé.")
        sys.exit(0)

    print(Fore.GREEN + "\n  " + "─" * 56 + "\n")

    try:
        subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n  [!] Interrompu. Session sauvegardée, utilise -resume pour reprendre.")
    except FileNotFoundError:
        print(Fore.RED + "  [-] DIRB introuvable. Est-il installé et dans le PATH ?")

if __name__ == "__main__":
    main()
