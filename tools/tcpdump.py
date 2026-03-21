import os
import sys
import subprocess
from colorama import Fore, init

init(autoreset=True)

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    print(Fore.GREEN + r"""
  ████████╗ ██████╗██████╗ ██████╗ ██╗   ██╗███╗   ███╗██████╗ 
  ╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██║   ██║████╗ ████║██╔══██╗
     ██║   ██║     ██████╔╝██║  ██║██║   ██║██╔████╔██║██████╔╝
     ██║   ██║     ██╔═══╝ ██║  ██║██║   ██║██║╚██╔╝██║██╔═══╝ 
     ██║   ╚██████╗██║     ██████╔╝╚██████╔╝██║ ╚═╝ ██║██║     
     ╚═╝    ╚═════╝╚═╝     ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝     
    """)
    print(Fore.RED + "          TCPDUMP AUTOMATION TOOL  |  by C404C")
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

# ══════════════════════════════════════════════════════════
# 1. MODE (CAPTURE / LECTURE)
# ══════════════════════════════════════════════════════════
def get_mode():
    section("1/5 — MODE")
    line("[1]  Capture en direct  — Écouter une interface réseau en temps réel")
    line("[2]  Lecture de fichier — Analyser un fichier .pcap existant (-r)")
    sep()
    while True:
        choice = ask("Votre choix (1/2)")
        if choice in ("1", "2"):
            return choice
        print(Fore.RED + "  [-] Choix invalide.")

# ══════════════════════════════════════════════════════════
# 2A. INTERFACE (MODE CAPTURE)
# ══════════════════════════════════════════════════════════
def get_interface():
    section("2/5 — INTERFACE RÉSEAU")
    line("Interfaces courantes sur Kali :")
    line("  eth0    — Ethernet filaire")
    line("  wlan0   — WiFi")
    line("  lo      — Loopback (trafic local)")
    line("  any     — Toutes les interfaces")
    line("  tun0    — VPN / TUN")
    sep()

    iface = ask_required("Interface (-i)  (ex: eth0, wlan0, any)")
    return ["-i", iface]

# ══════════════════════════════════════════════════════════
# 2B. FICHIER PCAP (MODE LECTURE)
# ══════════════════════════════════════════════════════════
def get_read_file():
    section("2/5 — FICHIER DE CAPTURE")
    line("Fichier .pcap / .pcapng capturé précédemment")
    sep()
    while True:
        f = ask_required("Chemin du fichier (-r)  (ex: /root/capture.pcap)")
        if check_file(f):
            return ["-r", f]
        if ask_yn("Continuer quand même"):
            return ["-r", f]

# ══════════════════════════════════════════════════════════
# 3. FILTRE BPF
# ══════════════════════════════════════════════════════════
def get_filter():
    section("3/5 — FILTRE BPF (Berkeley Packet Filter)")
    line("Filtres courants — tu peux les combiner avec 'and', 'or', 'not' :")
    line("")
    line("  ── Par protocole ─────────────────────────────────")
    line("  tcp              — Tout le trafic TCP")
    line("  udp              — Tout le trafic UDP")
    line("  icmp             — Ping / ICMP")
    line("  arp              — Requêtes ARP")
    line("  dns              — DNS  (udp port 53)")
    line("  http             — HTTP  (tcp port 80)")
    line("  https            — HTTPS  (tcp port 443)")
    line("  ── Par port ──────────────────────────────────────")
    line("  port 80          — Port 80 (src ou dst)")
    line("  dst port 443     — Destination port 443")
    line("  src port 22      — Source port 22")
    line("  portrange 1-1024 — Plage de ports")
    line("  ── Par IP ────────────────────────────────────────")
    line("  host 192.168.1.1         — Trafic vers/depuis cet hôte")
    line("  src host 10.0.0.1        — Seulement en provenance")
    line("  dst host 10.0.0.1        — Seulement à destination")
    line("  net 192.168.1.0/24       — Tout un réseau")
    line("  ── Combinaisons exemples ─────────────────────────")
    line("  tcp and port 80                   — HTTP uniquement")
    line("  host 192.168.1.1 and port 22      — SSH vers/depuis hôte")
    line("  not arp and not icmp              — Exclure ARP et ICMP")
    line("  tcp and (port 80 or port 443)     — HTTP + HTTPS")
    line("")
    line("  [0] Aucun filtre (tout capturer)")
    sep()
    f = ask("Filtre BPF (ou 0 pour aucun)")
    if f and f != "0":
        return f
    return ""

# ══════════════════════════════════════════════════════════
# 4. OPTIONS DE CAPTURE
# ══════════════════════════════════════════════════════════
def get_capture_options(mode):
    section("4/5 — OPTIONS DE CAPTURE")
    flags = []

    # Limite de paquets
    if ask_yn("Limiter le nombre de paquets capturés (-c)"):
        c = ask_int("Nombre de paquets (ex: 100, 1000)", min_val=1)
        flags += ["-c", c]

    # Snaplen
    if ask_yn("Taille de capture par paquet (-s)  [défaut: 262144 bytes = tout]"):
        line("")
        line("  0        → Capturer le paquet entier (recommandé)")
        line("  68       → Headers seulement (économique)")
        line("  1500     → MTU Ethernet standard")
        sep()
        s = ask_int("Snaplen en bytes", min_val=0)
        flags += ["-s", s]

    # Timestamp
    if ask_yn("Timestamp précision (--nano ou --micro)"):
        line("")
        line("  [1] --micro  — Microsecondes  (défaut)")
        line("  [2] --nano   — Nanosecondes   (plus précis)")
        sep()
        ts = ask("Votre choix")
        if ts == "1":   flags.append("--micro")
        elif ts == "2": flags.append("--nano")

    # Rotation de fichier (seulement en capture live)
    if mode == "1":
        if ask_yn("Rotation automatique de fichier (-G)  [capture par tranches]"):
            g = ask_int("Rotation toutes les X secondes (ex: 60 = 1min)", min_val=1)
            flags += ["-G", g]
            if ask_yn("Limiter le nombre de fichiers (-W)"):
                w = ask_int("Nombre max de fichiers", min_val=1)
                flags += ["-W", w]

        if ask_yn("Taille max par fichier de capture (-C)  [en MB]"):
            c_size = ask_int("Taille en MB (ex: 10, 100)", min_val=1)
            flags += ["-C", c_size]

    return flags

# ══════════════════════════════════════════════════════════
# 5. OUTPUT & AFFICHAGE
# ══════════════════════════════════════════════════════════
def get_output():
    section("5/5 — OUTPUT & AFFICHAGE")
    flags = []

    # Écriture dans un fichier
    if ask_yn("Sauvegarder la capture dans un fichier .pcap (-w)"):
        f = ask_required("Chemin du fichier (ex: /root/capture.pcap)")
        flags += ["-w", f]

    # Résolution DNS
    if ask_yn("Désactiver la résolution DNS (-n)  [affiche les IPs brutes, plus rapide]"):
        flags.append("-n")

    if ask_yn("Désactiver aussi la résolution des ports (-nn)  [ex: 80→80 et non 'http']"):
        flags.append("-nn")

    # Verbose
    line("")
    line("Niveau de verbosité :")
    line("  [1] -v   — Verbeux  (TTL, checksum...)")
    line("  [2] -vv  — Plus verbeux")
    line("  [3] -vvv — Maximum")
    line("  [0] Aucun")
    sep()
    v = ask("Votre choix")
    if v == "1":   flags.append("-v")
    elif v == "2": flags.append("-vv")
    elif v == "3": flags.append("-vvv")

    # Affichage du contenu
    if ask_yn("Afficher le contenu en ASCII (-A)  [utile pour HTTP]"):
        flags.append("-A")
    elif ask_yn("Afficher en HEX + ASCII (-X)"):
        flags.append("-X")
    elif ask_yn("Afficher en HEX + ASCII avec header Ethernet (-XX)"):
        flags.append("-XX")

    # Mode immédiat
    if ask_yn("Mode ligne par ligne immédiat (-l)  [utile pour grep/pipe]"):
        flags.append("-l")

    # Pas de promiscuous mode
    if ask_yn("Désactiver le mode promiscuous (-p)  [capture seulement son propre trafic]"):
        flags.append("-p")

    # Afficher les numéros absolus
    if ask_yn("Afficher les numéros de séquence absolus (-S)"):
        flags.append("-S")

    # Afficher les numéros de paquets
    if ask_yn("Afficher le numéro de chaque paquet (#)"):
        flags.append("--number")

    return flags

# ══════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════
def main():
    clear()
    banner()

    # Vérif root pour capture live
    mode = get_mode()
    if mode == "1" and os.geteuid() != 0:
        print(Fore.RED + "\n  [!] La capture en direct nécessite les droits root (sudo).\n")
        sys.exit(1)

    if mode == "1":
        source_flags = get_interface()
    else:
        source_flags = get_read_file()

    bpf_filter      = get_filter()
    capture_flags   = get_capture_options(mode)
    output_flags    = get_output()

    # Construction de la commande
    cmd = ["tcpdump"]
    cmd += source_flags
    cmd += capture_flags
    cmd += output_flags
    if bpf_filter:
        cmd.append(bpf_filter)

    # Résumé
    mode_label = "Capture en direct" if mode == "1" else "Lecture de fichier"
    print(Fore.RED + "\n  ╔══ CONFIGURATION FINALE " + "═" * 31 + "╗")
    print(Fore.RED + "  ║  Mode     : " + Fore.WHITE + mode_label)
    print(Fore.RED + "  ║  Source   : " + Fore.WHITE + f"{' '.join(source_flags)}")
    print(Fore.RED + "  ║  Filtre   : " + Fore.WHITE + (bpf_filter or "aucun (tout capturer)"))
    print(Fore.RED + "  ║  Capture  : " + Fore.WHITE + f"{' '.join(str(x) for x in capture_flags) or 'défaut'}")
    print(Fore.RED + "  ║  Output   : " + Fore.WHITE + f"{' '.join(output_flags) or 'terminal'}")
    print(Fore.RED + "  ╚" + "═" * 55)

    print(Fore.GREEN + f"\n  [+] Commande : " + Fore.WHITE + f"{' '.join(str(x) for x in cmd)}\n")

    confirm = input(Fore.GREEN + "  [?] Lancer tcpdump ? (o/n) : ").strip().lower()
    if confirm not in ("o", "oui", "y", "yes"):
        print(Fore.GREEN + "\n  [-] Annulé.")
        sys.exit(0)

    print(Fore.GREEN + "\n  " + "─" * 56 + "\n")
    print(Fore.WHITE + "  Ctrl+C pour arrêter la capture.\n")

    try:
        subprocess.run([str(x) for x in cmd], check=False)
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n  [!] Capture arrêtée.")
    except FileNotFoundError:
        print(Fore.RED + "  [-] tcpdump introuvable. Est-il installé et dans le PATH ?")

if __name__ == "__main__":
    main()
