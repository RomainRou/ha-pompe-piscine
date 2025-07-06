from homeassistant.components import input_boolean, input_datetime, input_number, input_select
from homeassistant.helpers import entity_registry as er

async def async_create_helpers(hass):
    registry = er.async_get(hass)
    # modes
    modes = [
        "Filtration normale", "Anti‑algues préventif", "Anti‑algues curatif",
        "Chlore lent", "Chlore choc", "Oxygène actif", "Floculant",
        "pH+ ou pH-", "Algicide longue durée", "Traitement multi‑actions",
        "Brome", "Électrolyse au sel", "Anti‑calcaire préventif", "Anti‑calcaire curatif"
    ]
    await input_select.async_create_input_select(
        hass, "piscine_intelligente", "mode_filtration", "Mode de filtration", modes
    )
    # cycle en cours
    await input_boolean.async_create_input_boolean(
        hass, "piscine_intelligente", "cycle_en_cours", "Cycle en cours"
    )
    await input_datetime.async_create_input_datetime(
        hass, "piscine_intelligente", "cycle_debut", "Début du cycle"
    )
    await input_number.async_create_input_number(
        hass, "piscine_intelligente", "duree_cycle", "Durée du cycle (sec)", 0, 86400, 1
    )
    # sliders réglages
    regs = {
        "anti_calcaire_preventif": (8, 14, 11),
        "anti_calcaire_curatif": (12, 24, 18),
        "anti_algues_preventif": (4, 6, 5),
        "anti_algues_curatif": (8, 12, 10),
        "chlore_choc": (8, 12, 10),
        "oxygene_actif": (6, 12, 9),
        "floculant": (2, 4, 3),
        "ph": (2, 4, 3),
        "algicide_ld": (6, 8, 7),
        "multi_actions": (6, 10, 9),
        "brome": (12, 24, 18),
        "electrolyse_sel": (12, 24, 18)
    }
    for key, (minv, maxv, default) in regs.items():
        await input_number.async_create_input_number(
            hass, "piscine_intelligente",
            f"reglage_{key}", key.replace("_", " ").title(),
            minv, maxv, 1, default
        )