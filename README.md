# Pompe Piscine Intelligente

Automatisation intelligente de la pompe de piscine basée sur :

- Température de l’eau
- Conditions météo
- Mode manuel (chlore choc, anti-algues, etc.)

## Installation

1. Ajouter ce dépôt dans HACS > Intégrations > Dépôts personnalisés
2. Redémarrer Home Assistant
3. Utiliser les services `pompe_piscine.set_mode`

## Exemple

```yaml
service: pompe_piscine.set_mode
data:
  mode: "Chlore choc"
  duree: 10
```

## Modes supportés

- Filtration normale
- Chlore choc
- Anti-algues préventif
- Electrolyse au sel
... et bien d'autres.
