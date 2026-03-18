import os
import sys
import subprocess
from colorama import Fore, init

init(autoreset=True)

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    print(Fore.GREEN + r"""
	▖ ▖▖  ▖▄▖▄▖                                
	▛▖▌▛▖▞▌▌▌▙▌                                
	▌▝▌▌▝ ▌▛▌▌                                 
                                           
                    ▌   ▜ ▘  ▗     ▜ ▌     
                    ▙▘▀▌▐ ▌▄▖▜▘▛▌▛▌▐ ▛▌▛▌▚▘
                    ▛▖█▌▐▖▌  ▐▖▙▌▙▌▐▖▙▌▙▌▞▖
                                           
	▄▖▖▖▄▖▖▖▄▖                                 
	▌ ▙▌▛▌▙▌▌                                  
	▙▖ ▌█▌ ▌▙▖
    """)
    print(Fore.RED + "           NMAP AUTOMATION TOOL  |  by C404C")
    print(Fore.RED + "              https://github.com/Charl-23\n")
    print(Fore.GREEN + "  " + "─" * 56 + "\n")

def section(title):
    print(Fore.GREEN + f"\n  ╔══ {title} " + "═" * (46 - len(title)) + "╗")

def ask(question, default=None):
    suffix = Fore.WHITE + f" [{default}]" if default else ""
    return input(Fore.GREEN + f"  [?] {question}{suffix} : " + Fore.WHITE).strip()

def ask_yn(question):
    r = input(Fore.GREEN + f"  [?] {question} " + Fore.WHITE + "(o/n) : ").strip().lower()
    return r in ("o", "oui", "y", "yes")

def line(text):
    print(Fore.WHITE + f"  ║  {text}")

def sep():
    print(Fore.GREEN + "  ╚" + "═" * 55)

def get_target():
    section("1/9 — SPÉCIFICATION DE LA CIBLE")
    line("Formats acceptés :")
    line("  IP unique      → 192.168.1.1")
    line("  Réseau CIDR    → 192.168.1.0/24")
    line("  Plage IP       → 10.0.0.1-254")
    line("  Domaine        → exemple.com")
    line("  Fichier liste  → taper -iL puis le chemin")
    line("  Cibles random  → taper -iR 100")
    sep()
    target = ask("Cible")
    if not target:
        print(Fore.GREEN + "  [-] Cible vide, abandon.")
        sys.exit(1)

    flags = []
    if ask_yn("Exclure des hôtes (--exclude)"):
        excl = ask("Hôtes à exclure (séparés par virgule)")
        flags += ["--exclude", excl]

    return target, flags

def get_host_discovery():
    section("2/9 — DÉCOUVERTE D'HÔTES (HOST DISCOVERY)")
    line("[1]  -sn   — Ping scan uniquement, pas de scan de ports")
    line("[2]  -Pn   — Ignorer ping, traiter tous les hôtes comme actifs")
    line("[3]  -PE   — Probe ICMP echo request")
    line("[4]  -PP   — Probe ICMP timestamp")
    line("[5]  -PM   — Probe ICMP netmask")
    line("[6]  -PS   — TCP SYN discovery (ports spécifiables)")
    line("[7]  -PA   — TCP ACK discovery")
    line("[8]  -PU   — UDP discovery")
    line("[9]  -n    — Ne jamais résoudre DNS (plus rapide)")
    line("[10] -R    — Toujours résoudre DNS")
    line("[0]  Par défaut nmap")
    sep()
    choice = ask("Votre choix")
    disc_map = {
        "1": ["-sn"], "2": ["-Pn"], "3": ["-PE"], "4": ["-PP"],
        "5": ["-PM"], "6": ["-PS"], "7": ["-PA"], "8": ["-PU"],
        "9": ["-n"],  "10": ["-R"],
    }
    return disc_map.get(choice, [])

def get_scan_technique():
    section("3/9 — TECHNIQUE DE SCAN")
    line("[1]  -sS  — TCP SYN Stealth   (furtif, requiert root)  ← recommandé")
    line("[2]  -sT  — TCP Connect       (sans root, moins discret)")
    line("[3]  -sU  — UDP               (détecte services UDP, lent)")
    line("[4]  -sA  — TCP ACK           (teste si ports filtrés/firewall)")
    line("[5]  -sW  — TCP Window        (variante ACK, certains OS)")
    line("[6]  -sM  — TCP Maimon        (FIN/ACK, évasion IDS)")
    line("[7]  -sN  — TCP Null          (aucun flag, passe certains firewalls)")
    line("[8]  -sF  — TCP FIN           (évasion IDS/firewall)")
    line("[9]  -sX  — Xmas Scan         (FIN+PSH+URG, évasion)")
    line("[10] -sI  — Idle/Zombie scan  (scan via un hôte tiers)")
    line("[11] -sO  — IP Protocol scan  (détecte protocoles IP supportés)")
    line("[12] -b   — FTP Bounce        (scan via serveur FTP)")
    line("[13] -sV  — Détection de version des services ouverts")
    line("[14] -sC  — Scripts NSE par défaut")
    line("[15] -A   — TOUT activer (OS + version + scripts + traceroute)")
    line("[0]  Aucun")
    sep()
    scan_map = {
        "1": ["-sS"], "2": ["-sT"], "3": ["-sU"], "4": ["-sA"],
        "5": ["-sW"], "6": ["-sM"], "7": ["-sN"], "8": ["-sF"],
        "9": ["-sX"], "11": ["-sO"], "13": ["-sV"],
        "14": ["-sC"], "15": ["-A"],
    }
    flags = []
    while True:
        choice = ask("Votre choix")
        if choice in scan_map:
            flags = scan_map[choice]
            break
        elif choice == "10":
            zombie = ask("Hôte zombie (ex: 192.168.1.5)")
            flags = ["-sI", zombie]
            break
        elif choice == "12":
            ftp = ask("Hôte FTP relais")
            flags = ["-b", ftp]
            break
        elif choice == "0":
            break
        else:
            print(Fore.GREEN + "  [-] Choix invalide.")

    if any(f in flags for f in ["-sV", "-A"]):
        line("")
        line("Intensité version detection :")
        line("  [1] --version-light  (intensité 2, rapide)")
        line("  [2] --version-all    (intensité 9, exhaustif)")
        line("  [3] Valeur manuelle  (0-9)")
        line("  [0] Par défaut")
        vi = ask("Votre choix")
        if vi == "1":   flags.append("--version-light")
        elif vi == "2": flags.append("--version-all")
        elif vi == "3":
            v = ask("Intensité (0-9)")
            flags += ["--version-intensity", v]

    return flags

def get_ports():
    section("4/9 — SPÉCIFICATION DES PORTS")
    line("[1]  -p <ports>        — Ports précis    ex: 22,80,443  ou  1-1000")
    line("[2]  --top-ports <n>   — Top N ports les plus courants  ex: 100")
    line("[3]  -F                — Fast mode (top 100 ports, rapide)")
    line("[4]  -p-               — Tous les ports (1-65535, très long)")
    line("[5]  -r                — Scan séquentiel (pas de randomisation)")
    line("[0]  Par défaut (top 1000 ports)")
    sep()
    choice = ask("Votre choix")
    flags = []
    if choice == "1":
        p = ask("Ports (ex: 22,80,443 ou 1-1000)")
        flags = ["-p", p]
    elif choice == "2":
        n = ask("Nombre de top ports (ex: 100, 500, 1000)")
        flags = ["--top-ports", n]
    elif choice == "3":
        flags = ["-F"]
    elif choice == "4":
        flags = ["-p-"]
    elif choice == "5":
        flags = ["-r"]

    if ask_yn("Exclure certains ports (--exclude-ports)"):
        excl = ask("Ports à exclure (ex: 80,443)")
        flags += ["--exclude-ports", excl]

    return flags

def get_os():
    section("5/9 — DÉTECTION DU SYSTÈME D'EXPLOITATION")
    line("[1]  -O                       — Détection OS standard")
    line("[2]  -O --osscan-guess        — Estimation agressive si résultat incertain")
    line("[3]  -O --osscan-limit        — Limiter aux cibles avec ports ouverts clairs")
    line("[0]  Désactivé")
    sep()
    choice = ask("Votre choix")
    return {
        "1": ["-O"],
        "2": ["-O", "--osscan-guess"],
        "3": ["-O", "--osscan-limit"],
    }.get(choice, [])

def get_timing():
    section("6/9 — TIMING & PERFORMANCE")
    line("[0]  -T0  Paranoid   → 1 probe/5min, invisible pour IDS")
    line("[1]  -T1  Sneaky     → très lent, discret")
    line("[2]  -T2  Polite     → lent, pas de saturation réseau")
    line("[3]  -T3  Normal     → comportement par défaut de nmap  ← recommandé")
    line("[4]  -T4  Aggressive → rapide, suppose réseau fiable")
    line("[5]  -T5  Insane     → ultra rapide, peut rater des résultats")
    sep()
    while True:
        choice = ask("Timing (0-5)")
        if choice in [str(i) for i in range(6)]:
            flags = [f"-T{choice}"]
            break
        print(Fore.GREEN + "  [-] Entrez 0, 1, 2, 3, 4 ou 5.")

    if ask_yn("Options avancées de timing"):
        if ask_yn("  --min-rate  (paquets/sec minimum)"):
            r = ask("  Valeur min-rate (ex: 100)")
            flags += ["--min-rate", r]
        if ask_yn("  --max-rate  (paquets/sec maximum)"):
            r = ask("  Valeur max-rate (ex: 500)")
            flags += ["--max-rate", r]
        if ask_yn("  --max-retries  (tentatives max par port)"):
            r = ask("  Valeur (ex: 3)")
            flags += ["--max-retries", r]
        if ask_yn("  --host-timeout  (abandon hôte après délai)"):
            r = ask("  Valeur (ex: 30m, 2h, 5s)")
            flags += ["--host-timeout", r]
        if ask_yn("  --scan-delay  (délai entre probes)"):
            r = ask("  Valeur (ex: 1s, 500ms)")
            flags += ["--scan-delay", r]

    return flags

def get_scripts():
    section("7/9 — SCRIPTS NSE (NMAP SCRIPTING ENGINE)")
    line("[1]  --script=default    — Scripts sûrs par défaut")
    line("[2]  --script=vuln       — Détection de vulnérabilités connues")
    line("[3]  --script=auth       — Tests d'authentification (logins, bypass)")
    line("[4]  --script=exploit    — Exploitation active de vulnérabilités")
    line("[5]  --script=discovery  — Découverte réseau étendue")
    line("[6]  --script=safe       — Scripts garantis sans danger pour la cible")
    line("[7]  --script=brute      — Brute-force logins et services")
    line("[8]  --script=malware    — Détection d'infections / backdoors")
    line("[9]  Script personnalisé — Entrer manuellement le nom")
    line("[0]  Aucun script")
    sep()
    script_map = {
        "1": "default", "2": "vuln",      "3": "auth",
        "4": "exploit",  "5": "discovery", "6": "safe",
        "7": "brute",    "8": "malware",
    }
    flags = []
    choice = ask("Votre choix")
    if choice in script_map:
        flags = [f"--script={script_map[choice]}"]
    elif choice == "9":
        s = ask("Nom du script ou catégorie")
        flags = [f"--script={s}"]

    if flags:
        if ask_yn("Passer des arguments aux scripts (--script-args)"):
            args = ask("Arguments (ex: user=admin,pass=1234)")
            flags += ["--script-args", args]
        if ask_yn("Voir le trafic détaillé des scripts (--script-trace)"):
            flags.append("--script-trace")

    return flags

def get_evasion():
    section("8/9 — ÉVASION FIREWALL / IDS / SPOOFING")
    flags = []

    if ask_yn("Fragmenter les paquets (-f)  [contourne certains firewalls]"):
        flags.append("-f")
        if ask_yn("  MTU personnalisé (--mtu, multiple de 8)"):
            mtu = ask("  Valeur MTU (ex: 16, 24)")
            flags += ["--mtu", mtu]

    if ask_yn("Utiliser des leurres (-D)  [cache ton IP parmi des faux scanneurs]"):
        decoys = ask("  Leurres séparés par virgule (ex: 10.0.0.1,10.0.0.2,ME)")
        flags += ["-D", decoys]

    if ask_yn("Spoofer l'IP source (-S)  [attention: réponses perdues]"):
        ip = ask("  IP source à usurper")
        flags += ["-S", ip]

    if ask_yn("Spoofer l'adresse MAC (--spoof-mac)"):
        mac = ask("  MAC, prefix ou vendeur (ex: Apple, 00:11:22, random)", "random")
        flags += ["--spoof-mac", mac]

    if ask_yn("Port source fixe (-g)  [ex: 53 ou 80 pour passer firewall]"):
        port = ask("  Port source (ex: 53, 80)")
        flags += ["-g", port]

    if ask_yn("Passer par un proxy HTTP/SOCKS4 (--proxies)"):
        prox = ask("  URL du proxy (ex: http://127.0.0.1:8080)")
        flags += ["--proxies", prox]

    if ask_yn("TTL personnalisé (--ttl)  [modifie la durée de vie IP]"):
        ttl = ask("  Valeur TTL (ex: 64, 128)")
        flags += ["--ttl", ttl]

    if ask_yn("Données aléatoires dans paquets (--data-length)  [leurre IDS]"):
        dl = ask("  Longueur en octets (ex: 25)")
        flags += ["--data-length", dl]

    if ask_yn("Checksums invalides (--badsum)  [teste si IDS filtre correctement]"):
        flags.append("--badsum")

    if ask_yn("Spécifier l'interface réseau (-e)"):
        iface = ask("  Interface (ex: eth0, wlan0)")
        flags += ["-e", iface]

    return flags

def get_output_misc():
    section("9/9 — OUTPUT & OPTIONS DIVERSES")
    flags = []

    line("Format de sortie fichier :")
    line("  [1] -oN  — Normal (texte lisible)")
    line("  [2] -oX  — XML   (import tools)")
    line("  [3] -oG  — Grepable (grep/awk)")
    line("  [4] -oA  — Les 3 formats simultanément")
    line("  [0] Pas de fichier de sortie")
    sep()
    choice = ask("Format de sortie")
    out_map = {"1": "-oN", "2": "-oX", "3": "-oG", "4": "-oA"}
    if choice in out_map:
        fname = ask("Nom du fichier (sans extension)", "scan_result")
        flags += [out_map[choice], fname]

    if ask_yn("Mode verbeux (-vv)  [affiche plus de détails en temps réel]"):
        flags.append("-vv")

    if ask_yn("Mode debug (-dd)  [informations très détaillées pour debugging]"):
        flags.append("-dd")

    if ask_yn("Afficher seulement les ports OUVERTS (--open)"):
        flags.append("--open")

    if ask_yn("Afficher la raison de l'état de chaque port (--reason)"):
        flags.append("--reason")

    if ask_yn("Traceroute (--traceroute)  [trace le chemin réseau vers la cible]"):
        flags.append("--traceroute")

    if ask_yn("Scanner en IPv6 (-6)"):
        flags.append("-6")

    if ask_yn("Afficher les interfaces et routes locales (--iflist)"):
        flags.append("--iflist")

    if ask_yn("Ajouter au fichier existant plutôt qu'écraser (--append-output)"):
        flags.append("--append-output")

    return flags

def main():
    clear()
    banner()

    target, target_flags = get_target()
    discovery            = get_host_discovery()
    scan_tech            = get_scan_technique()
    ports                = get_ports()
    os_det               = get_os()
    timing               = get_timing()
    scripts              = get_scripts()
    evasion              = get_evasion()
    output_misc          = get_output_misc()

    cmd = ["nmap"]
    cmd += scan_tech
    cmd += discovery
    cmd += ports
    cmd += os_det
    cmd += timing
    cmd += scripts
    cmd += evasion
    cmd += output_misc
    cmd += target_flags
    cmd.append(target)

    print(Fore.RED + "\n  ╔══ CONFIGURATION FINALE " + "═" * 31 + "╗")
    print(Fore.RED + "  ║  Cible      : " + Fore.WHITE + f"{target}")
    print(Fore.RED + "  ║  Scan       : " + Fore.WHITE + f"{' '.join(scan_tech) or 'défaut'}")
    print(Fore.RED + "  ║  Discovery  : " + Fore.WHITE + f"{' '.join(discovery) or 'défaut'}")
    print(Fore.RED + "  ║  Ports      : " + Fore.WHITE + f"{' '.join(ports) or 'top 1000'}")
    print(Fore.RED + "  ║  OS Detect  : " + Fore.WHITE + f"{' '.join(os_det) or 'non'}")
    print(Fore.RED + "  ║  Timing     : " + Fore.WHITE + f"{timing[0] if timing else 'T3'}")
    print(Fore.RED + "  ║  Scripts    : " + Fore.WHITE + f"{' '.join(scripts) or 'aucun'}")
    print(Fore.RED + "  ║  Évasion    : " + Fore.WHITE + f"{' '.join(evasion) or 'aucune'}")
    print(Fore.RED + "  ╚" + "═" * 55)

    print(Fore.GREEN + f"\n  [+] Commande : " + Fore.WHITE + f"{' '.join(cmd)}\n")

    confirm = input(Fore.GREEN + "  [?] Lancer nmap ? (o/n) : ").strip().lower()
    if confirm not in ("o", "oui", "y", "yes"):
        print(Fore.GREEN + "\n  [-] Annulé.")
        sys.exit(0)

    print(Fore.GREEN + "\n  " + "─" * 56 + "\n")

    try:
        subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        print(Fore.GREEN + "\n\n  [!] Interrompu par l'utilisateur.")
    except FileNotFoundError:
        print(Fore.GREEN + "  [-] Nmap introuvable. Est-il installé et dans le PATH ?")

if __name__ == "__main__":
    main()
