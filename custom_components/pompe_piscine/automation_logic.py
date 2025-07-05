def setup_automation(hass, config):
    pompe = config["pompe_switch"]
    temp_eau_sensor = config["input_temperature_piscine"]
    temp_ext_sensor = config["input_temperature_exterieure"]
    meteo_entity = config["input_weather_entity"]
    mode_entity = config["input_select_mode"]
    saison_sensor = config["input_saison_sensor"]
    hiver_mode = config["input_winter_mode"]
    seuil_temp = config["input_seuil_temperature"]
    duree_min_hiver = config["input_filtration_minimale_hiver"]
    heure_cycle_matin = config["input_heure_cycle_matin"]
    heure_cycle_apresmidi = config["input_heure_cycle_apresmidi"]
    telegram_user = config["telegram_user"]

    # Réglages spécifiques pour modes spéciaux (extrait du blueprint)
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

    from homeassistant.helpers.event import async_track_time_change
    from datetime import datetime, time

    async def should_run():
        temp_eau = float(hass.states.get(temp_eau_sensor).state or 0)
        temp_ext = float(hass.states.get(temp_ext_sensor).state or 0)
        mode = hass.states.get(mode_entity).state
        saison = hass.states.get(saison_sensor).state
        meteo = hass.states.get(meteo_entity).state if hass.states.get(meteo_entity) else None
        hiver = hass.states.get(hiver_mode).state == "on"

        # Ne pas filtrer si pluie détectée
        if meteo and "rain" in meteo.lower():
            return False

        # Mode hiver => filtration minimale
        if hiver:
            return True

        # Sinon filtrer si température eau > seuil
        if temp_eau >= seuil_temp:
            return True

        return False

    async def calc_duree_cycle():
        mode = hass.states.get(mode_entity).state
        temp_eau = float(hass.states.get(temp_eau_sensor).state or 0)
        temp_ext = float(hass.states.get(temp_ext_sensor).state or 0)
        hiver = hass.states.get(hiver_mode).state == "on"

        if hiver:
            # Durée minimale hiver en minutes
            return duree_min_hiver * 60

        if mode == "Filtration normale" or mode == "Chlore lent":
            # Durée = température / 2 (heures)
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
            "message": f"Cycle de filtration démarré en mode '{hass.states.get(mode_entity).state}' pour {round(duree / 60)} minutes.",
            "target": telegram_user
        })

        # Programme l’arrêt après la durée
        async def stop_cycle(_):
            await hass.services.async_call("switch", "turn_off", {"entity_id": pompe})
            await hass.services.async_call("notify", "telegram", {
                "message": f"Cycle de filtration terminé.",
                "target": telegram_user
            })

        hass.helpers.event.async_call_later(duree, stop_cycle)

    # Planifie les cycles matin et après-midi
    h_matin = datetime.strptime(heure_cycle_matin, "%H:%M:%S").time()
    h_apresmidi = datetime.strptime(heure_cycle_apresmidi, "%H:%M:%S").time()

    async_track_time_change(hass, start_cycle, hour=h_matin.hour, minute=h_matin.minute, second=h_matin.second)
    async_track_time_change(hass, start_cycle, hour=h_apresmidi.hour, minute=h_apresmidi.minute, second=h_apresmidi.second)