#!/usr/bin/env python3
"""
subnetting.py — Calculateur de sous-réseaux IPv4 CLI
Auteur : Mohamed Chahid Echattioui (@fzazdbl)
"""

import argparse
import ipaddress
import sys

# ── ANSI ──────────────────────────────────────────────────────────────────────
R = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
YEL = "\033[93m"
GRN = "\033[92m"
CYN = "\033[96m"
MAG = "\033[95m"
BLU = "\033[94m"
DIM = "\033[2m"


def c(text, code):
    return f"{code}{text}{R}"


def label(text):
    return c(f"  {text:<22}", BLU + BOLD)


# ── Utilitaires ───────────────────────────────────────────────────────────────
def ip_class(ip: ipaddress.IPv4Address) -> str:
    first = int(str(ip).split(".")[0])
    if first < 128:
        return "A"
    elif first < 192:
        return "B"
    elif first < 224:
        return "C"
    elif first < 240:
        return "D (multicast)"
    return "E (réservé)"


def is_private(network: ipaddress.IPv4Network) -> bool:
    return network.network_address.is_private


def to_binary(ip: ipaddress.IPv4Address) -> str:
    parts = str(ip).split(".")
    bins = [f"{int(p):08b}" for p in parts]
    return ".".join(bins)


def banner():
    print(f"""
{MAG}{BOLD}
  ███████╗██╗   ██╗██████╗ ███╗   ██╗███████╗████████╗
  ██╔════╝██║   ██║██╔══██╗████╗  ██║██╔════╝╚══██╔══╝
  ███████╗██║   ██║██████╔╝██╔██╗ ██║█████╗     ██║
  ╚════██║██║   ██║██╔══██╗██║╚██╗██║██╔══╝     ██║
  ███████║╚██████╔╝██████╔╝██║ ╚████║███████╗   ██║
  ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝   ╚═╝
{R}{CYN}  Calculateur de sous-réseaux IPv4  |  @fzazdbl{R}
""")


# ── Analyse principale ────────────────────────────────────────────────────────
def analyze(cidr: str) -> ipaddress.IPv4Network:
    try:
        net = ipaddress.IPv4Network(cidr, strict=False)
    except ValueError as e:
        print(c(f"  ✗ CIDR invalide : {e}", RED))
        sys.exit(1)
    return net


def print_info(net: ipaddress.IPv4Network) -> None:
    hosts = list(net.hosts())
    num_hosts = net.num_addresses - 2 if net.prefixlen < 31 else net.num_addresses
    first_host = hosts[0] if hosts else net.network_address
    last_host = hosts[-1] if hosts else net.broadcast_address

    private = "Privé  🔒" if is_private(net) else "Public  🌐"
    cls = ip_class(net.network_address)

    rows = [
        ("Réseau",           c(str(net.network_address), GRN + BOLD)),
        ("Masque",           c(str(net.netmask), GRN)),
        ("CIDR",             c(f"/{net.prefixlen}", GRN)),
        ("Wildcard",         c(str(net.hostmask), YEL)),
        ("Broadcast",        c(str(net.broadcast_address), RED)),
        ("Premier hôte",     c(str(first_host), CYN)),
        ("Dernier hôte",     c(str(last_host), CYN)),
        ("Nombre d'hôtes",   c(f"{num_hosts:,}", BOLD)),
        ("Total adresses",   c(f"{net.num_addresses:,}", DIM)),
        ("Classe",           c(cls, MAG)),
        ("Type",             c(private, MAG)),
    ]

    print(c(f"\n  ┌─ Réseau : {net} ───────────────────────────────", DIM))
    for name, val in rows:
        print(f"{label(name)}: {val}")

    # Représentation binaire
    print(c("\n  ─── Binaire ────────────────────────────────────", DIM))
    print(f"{label('Réseau')}: {c(to_binary(net.network_address), DIM)}")
    print(f"{label('Masque')}: {c(to_binary(net.netmask), DIM)}")
    print(f"{label('Broadcast')}: {c(to_binary(net.broadcast_address), DIM)}")
    print()


# ── Split ─────────────────────────────────────────────────────────────────────
def split_network(net: ipaddress.IPv4Network, n: int) -> None:
    # Trouver le préfixe nécessaire pour au moins N sous-réseaux
    import math
    bits_needed = math.ceil(math.log2(n)) if n > 1 else 0
    new_prefix = net.prefixlen + bits_needed

    if new_prefix > 30:
        print(c(f"  ✗ Impossible de découper en {n} sous-réseaux (préfixe /{new_prefix} trop grand)", RED))
        sys.exit(1)

    subnets = list(net.subnets(new_prefix=new_prefix))
    print(c(f"\n  Découpage de {net} en /{new_prefix} ({len(subnets)} sous-réseaux)\n", YEL + BOLD))

    for i, sub in enumerate(subnets, 1):
        hosts = list(sub.hosts())
        first = hosts[0] if hosts else sub.network_address
        last = hosts[-1] if hosts else sub.broadcast_address
        num = sub.num_addresses - 2 if sub.prefixlen < 31 else sub.num_addresses
        print(
            f"  {c(f'[{i:>3}]', DIM)} {c(str(sub), GRN + BOLD):<30}"
            f"  hôtes: {c(str(first), CYN)} → {c(str(last), CYN)}"
            f"  ({c(str(num), BOLD)})"
        )
    print()


# ── Check ──────────────────────────────────────────────────────────────────────
def check_ip(net: ipaddress.IPv4Network, ip_str: str) -> None:
    try:
        ip = ipaddress.IPv4Address(ip_str)
    except ValueError:
        print(c(f"  ✗ IP invalide : {ip_str}", RED))
        sys.exit(1)

    if ip in net:
        role = ""
        if ip == net.network_address:
            role = c(" (adresse réseau)", YEL)
        elif ip == net.broadcast_address:
            role = c(" (broadcast)", YEL)
        print(c(f"\n  ✓ {ip} appartient à {net}{role}\n", GRN + BOLD))
    else:
        print(c(f"\n  ✗ {ip} n'appartient PAS à {net}\n", RED + BOLD))


# ── CLI ───────────────────────────────────────────────────────────────────────
def build_parser():
    p = argparse.ArgumentParser(
        prog="subnetting",
        description="Calculateur de sous-réseaux IPv4 avec représentation binaire",
    )
    p.add_argument("cidr", help="Réseau en notation CIDR (ex: 192.168.1.0/24)")
    p.add_argument("--split", "-s", type=int, metavar="N",
                   help="Découper en N sous-réseaux")
    p.add_argument("--check", "-c", metavar="IP",
                   help="Vérifier si une IP appartient au réseau")
    p.add_argument("--no-banner", action="store_true",
                   help="Ne pas afficher la bannière")
    return p


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.no_banner:
        banner()

    net = analyze(args.cidr)
    print_info(net)

    if args.split:
        split_network(net, args.split)

    if args.check:
        check_ip(net, args.check)


if __name__ == "__main__":
    main()
