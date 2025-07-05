def setup_automation(hass, config):
    pompe = config["pompe_switch"]
    temp_eau = config["temperature_eau"]
    temp_ext = config["temperature_ext"]
    meteo = config["condition_meteo"]
    temps_cycle = config["temps_cycle"]
    telegram_user = config["telegram_user_id"]
    saison = config["saison"]

    def should_run():
        # Ici, ajouter la logique pour déterminer s'il faut démarrer la pompe
        return True

    def start_cycle(now):
        if should_run():
            hass.services.call("switch", "turn_on", {"entity_id": pompe})
            hass.services.call("notify", "telegram", {
                "message": f"Cycle de filtration démarré pour {temps_cycle} minutes.",
                "target": telegram_user
            })

    from homeassistant.helpers.event import async_track_time_change
    async_track_time_change(hass, start_cycle, hour=9, minute=0, second=0)