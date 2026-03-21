<div align="center">

# ⚔️ Little Kali ToolKit

<img src="https://img.shields.io/badge/Platform-Kali%20Linux-557C94?style=for-the-badge&logo=linux&logoColor=white"/>
<img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Tools-14-red?style=for-the-badge"/>
<img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge"/>

<br/>

**Suite d'outils pour le pentesting, réseau, cracking, WiFi et ingénierie sociale.**

</div>

---

## 📸 Aperçu / Preview

<div align="center">
  <img src="assets/menu.png" alt="Menu principal" width="750"/>
</div>

---

## 📁 Structure du projet

```
Little-Kali-ToolKit/
├── multitool.py          ← Launcher principal (menu interactif)
├── assets/
│   └── menu.png
└── tools/
    ├── nmap.py
    ├── sqlmap.py
    ├── commix.py
    ├── wifite.py
    ├── setoolkit.py
    ├── aircrack.py
    ├── john.py
    ├── hashcat.py
    ├── hydra.py
    ├── nikto.py
    ├── gobuster.py
    ├── dirb.py
    ├── netcat.py
    └── tcpdump.py
```

---

## ⚙️ Prérequis

- **Kali Linux** (ou toute distribution Debian-based)
- **Python 3.x**
- **Dépendance Python :**
```bash
pip install colorama
```

- **Outils système requis :**

| Outil | Installation |
|---|---|
| nmap | `sudo apt install nmap` |
| sqlmap | `sudo apt install sqlmap` |
| commix | `sudo apt install commix` |
| wifite | `sudo apt install wifite` |
| setoolkit | `sudo apt install set` |
| aircrack-ng | `sudo apt install aircrack-ng` |
| john | `sudo apt install john` |
| hashcat | `sudo apt install hashcat` |
| hydra | `sudo apt install hydra` |
| nikto | `sudo apt install nikto` |
| gobuster | `sudo apt install gobuster` |
| dirb | `sudo apt install dirb` |
| netcat | `sudo apt install netcat-traditional` |
| tcpdump | `sudo apt install tcpdump` |

---

## 🚀 Installation & Lancement

```bash
git clone https://github.com/Charl-23/Little-Kali-ToolKit.git
cd Little-Kali-ToolKit
pip install colorama
python3 multitool.py
```

> Certains outils nécessitent les droits root :
> ```bash
> sudo python3 multitool.py
> ```

---

## 🧰 Outils intégrés

---

### 🔍 RÉSEAU & SCAN

---

#### [1] Nmap — Network Scanner & Port Discovery

**Nmap** est l'outil de référence pour la reconnaissance réseau. Il permet de scanner des machines pour découvrir les ports ouverts, les services qui tournent derrière, le système d'exploitation de la cible, et détecter des vulnérabilités connues.

**Cas d'usage concrets :**
- Scanner un réseau local pour lister toutes les machines connectées
- Identifier les ports ouverts d'un serveur avant un pentest
- Détecter la version d'Apache, SSH, FTP tournant sur une cible
- Vérifier si un firewall filtre certains ports
- Lancer des scripts NSE pour détecter des CVEs automatiquement

**Ce que le script automatise :** choix guidé sur 9 étapes — cible, type de scan, ports, OS detection, timing T0→T5, scripts NSE, évasion firewall/IDS, output.

---

#### [13] Netcat — Network Swiss Army Knife

**Netcat** est le couteau suisse du réseau. Il permet d'ouvrir des connexions TCP/UDP brutes, d'écouter sur un port, de transférer des fichiers, de scanner des ports et d'établir des shells distants.

**Cas d'usage concrets :**
- Ouvrir un listener pour recevoir un reverse shell d'une cible compromise
- Envoyer un fichier d'une machine à une autre sans FTP
- Scanner rapidement si un port est ouvert sur une cible
- Établir un bind shell ou un reverse shell lors d'un pentest
- Tester la connectivité entre deux machines

**Ce que le script automatise :** 6 modes distincts — connexion sortante, écoute, scan de ports, reverse shell, bind shell, transfert de fichier.

---

#### [14] Tcpdump — Network Packet Analyzer

**Tcpdump** est un analyseur de paquets réseau en ligne de commande. Il capture et affiche le trafic réseau en temps réel, permettant d'analyser les communications, détecter des anomalies et intercepter des données.

**Cas d'usage concrets :**
- Capturer le trafic HTTP d'un réseau pour analyser des requêtes
- Intercepter des credentials transitant en clair (HTTP, FTP, Telnet)
- Analyser un fichier `.pcap` capturé avec Wireshark ou airodump-ng
- Filtrer le trafic par IP, port, protocole pour diagnostiquer un réseau
- Enregistrer une capture longue durée avec rotation automatique

**Ce que le script automatise :** mode capture live ou lecture pcap, interface réseau, filtre BPF guidé (protocole, IP, port), snaplen, timestamp, output fichier.

---

### 💉 INJECTION & WEB

---

#### [2] SQLMap — SQL Injection Automation

**SQLMap** est un outil d'exploitation automatique des injections SQL. Il détecte et exploite les failles SQL dans les paramètres d'une URL pour extraire des données d'une base de données.

**Cas d'usage concrets :**
- Tester si un paramètre GET/POST d'un site est vulnérable à l'injection SQL
- Extraire la liste des bases de données, tables et colonnes
- Récupérer les identifiants et mots de passe stockés en base
- Valider la sécurité d'une application web lors d'un audit

**Ce que le script automatise :** Level 1 scan simple, Level 2/3 ajoute automatiquement `--banner`, `--dbs`, `--tables`, `--columns`, `--dump`.

---

#### [3] Commix — Command Injection Automation

**Commix** (Command Injection Exploiter) détecte et exploite les failles d'injection de commandes OS dans les applications web. Là où SQLMap cible les bases de données, Commix cible le système d'exploitation du serveur.

**Cas d'usage concrets :**
- Tester si un champ de formulaire web exécute des commandes sur le serveur
- Obtenir une exécution de commandes distante (RCE) sur un serveur vulnérable
- Identifier des failles d'injection dans des paramètres d'URL ou de cookies
- Audit de sécurité d'applications web exposant des appels système

**Ce que le script automatise :** URL cible, niveau d'injection (1→3), niveau d'énumération (basique / étendu / complet).

---

#### [10] Nikto — Web Server Vulnerability Scanner

**Nikto** est un scanner de vulnérabilités web. Il teste les serveurs HTTP/HTTPS à la recherche de mauvaises configurations, fichiers sensibles exposés, injections XSS/SQL, et des milliers de vulnérabilités connues.

**Cas d'usage concrets :**
- Scanner un serveur web pour trouver des pages d'administration exposées
- Détecter des fichiers de configuration accessibles (`.env`, `config.php`...)
- Identifier des versions de logiciels obsolètes avec CVEs connues
- Tester la résistance d'un site aux injections XSS et SQL basiques
- Audit complet d'un serveur web avant livraison en production

**Ce que le script automatise :** cible + auth, tuning par catégorie (15 types), évasion WAF/IDS (10 techniques), mutation, output multi-format, timeout.

---

#### [11] Gobuster — Directory & DNS Enumeration

**Gobuster** est un outil de brute-force de répertoires, fichiers et sous-domaines. Il teste rapidement des milliers de chemins sur un serveur web ou des entrées DNS pour découvrir du contenu caché.

**Cas d'usage concrets :**
- Trouver des répertoires cachés (`/admin`, `/backup`, `/api`...) sur un serveur web
- Découvrir des sous-domaines non référencés d'un domaine cible
- Enumérer des buckets AWS S3 ou Google Cloud Storage mal configurés
- Fuzzer des paramètres d'URL pour trouver des endpoints cachés
- Cartographier la surface d'attaque d'une application web

**Ce que le script automatise :** 7 modes (dir, vhost, dns, fuzz, s3, gcs, tftp), wordlist, extensions, codes HTTP, headers, proxy, threads.

---

#### [12] Dirb — Web Content Scanner

**Dirb** est un scanner de contenu web par dictionnaire. Il parcourt récursivement un site web en testant des chemins depuis une wordlist pour découvrir des ressources cachées ou non référencées.

**Cas d'usage concrets :**
- Découvrir des répertoires et fichiers cachés sur un serveur Apache/Nginx
- Trouver des backups exposés (`.bak`, `.old`, `.zip`)
- Tester des extensions spécifiques sur toutes les pages (`/page.php`, `/page.html`)
- Scanner récursivement un site pour une cartographie complète
- Audit de configuration d'un serveur web

**Ce que le script automatise :** URL, wordlists multiples, extensions, authentification HTTP, cookies, headers, proxy, récursion, output.

---

### 🔑 MOT DE PASSE & CRACK

---

#### [7] John — Password Hash Cracker

**John the Ripper** est un outil de cracking de mots de passe. Il supporte des centaines de formats de hash et propose plusieurs modes d'attaque pour retrouver les mots de passe en clair depuis leurs hashes.

**Cas d'usage concrets :**
- Cracker des hashes `/etc/shadow` récupérés sur un système Linux compromis
- Retrouver le mot de passe d'une clé SSH protégée (`ssh2john id_rsa > hash.txt`)
- Cracker des archives ZIP, PDF, KeePass ou fichiers Office protégés
- Tester la robustesse des mots de passe d'une organisation (audit)
- Reprendre une session de cracking interrompue

**Ce que le script automatise :** fichier de hashes, format (14 types + auto), mode (wordlist/single/incremental/mask/prince/loopback), règles, filtres, sessions.

---

#### [8] Hashcat — GPU Hash Cracker

**Hashcat** est le cracker de hashes le plus rapide au monde, utilisant la puissance du GPU pour des vitesses de cracking bien supérieures à John. Il supporte plus de 300 types de hash.

**Cas d'usage concrets :**
- Cracker des hashes NTLM Windows récupérés via Mimikatz ou responder
- Attaquer des hashes WPA/WPA2 capturés avec airodump-ng
- Cracker des hashes bcrypt, sha512crypt avec des règles avancées
- Tester la robustesse des mots de passe d'une base de données compromise
- Utiliser des masques intelligents pour cibler des formats de mots de passe spécifiques

**Ce que le script automatise :** type de hash (23 courants), mode d'attaque (straight/combination/bruteforce/hybrid), wordlist, règles, masque, profil GPU, session.

---

#### [9] Hydra — Login Brute-Force Tool

**Hydra** est un outil de brute-force de logins. Il teste automatiquement des milliers de combinaisons d'identifiants/mots de passe sur de nombreux services réseau pour trouver des accès valides.

**Cas d'usage concrets :**
- Tester la résistance des mots de passe SSH d'un serveur
- Brute-forcer le formulaire de login d'une application web
- Tester des identifiants par défaut sur des services FTP, RDP, MySQL, SMB
- Valider qu'un service VNC ou Telnet n'utilise pas de mots de passe faibles
- Attaquer plusieurs cibles simultanément lors d'un test d'intrusion réseau

**Ce que le script automatise :** cible unique ou liste, 24 services supportés, login/wordlist/bruteforce, threads, délai anti-ban, output, session.

---

### 📶 WIFI

---

#### [4] Wifite — Wifi Attack Automation

**Wifite** est un outil d'attaque automatisée sur les réseaux WiFi. Il capture les handshakes WPA/WPA2, casse les clés WEP, et tente de déchiffrer les mots de passe via une wordlist en gérant automatiquement le mode monitor.

**Cas d'usage concrets :**
- Tester la robustesse du mot de passe de son propre réseau WiFi
- Capturer un handshake WPA2 pour un crackage hors-ligne
- Auditer la sécurité d'un réseau WiFi lors d'un test d'intrusion autorisé
- Identifier les réseaux vulnérables à WEP dans un environnement de test

**Ce que le script automatise :** chemin de wordlist, option `--kill`, vérification du fichier avant lancement.

> ⚠️ Requiert les droits root et une carte WiFi compatible mode monitor.

---

#### [6] Aircrack-ng — WiFi Password Cracking

**Aircrack-ng** est la suite de référence pour l'audit WiFi. Il permet de cracker les clés WEP par analyse statistique des IVs et les clés WPA/WPA2 par attaque dictionnaire sur un handshake capturé.

**Cas d'usage concrets :**
- Cracker une clé WEP depuis un fichier de capture `.ivs` ou `.cap`
- Tester un handshake WPA2 capturé contre une wordlist comme rockyou.txt
- Utiliser une base PMK précalculée avec airolib-ng pour accélérer le cracking WPA
- Exporter vers Hashcat (HCCAPX) pour utiliser le GPU
- Filtrer le cracking par ESSID ou BSSID pour cibler un réseau précis

**Ce que le script automatise :** mode WEP ou WPA-PSK, fichier de capture, ESSID/BSSID, longueur clé WEP, wordlist, base airolib, export Hashcat.

---

### 🎭 SOCIAL ENGINEERING

---

#### [5] SEToolkit — Social Engineering Toolkit

**SEToolkit** (Social Engineer Toolkit) est un framework dédié aux attaques d'ingénierie sociale. Il permet de créer des campagnes de phishing, des faux sites web clonés et des payloads ciblant l'humain plutôt que la machine.

**Cas d'usage concrets :**
- Cloner un site web (ex: page de login) pour capturer des identifiants
- Créer une campagne de spear phishing lors d'un pentest Red Team
- Générer un payload pour tester la sensibilisation des utilisateurs
- Simuler une attaque d'ingénierie sociale dans un cadre professionnel autorisé

**Ce que le script automatise :** vérification des droits root, confirmation avant lancement, lancement direct de SEToolkit.

---

## ⚠️ Avertissement légal / Legal Disclaimer

> 🇫🇷 Ce projet est destiné **uniquement à des fins éducatives** et à des tests sur des systèmes vous appartenant ou pour lesquels vous avez une **autorisation explicite écrite**.  
> L'utilisation de ces outils sur des systèmes tiers sans autorisation est **illégale** et peut entraîner des poursuites judiciaires. L'auteur décline toute responsabilité pour toute utilisation abusive.

> 🇬🇧 This project is intended **for educational purposes only** and for testing on systems you own or have **explicit written permission** to test.  
> Using these tools on third-party systems without authorization is **illegal**. The author takes no responsibility for any misuse.

---

## 👤 Auteur / Author

**C404C**  
🔗 GitHub : [@Charl-23](https://github.com/Charl-23)

---

<div align="center">
  <sub>Made with ❤️ on Kali Linux</sub>
</div>
