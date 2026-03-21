import os
import sys
import subprocess
from colorama import Fore, init

init(autoreset=True)

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    print(Fore.GREEN + r"""
	  ▘▌ ▗                               
	▛▌▌▙▘▜▘▛▌                            
	▌▌▌▛▖▐▖▙▌                            
                                     
              ▌   ▜ ▘  ▗     ▜ ▌     
              ▙▘▀▌▐ ▌  ▜▘▛▌▛▌▐ ▛▌▛▌▚▘
              ▛▖█▌▐▖▌  ▐▖▙▌▙▌▐▖▙▌▙▌▞▖
                                     
	▄▖▖▖▄▖▖▖▄▖                           
	▌ ▙▌▛▌▙▌▌                            
	▙▖ ▌█▌ ▌▙
    """)
    print(Fore.RED + "           NIKTO AUTOMATION TOOL  |  by C404C")
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

def get_target():
    section("1/6 — CIBLE")
    line("Ex: http://192.168.1.1  |  https://site.com  |  192.168.1.1")
    sep()
    host = ask_required("URL ou IP cible (-host)")
    flags = ["-host", host]

    if ask_yn("Port non standard (-port)  [défaut: 80]"):
        port = ask_int("Port", min_val=1, max_val=65535)
        flags += ["-port", port]

    if ask_yn("Forcer SSL (-ssl)"):
        flags.append("-ssl")

    if ask_yn("Désactiver SSL (-nossl)"):
        flags.append("-nossl")

    if ask_yn("Spécifier un virtual host (-vhost)  [pour Host header]"):
        vhost = ask_required("Virtual host (ex: admin.site.com)")
        flags += ["-vhost", vhost]

    if ask_yn("Authentification HTTP (-id)  [format: user:pass ou user:pass:realm]"):
        auth = ask_required("Identifiants (ex: admin:password)")
        flags += ["-id", auth]

    if ask_yn("IPv4 uniquement (-ipv4)"):
        flags.append("-ipv4")
    elif ask_yn("IPv6 uniquement (-ipv6)"):
        flags.append("-ipv6")

    return flags

def get_tuning():
    section("2/6 — TUNING — TYPE DE TESTS (-Tuning)")
    line("Sélectionne les catégories de vulnérabilités à tester.")
    line("Tu peux combiner plusieurs codes (ex: 1234 ou 9a)")
    line("")
    line("  1   Fichiers intéressants / vus dans des logs")
    line("  2   Mauvaise config / fichiers par défaut")
    line("  3   Divulgation d'informations")
    line("  4   Injection (XSS / Script / HTML)")
    line("  5   Remote File Retrieval — dans le webroot")
    line("  6   Déni de Service")
    line("  7   Remote File Retrieval — partout sur le serveur")
    line("  8   Exécution de commandes / Remote Shell")
    line("  9   Injection SQL")
    line("  0   Upload de fichiers")
    line("  a   Bypass d'authentification")
    line("  b   Identification de logiciels")
    line("  c   Remote Source Inclusion")
    line("  d   WebService")
    line("  e   Console d'administration")
    line("  x   Inverser la sélection (tout sauf ce qui est spécifié)")
    line("")
    line("  [0] Tout tester (pas de -Tuning, nikto fait tout)")
    sep()
    tuning = ask("Codes de tuning (ex: 1234, 9a, ou 0 pour tout)")
    if tuning and tuning != "0":
        return ["-Tuning", tuning]
    return []

def get_evasion():
    section("3/6 — ÉVASION IDS / WAF (-evasion)")
    line("Techniques d'encodage pour contourner les IDS/WAF.")
    line("Tu peux combiner plusieurs codes (ex: 12 ou 1AB)")
    line("")
    line("  1   Encodage URI aléatoire (non-UTF8)")
    line("  2   Auto-référence répertoire  (/./ )")
    line("  3   Fin d'URL prématurée")
    line("  4   Préfixe long aléatoire")
    line("  5   Faux paramètre")
    line("  6   TAB comme séparateur dans la requête")
    line("  7   Changer la casse de l'URL")
    line("  8   Séparateur Windows  (\\)")
    line("  A   Retour chariot (0x0d) comme séparateur")
    line("  B   Valeur binaire 0x0b comme séparateur")
    line("")
    line("  [0] Aucune évasion")
    sep()
    ev = ask("Codes d'évasion (ou 0 pour aucune)")
    if ev and ev != "0":
        return ["-evasion", ev]
    return []

def get_mutation():
    section("4/6 — MUTATION — DÉCOUVERTE SUPPLÉMENTAIRE (-mutate)")
    line("Techniques pour deviner des fichiers/répertoires supplémentaires.")
    line("")
    line("  1   Tester tous les fichiers dans tous les répertoires root")
    line("  2   Deviner des noms de fichiers de mots de passe")
    line("  3   Énumérer les utilisateurs via Apache  (/~user)")
    line("  4   Énumérer les utilisateurs via cgiwrap")
    line("  5   Bruteforce des sous-domaines")
    line("  6   Deviner des noms de répertoires (depuis dictionnaire)")
    line("")
    line("  [0] Aucune mutation")
    sep()
    mut = ask("Code de mutation (1-6 ou 0 pour aucune)")
    flags = []
    if mut and mut != "0" and mut in "123456":
        flags += ["-mutate", mut]
        if mut == "6":
            if ask_yn("Spécifier un dictionnaire pour la mutation (-mutate-options)"):
                d = ask_required("Chemin du dictionnaire")
                flags += ["-mutate-options", d]
    return flags

def get_output():
    section("5/6 — OUTPUT & AFFICHAGE")
    flags = []

    if ask_yn("Sauvegarder les résultats dans un fichier (-output)"):
        f = ask_required("Chemin du fichier de sortie (ex: /root/nikto_result.html)")
        flags += ["-output", f]

        line("")
        line("Format de sortie (-Format) :")
        line("  [1] txt   — Texte brut")
        line("  [2] html  — HTML  ← lisible dans un navigateur")
        line("  [3] csv   — CSV")
        line("  [4] json  — JSON")
        line("  [5] xml   — XML")
        line("  [6] sql   — SQL")
        line("  [0] Auto (depuis l'extension du fichier)")
        sep()
        fmt_map = {"1":"txt","2":"htm","3":"csv","4":"json","5":"xml","6":"sql"}
        fmt = ask("Format")
        if fmt in fmt_map:
            flags += ["-Format", fmt_map[fmt]]

    line("")
    line("Options d'affichage (-Display) :")
    line("  1=redirects  2=cookies  3=200 OK  4=auth required")
    line("  V=verbose  P=progress  E=erreurs HTTP  D=debug")
    line("  Combine les codes : ex 123V")
    sep()
    disp = ask("Codes d'affichage (Entrée = aucun)")
    if disp:
        flags += ["-Display", disp]

    if ask_yn("Utiliser les cookies des réponses dans les requêtes (-usecookies)"):
        flags.append("-usecookies")

    if ask_yn("Suivre les redirections 3xx (-followredirects)"):
        flags.append("-followredirects")

    if ask_yn("Supprimer le slash final des URLs (-noslash)"):
        flags.append("-noslash")

    if ask_yn("Désactiver la résolution DNS (-nolookup)"):
        flags.append("-nolookup")

    if ask_yn("Désactiver la détection de page 404 (-no404)"):
        flags.append("-no404")

    if ask_yn("Ignorer certains codes HTTP en réponse négative (-404code)"):
        codes = ask_required("Codes séparés par virgule (ex: 302,301)")
        flags += ["-404code", codes]

    return flags

def get_advanced():
    section("6/6 — TIMING & OPTIONS AVANCÉES")
    flags = []

    if ask_yn("Timeout des requêtes (-timeout)  [défaut: 10s]"):
        t = ask_int("Timeout en secondes", min_val=1)
        flags += ["-timeout", t]

    if ask_yn("Durée max de test par hôte (-maxtime)  [ex: 1h, 30m, 3600s]"):
        mt = ask_required("Durée max (ex: 1h, 30m, 3600s)")
        flags += ["-maxtime", mt]

    if ask_yn("Pause entre les tests (-Pause)  [en secondes]"):
        p = ask_int("Pause en secondes", min_val=1)
        flags += ["-Pause", p]

    if ask_yn("Utiliser un proxy (-useproxy)  [configuré dans nikto.conf]"):
        flags.append("-useproxy")

    if ask_yn("User-agent personnalisé (-useragent)"):
        ua = ask_required("User-agent (ex: Mozilla/5.0 ...)")
        flags += ["-useragent", ua]

    if ask_yn("Scanner des répertoires CGI (-Cgidirs)"):
        line("")
        line("  [1] all   — tous les répertoires CGI")
        line("  [2] none  — aucun")
        line("  [3] Personnalisé  — ex: /cgi/ /cgi-bin/")
        sep()
        cgi = ask("Votre choix")
        if cgi == "1":   flags += ["-Cgidirs", "all"]
        elif cgi == "2": flags += ["-Cgidirs", "none"]
        elif cgi == "3":
            dirs = ask_required("Répertoires CGI (ex: /cgi/ /cgi-a/)")
            flags += ["-Cgidirs", dirs]

    if ask_yn("Désactiver les fonctions interactives (-nointeractive)"):
        flags.append("-nointeractive")

    return flags

def main():
    clear()
    banner()

    target_flags   = get_target()
    tuning_flags   = get_tuning()
    evasion_flags  = get_evasion()
    mutation_flags = get_mutation()
    output_flags   = get_output()
    advanced_flags = get_advanced()

    cmd = ["nikto"]
    cmd += target_flags
    cmd += tuning_flags
    cmd += evasion_flags
    cmd += mutation_flags
    cmd += output_flags
    cmd += advanced_flags

    host_display = target_flags[1] if len(target_flags) > 1 else "?"
    print(Fore.RED + "\n  ╔══ CONFIGURATION FINALE " + "═" * 31 + "╗")
    print(Fore.RED + "  ║  Cible    : " + Fore.WHITE + host_display)
    print(Fore.RED + "  ║  Tuning   : " + Fore.WHITE + f"{' '.join(tuning_flags) or 'complet (tout)'}")
    print(Fore.RED + "  ║  Évasion  : " + Fore.WHITE + f"{' '.join(evasion_flags) or 'aucune'}")
    print(Fore.RED + "  ║  Mutation : " + Fore.WHITE + f"{' '.join(mutation_flags) or 'aucune'}")
    print(Fore.RED + "  ║  Output   : " + Fore.WHITE + f"{' '.join(output_flags) or 'terminal'}")
    print(Fore.RED + "  ║  Avancé   : " + Fore.WHITE + f"{' '.join(advanced_flags) or 'défaut'}")
    print(Fore.RED + "  ╚" + "═" * 55)

    print(Fore.GREEN + f"\n  [+] Commande : " + Fore.WHITE + f"{' '.join(cmd)}\n")

    confirm = input(Fore.GREEN + "  [?] Lancer nikto ? (o/n) : ").strip().lower()
    if confirm not in ("o", "oui", "y", "yes"):
        print(Fore.GREEN + "\n  [-] Annulé.")
        sys.exit(0)

    print(Fore.GREEN + "\n  " + "─" * 56 + "\n")

    try:
        subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n  [!] Interrompu par l'utilisateur.")
    except FileNotFoundError:
        print(Fore.RED + "  [-] Nikto introuvable. Est-il installé et dans le PATH ?")

if __name__ == "__main__":
    main()
