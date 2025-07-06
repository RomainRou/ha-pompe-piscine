DOMAIN = "piscine_intelligente"
CONF_POMPE_SWITCH = "pompe_switch"
CONF_SENSOR_TEMP = "sensor_temp"
CONF_SENSOR_TEMP_EXT = "sensor_temp_ext"
CONF_SENSOR_SAISON = "sensor_saison"
CONF_WEATHER = "weather_entity"
CONF_MODE_SELECT = "mode_select"
CONF_TELEGRAM_ID = "telegram_user"

PLATFORMS = ["switch", "sensor"]
MODE_OPTIONS = [
    "Filtration normale",
    "Anti-algues préventif",
    "Anti-algues curatif",
    "Chlore lent",
    "Chlore choc",
    "Oxygène actif",
    "Floculant",
    "pH+ ou pH-",
    "Algicide longue durée",
    "Traitement multi-actions",
    "Brome",
    "Électrolyse au sel",
    "Anti-calcaire préventif",
    "Anti-calcaire curatif",
]