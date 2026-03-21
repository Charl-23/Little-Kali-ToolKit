import os
import sys
import subprocess
from colorama import Fore, init

init(autoreset=True)

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    print(Fore.GREEN + r"""
	▌     ▌     ▗                        
	▛▌▀▌▛▘▛▌▛▘▀▌▜▘                       
	▌▌█▌▄▌▌▌▙▖█▌▐▖                       
	                                     
              ▌   ▜ ▘  ▗     ▜ ▌     
              ▙▘▀▌▐ ▌  ▜▘▛▌▛▌▐ ▛▌▛▌▚▘
              ▛▖█▌▐▖▌  ▐▖▙▌▙▌▐▖▙▌▙▌▞▖
                                     
	▄▖▖▖▄▖▖▖▄▖                           
	▌ ▙▌▛▌▙▌▌                            
	▙▖ ▌█▌ ▌▙
    """)
    print(Fore.RED + "          HASHCAT AUTOMATION TOOL  |  by C404C")
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

def get_hash_type():
    section("1/5 — TYPE DE HASH (-m)")
    line("Codes les plus courants :")
    line("")
    line("  ── Linux / Unix ──────────────────────────────────")
    line("  [1]  500   — md5crypt  ($1$)  /etc/shadow Linux MD5")
    line("  [2]  1800  — sha512crypt  ($6$)  /etc/shadow SHA-512  ← courant")
    line("  [3]  7400  — sha256crypt  ($5$)  /etc/shadow SHA-256")
    line("  ── Windows ───────────────────────────────────────")
    line("  [4]  1000  — NTLM  ← Windows moderne")
    line("  [5]  3000  — LM    ← Windows ancien")
    line("  [6]  5600  — NetNTLMv2  ← captures réseau")
    line("  ── Web / CMS ─────────────────────────────────────")
    line("  [7]  0     — MD5 brut")
    line("  [8]  100   — SHA1 brut")
    line("  [9]  1400  — SHA256 brut")
    line("  [10] 1700  — SHA512 brut")
    line("  [11] 400   — phpBB3 / WordPress  ($P$)")
    line("  [12] 3200  — bcrypt  ($2a$, $2b$)")
    line("  ── WiFi ──────────────────────────────────────────")
    line("  [13] 2500  — WPA-EAPOL-PBKDF2  (hccapx)")
    line("  [14] 22000 — WPA-PBKDF2-PMKID+EAPOL  ← hashcat moderne")
    line("  [15] 16800 — WPA-PMKID-PBKDF2  (PMKID)")
    line("  ── Bases de données ──────────────────────────────")
    line("  [16] 300   — MySQL4.1/MySQL5+")
    line("  [17] 1731  — MSSQL (2012, 2014)")
    line("  ── Autres ────────────────────────────────────────")
    line("  [18] 13100 — Kerberos 5, etype 23, TGS-REP  (Kerberoast)")
    line("  [19] 18200 — Kerberos 5, AS-REP  (ASREPRoast)")
    line("  [20] 13400 — KeePass 1/2")
    line("  [21] 11600 — 7-Zip")
    line("  [22] 13600 — WinZip")
    line("  [23] Personnalisé — Entrer le code manuellement")
    line("  [0]  Auto-detect — hashcat tente de détecter")
    sep()
    hash_map = {
        "1": "500",   "2": "1800",  "3": "7400",
        "4": "1000",  "5": "3000",  "6": "5600",
        "7": "0",     "8": "100",   "9": "1400",
        "10": "1700", "11": "400",  "12": "3200",
        "13": "2500", "14": "22000","15": "16800",
        "16": "300",  "17": "1731", "18": "13100",
        "19": "18200","20": "13400","21": "11600",
        "22": "13600",
    }
    while True:
        choice = ask("Votre choix")
        if choice in hash_map:
            return ["-m", hash_map[choice]]
        elif choice == "23":
            code = ask_int("Code du hash (voir hashcat --help)", min_val=0)
            return ["-m", code]
        elif choice == "0":
            return []
        print(Fore.RED + "  [-] Choix invalide.")

def get_hashfile():
    section("2/5 — FICHIER DE HASHES")
    line("Fichier contenant le(s) hash(es) à cracker")
    line("Ex: hashes.txt  |  /root/capture.hccapx  |  5f4dcc3b5aa765d61d8327deb882cf99")
    line("")
    line("  → Un hash direct (coller le hash brut)")
    line("  → Ou un fichier contenant les hashes (un par ligne)")
    sep()
    return ask_required("Hash ou chemin du fichier de hashes")

def get_attack_mode():
    section("3/5 — MODE D'ATTAQUE (-a)")
    line("[0]  Straight      — Wordlist simple  ← le plus utilisé")
    line("                     Chaque mot de la wordlist est testé tel quel")
    line("[1]  Combination   — Combine deux wordlists")
    line("                     Chaque mot de liste1 est concaténé avec liste2")
    line("[3]  Brute-force   — Masque de caractères")
    line("                     Génère toutes les combinaisons possibles")
    line("[6]  Hybrid        — Wordlist + Masque")
    line("                     Ajoute un masque à la FIN de chaque mot")
    line("[7]  Hybrid        — Masque + Wordlist")
    line("                     Ajoute un masque au DÉBUT de chaque mot")
    line("[9]  Association   — Un candidat par hash (wordlist 1:1)")
    sep()
    mode_map = {"0": "0", "1": "1", "3": "3", "6": "6", "7": "7", "9": "9"}
    while True:
        choice = ask("Votre choix (0/1/3/6/7/9)")
        if choice in mode_map:
            return choice
        print(Fore.RED + "  [-] Choix invalide.")

def get_straight_args():
    flags = []
    while True:
        wl = ask_required("Wordlist (-w)  (ex: /usr/share/wordlists/rockyou.txt)")
        if check_file(wl):
            break
        if ask_yn("Continuer quand même"):
            break

    if ask_yn("Appliquer des règles (-r)"):
        line("")
        line("Règles courantes sur Kali :")
        line("  /usr/share/hashcat/rules/best64.rule     ← recommandé")
        line("  /usr/share/hashcat/rules/rockyou-30000.rule")
        line("  /usr/share/hashcat/rules/d3ad0ne.rule")
        line("  /usr/share/hashcat/rules/Hob0Rules.rule")
        sep()
        while True:
            rf = ask_required("Chemin du fichier de règles")
            if check_file(rf):
                break
            if ask_yn("Continuer quand même"):
                break
        flags += ["-r", rf]

    return [wl] + flags

def get_combination_args():
    print(Fore.WHITE + "  Chaque mot de liste1 sera concaténé avec chaque mot de liste2.\n")
    while True:
        wl1 = ask_required("Wordlist 1")
        if check_file(wl1): break
        if ask_yn("Continuer quand même"): break
    while True:
        wl2 = ask_required("Wordlist 2")
        if check_file(wl2): break
        if ask_yn("Continuer quand même"): break
    return [wl1, wl2]

def get_bruteforce_args():
    flags = []
    line("")
    line("Charsets intégrés :")
    line("  ?l = minuscules (a-z)     ?u = majuscules (A-Z)")
    line("  ?d = chiffres (0-9)       ?s = caractères spéciaux")
    line("  ?a = tout (?l?u?d?s)      ?h = hex minuscule (0-9a-f)")
    line("  ?H = hex majuscule        ?b = 0x00-0xff")
    line("")
    line("Ex: ?a?a?a?a?a?a    = 6 chars quelconques")
    line("    ?u?l?l?l?d?d    = Maj + 3min + 2chiffres  (type 'Admin42')")
    line("    ?d?d?d?d        = 4 chiffres (PIN)")
    sep()
    mask = ask_required("Masque (ex: ?a?a?a?a?a?a?a?a)")

    if ask_yn("Mode incrémental (-i)  [teste de 1 char jusqu'au masque]"):
        flags.append("-i")
        if ask_yn("  Longueur minimale (--increment-min)"):
            mn = ask_int("  Min", min_val=1)
            flags += ["--increment-min", mn]
        if ask_yn("  Longueur maximale (--increment-max)"):
            mx = ask_int("  Max", min_val=1)
            flags += ["--increment-max", mx]

    return [mask] + flags

def get_hybrid_args(mode):
    line("")
    if mode == "6":
        line("Mode 6 : mot_de_wordlist + masque  (ex: password123)")
    else:
        line("Mode 7 : masque + mot_de_wordlist  (ex: 123password)")
    sep()
    while True:
        wl = ask_required("Wordlist")
        if check_file(wl): break
        if ask_yn("Continuer quand même"): break
    mask = ask_required("Masque (ex: ?d?d?d ou ?s?d?d?d)")
    if mode == "6":
        return [wl, mask]
    else:
        return [mask, wl]

def get_association_args():
    print(Fore.WHITE + "  Mode 1:1 — un candidat par hash (wordlist correspondante).\n")
    while True:
        wl = ask_required("Wordlist (un candidat par ligne, correspondant au hash)")
        if check_file(wl): break
        if ask_yn("Continuer quand même"): break
    flags = []
    if ask_yn("Appliquer des règles (-r)"):
        rf = ask_required("Chemin du fichier de règles")
        flags += ["-r", rf]
    return [wl] + flags

def get_options():
    section("4/5 — PERFORMANCE & OPTIONS")
    flags = []

    line("Profil de charge (-w) :")
    line("  [1] Low       — Minimal impact  (PC utilisable)")
    line("  [2] Default   — Équilibré")
    line("  [3] High      — Rapide  (PC inutilisable)  ← recommandé")
    line("  [4] Nightmare — Maximum  (GPU à fond)")
    line("  [0] Par défaut")
    sep()
    wp = ask("Profil de charge")
    if wp in ("1", "2", "3", "4"):
        flags += ["-w", wp]

    if ask_yn("Optimiser les kernels GPU (-O)  [limite la longueur des mots, +vitesse]"):
        flags.append("-O")

    if ask_yn("Spécifier les devices GPU/CPU (-d)  [ex: 1 ou 1,2]"):
        d = ask_required("Devices (ex: 1 ou 1,2)")
        flags += ["-d", d]

    if ask_yn("Limiter la température GPU (--hwmon-temp-abort)"):
        t = ask_int("Température max en °C (ex: 85)", min_val=50, max_val=110)
        flags += ["--hwmon-temp-abort", t]

    if ask_yn("Arrêter après X secondes (--runtime)"):
        r = ask_int("Durée en secondes", min_val=1)
        flags += ["--runtime", r]

    if ask_yn("Nommer la session (--session)  [pour la reprendre]"):
        name = ask_required("Nom de session (ex: crack_admin)")
        flags += ["--session", name]

    if ask_yn("Reprendre une session (--restore)"):
        flags.append("--restore")

    if ask_yn("Ignorer les warnings (--force)  [à utiliser avec précaution]"):
        flags.append("--force")

    if ask_yn("Activer le status automatique (--status)"):
        flags.append("--status")
        if ask_yn("  Intervalle status (--status-timer)  [secondes]"):
            st = ask_int("  Intervalle", min_val=1)
            flags += ["--status-timer", st]

    return flags

def get_output():
    section("5/5 — OUTPUT")
    flags = []

    if ask_yn("Sauvegarder les hashes crackés dans un fichier (-o)"):
        f = ask_required("Chemin du fichier (ex: /root/cracked.txt)")
        flags += ["-o", f]

        line("")
        line("Format de sortie (--outfile-format) :")
        line("  1 = hash[:salt]   2 = mot de passe   3 = hex du mdp")
        line("  4 = crack_pos     5 = timestamp abs   6 = timestamp rel")
        line("  Combine : ex 1,2,3")
        sep()
        fmt = ask("Format(s) (Entrée = défaut)", "1,2")
        if not fmt:
            fmt = "1,2"
        flags += ["--outfile-format", fmt]

    if ask_yn("Afficher les hashes déjà crackés (--show)"):
        flags.append("--show")

    if ask_yn("Afficher les hashes non crackés (--left)"):
        flags.append("--left")

    if ask_yn("Mode silencieux (--quiet)"):
        flags.append("--quiet")

    if ask_yn("Supprimer les hashes du fichier une fois crackés (--remove)"):
        flags.append("--remove")

    if ask_yn("Désactiver le fichier potfile (--potfile-disable)"):
        flags.append("--potfile-disable")

    return flags

def main():
    clear()
    banner()

    hash_flags   = get_hash_type()
    hashfile     = get_hashfile()
    attack_mode  = get_attack_mode()

    mode_labels = {
        "0": "Straight (Wordlist)",
        "1": "Combination",
        "3": "Brute-force (Mask)",
        "6": "Hybrid Wordlist+Mask",
        "7": "Hybrid Mask+Wordlist",
        "9": "Association",
    }
    if attack_mode == "0":
        extra_args = get_straight_args()
    elif attack_mode == "1":
        extra_args = get_combination_args()
    elif attack_mode == "3":
        extra_args = get_bruteforce_args()
    elif attack_mode in ("6", "7"):
        extra_args = get_hybrid_args(attack_mode)
    elif attack_mode == "9":
        extra_args = get_association_args()
    else:
        extra_args = []

    perf_flags   = get_options()
    output_flags = get_output()

    cmd = ["hashcat"]
    cmd += hash_flags
    cmd += ["-a", attack_mode]
    cmd += perf_flags
    cmd += output_flags
    cmd.append(hashfile)
    cmd += extra_args

    print(Fore.RED + "\n  ╔══ CONFIGURATION FINALE " + "═" * 31 + "╗")
    print(Fore.RED + "  ║  Hash type : " + Fore.WHITE + f"{' '.join(hash_flags) or 'auto'}")
    print(Fore.RED + "  ║  Mode      : " + Fore.WHITE + mode_labels.get(attack_mode, "?"))
    print(Fore.RED + "  ║  Fichier   : " + Fore.WHITE + hashfile)
    print(Fore.RED + "  ║  Args      : " + Fore.WHITE + f"{' '.join(str(x) for x in extra_args)}")
    print(Fore.RED + "  ║  Perf      : " + Fore.WHITE + f"{' '.join(perf_flags) or 'défaut'}")
    print(Fore.RED + "  ║  Output    : " + Fore.WHITE + f"{' '.join(output_flags) or 'terminal'}")
    print(Fore.RED + "  ╚" + "═" * 55)

    print(Fore.GREEN + f"\n  [+] Commande : " + Fore.WHITE + f"{' '.join(str(x) for x in cmd)}\n")

    confirm = input(Fore.GREEN + "  [?] Lancer hashcat ? (o/n) : ").strip().lower()
    if confirm not in ("o", "oui", "y", "yes"):
        print(Fore.GREEN + "\n  [-] Annulé.")
        sys.exit(0)

    print(Fore.GREEN + "\n  " + "─" * 56 + "\n")

    try:
        subprocess.run([str(x) for x in cmd], check=False)
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n  [!] Interrompu par l'utilisateur.")
    except FileNotFoundError:
        print(Fore.RED + "  [-] Hashcat introuvable. Est-il installé et dans le PATH ?")

if __name__ == "__main__":
    main()
