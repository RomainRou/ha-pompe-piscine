from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_registry import async_get

# Liste des entités nécessaires au bon fonctionnement de l'intégration
REQUIRED_ENTITIES = [
    "input_select.mode_filtration",
    "input_boolean.cycle_en_cours",
    "input_datetime.cycle_debut",
    "input_number.duree_cycle",
    "input_number.reglage_anti_calcaire_preventif",
    "input_number.reglage_anti_calcaire_curatif",
    "input_number.reglage_anti_algues_preventif",
    "input_number.reglage_anti_algues_curatif",
    "input_number.reglage_chlore_choc",
    "input_number.reglage_oxygene_actif",
    "input_number.reglage_floculant",
    "input_number.reglage_ph",
    "input_number.reglage_algicide_ld",
    "input_number.reglage_multi_actions",
    "input_number.reglage_brome",
    "input_number.reglage_electrolyse_sel"
]

async def async_validate_helpers(hass: HomeAssistant) -> bool:
    """Vérifie que toutes les entités nécessaires sont bien présentes dans le registre d'entités."""
    entity_registry = async_get(hass)
    missing = []

    for entity_id in REQUIRED_ENTITIES:
        if entity_registry.async_get(entity_id) is None:
            missing.append(entity_id)

    if missing:
        _log_missing_entities(hass, missing)
        return False

    return True

def _log_missing_entities(hass: HomeAssistant, missing: list[str]):
    """Log des entités manquantes avec un avertissement clair."""
    hass.components.logger.warning(
        f"[Piscine Intelligente] Les entités suivantes sont manquantes : {', '.join(missing)}. "
        f"Veuillez les créer manuellement dans configuration.yaml ou via l’interface utilisateur."
    )