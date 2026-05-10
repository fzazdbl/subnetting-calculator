# subnetting-calculator

> Calculateur de sous-réseaux IPv4 CLI avec représentation binaire et découpage — pur Python stdlib

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

## Fonctionnalités

- **Analyse complète d'un CIDR** : réseau, broadcast, masque, wildcard, hôtes, classe, type (privé/public)
- **Représentation binaire** des adresses (réseau, masque, broadcast)
- **Découpage en N sous-réseaux** (`--split N`) avec liste complète des plages
- **Vérification d'appartenance** (`--check IP`) d'une adresse dans un réseau
- Couleurs ANSI, zéro dépendance externe

## Installation

```bash
git clone https://github.com/fzazdbl/subnetting-calculator.git
cd subnetting-calculator
python subnetting.py --help
```

## Utilisation

```bash
# Analyser un réseau
python subnetting.py 192.168.1.0/24

# Découper en 4 sous-réseaux
python subnetting.py 10.0.0.0/16 --split 4

# Vérifier si une IP appartient au réseau
python subnetting.py 172.16.0.0/12 --check 172.20.5.10

# Combiner découpage et vérification
python subnetting.py 192.168.0.0/24 --split 8 --check 192.168.0.130
```

## Exemple de sortie

```
  Réseau               : 192.168.1.0
  Masque               : 255.255.255.0
  CIDR                 : /24
  Wildcard             : 0.0.0.255
  Broadcast            : 192.168.1.255
  Premier hôte         : 192.168.1.1
  Dernier hôte         : 192.168.1.254
  Nombre d'hôtes       : 254
  Total adresses       : 256
  Classe               : C
  Type                 : Privé  🔒

  ─── Binaire ───
  Réseau    : 11000000.10101000.00000001.00000000
  Masque    : 11111111.11111111.11111111.00000000
  Broadcast : 11000000.10101000.00000001.11111111
```

## Options

| Option | Alias | Description |
|--------|-------|-------------|
| `cidr` | — | Réseau en notation CIDR (ex: 192.168.1.0/24) |
| `--split N` | `-s` | Découper en N sous-réseaux |
| `--check IP` | `-c` | Vérifier si une IP appartient au réseau |
| `--no-banner` | — | Désactiver la bannière ASCII |

## Auteur

**Mohamed Chahid Echattioui** — [@fzazdbl](https://github.com/fzazdbl)

## Licence

MIT
