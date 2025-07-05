from .const import (
    CONF_POMPE,
    CONF_TEMP_EAU,
    CONF_TEMP_EXT,
    CONF_METEO,
    CONF_SAISON,
    CONF_TEMPS_CYCLE,
    CONF_TELEGRAM_USER,
)

from homeassistant.helpers.event import async_track_time_change
from datetime import datetime

def setup_automation(hass, config):
    pompe = config[CONF_POMPE]
    temp_eau_sensor = config[CONF_TEMP_EAU]
    temp_ext_sensor = config[CONF_TEMP_EXT]
    meteo_entity = config[CONF_METEO]
    saison_sensor = config[CONF_SAISON]
    temps_cycle = config[CONF_TEMPS_CYCLE]
    telegram_user = config[CONF_TELEGRAM_USER]

    # Ces clés doivent être ajoutées au const.py et au config flow si elles sont utilisées
    mode_entity = config.get("input_select_mode")
    hiver_mode = config.get("input_winter_mode")
    seuil_temp = config.get("input_seuil_temperature")
    duree_min_hiver = config.get("input_filtration_minimale_hiver")
    heure_cycle_matin = config.get("input_heure_cycle_matin")
    heure_cycle_apresmidi = config.get("input_heure_cycle_apresmidi")

    # Réglages spécifiques pour modes spéciaux (valeurs par défaut)
    reglage_anti_calcaire_preventif = config.get("reglage_anti_calcaire_preventif", 11)
    reglage_anti_calcaire_curatif = config.get("reglage_anti_calcaire_curatif", 18)
    reglage_anti_algues_preventif = config.get("reglage_anti_algues_preventif", 5)
    reglage_anti_algues_curatif = config.get("reglage_anti_algues_curatif", 10)
    reglage_chlore_choc = config.get("reglage_chlore_choc", 10)
    reglage_oxygene_actif = config.get("reglage_oxygene_actif", 9)
    reglage_floculant = config.get("reglage_floculant", 3)
    reglage_ph = config.get("reglage_ph", 3)
    reglage_algicide_ld = config.get("reglage_algicide_ld", 7)
    reglage_multi_actions = config.get("reglage_multi_actions", 9)
    reglage_brome = config.get("reglage_brome", 18)
    reglage_sel = config.get("reglage_sel", 18)

    async def should_run():
        temp_eau = float(hass.states.get(temp_eau_sensor).state or 0)
        temp_ext = float(hass.states.get(temp_ext_sensor).state or 0)
        mode = hass.states.get(mode_entity).state if mode_entity else None
        saison = hass.states.get(saison_sensor).state if saison_sensor else None
        meteo = hass.states.get(meteo_entity).state if hass.states.get(meteo_entity) else None
        hiver = hass.states.get(hiver_mode).state == "on" if hiver_mode and hass.states.get(hiver_mode) else False

        # Ne pas filtrer si pluie détectée
        if meteo and "rain" in meteo.lower():
            return False

        # Mode hiver => filtration minimale
        if hiver:
            return True

        # Sinon filtrer si température eau > seuil
        if seuil_temp is not None and temp_eau >= float(seuil_temp):
            return True

        return False

    async def calc_duree_cycle():
        mode = hass.states.get(mode_entity).state if mode_entity else None
        temp_eau = float(hass.states.get(temp_eau_sensor).state or 0)
        hiver = hass.states.get(hiver_mode).state == "on" if hiver_mode and hass.states.get(hiver_mode) else False

        if hiver and duree_min_hiver:
            # Durée minimale hiver en minutes
            return int(duree_min_hiver) * 60

        if mode == "Filtration normale" or mode == "Chlore lent":
            duree = (temp_eau / 2) * 3600
        elif mode == "Anti-calcaire préventif":
            duree = reglage_anti_calcaire_preventif * 3600
        elif mode == "Anti-calcaire curatif":
            duree = reglage_anti_calcaire_curatif * 3600
        elif mode == "Anti-algues préventif":
            duree = reglage_anti_algues_preventif * 3600
        elif mode == "Anti-algues curatif":
            duree = reglage_anti_algues_curatif * 3600
        elif mode == "Chlore choc":
            duree = reglage_chlore_choc * 3600
        elif mode == "Oxygène actif":
            duree = reglage_oxygene_actif * 3600
        elif mode == "Floculant":
            duree = reglage_floculant * 3600
        elif mode == "pH+ ou pH-":
            duree = reglage_ph * 3600
        elif mode == "Algicide longue durée":
            duree = reglage_algicide_ld * 3600
        elif mode == "Traitement multi-actions":
            duree = reglage_multi_actions * 3600
        elif mode == "Brome":
            duree = reglage_brome * 3600
        elif mode == "Électrolyse au sel":
            duree = reglage_sel * 3600
        else:
            duree = 0

        return duree

    async def start_cycle(now):
        if not await should_run():
            return

        duree = await calc_duree_cycle()
        if duree <= 0:
            return

        # Démarre la pompe
        await hass.services.async_call("switch", "turn_on", {"entity_id": pompe})
        # Envoi notification telegram
        await hass.services.async_call("notify", "telegram", {
            "message": f"Cycle de filtration démarré en mode '{hass.states.get(mode_entity).state if mode_entity else 'inconnu'}' pour {round(duree / 60)} minutes.",
            "target": telegram_user
        })

        # Programme l’arrêt après la durée
        async def stop_cycle(_):
            await hass.services.async_call("switch", "turn_off", {"entity_id": pompe})
            await hass.services.async_call("notify", "telegram", {
                "message": "Cycle de filtration terminé.",
                "target": telegram_user
            })

        hass.helpers.event.async_call_later(duree, stop_cycle)

    if heure_cycle_matin and heure_cycle_apresmidi:
        try:
            h_matin = datetime.strptime(heure_cycle_matin, "%H:%M:%S").time()
            h_apresmidi = datetime.strptime(heure_cycle_apresmidi, "%H:%M:%S").time()

            async_track_time_change(hass, start_cycle, hour=h_matin.hour, minute=h_matin.minute, second=h_matin.second)
            async_track_time_change(hass, start_cycle, hour=h_apresmidi.hour, minute=h_apresmidi.minute, second=h_apresmidi.second)
        except Exception as e:
            hass.logger.error(f"Erreur lors de la planification des cycles : {e}")
    else:
        hass.logger.warning("Heures de cycle matin ou après-midi non configurées.")