DOMAIN = "pompe_piscine"
CONF_POMPE_SWITCH = "pompe_switch"
CONF_SENSOR_TEMP = "sensor_temp"
CONF_SENSOR_TEMP_EXT = "sensor_temp_ext"
CONF_SENSOR_SAISON = "sensor_saison"
CONF_WEATHER = "weather_entity"
CONF_MODE_SELECT = "mode_select"
CONF_TELEGRAM_ID = "telegram_user"

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

INPUT_DATETIME = ["heure_matin", "heure_apresmidi"]
INPUT_BOOLEAN = ["cycle_en_cours"]
INPUT_NUMBER = [
    "anti_calcaire_preventif",
    "anti_calcaire_curatif",
    "anti_algues_preventif",
    "anti_algues_curatif",
    "chlore_choc",
    "oxygene_actif",
    "floculant",
    "ph",
    "algicide_ld",
    "multi_actions",
    "brome",
    "electrolyse_sel",
    "filtration_min_hiver",
    "contenance_piscine",
    "debit_pompe",
]

INPUT_NUMBER_DEFAULTS = {
    "anti_calcaire_preventif": 11,
    "anti_calcaire_curatif": 18,
    "anti_algues_preventif": 5,
    "anti_algues_curatif": 10,
    "chlore_choc": 10,
    "oxygene_actif": 9,
    "floculant": 3,
    "ph": 3,
    "algicide_ld": 7,
    "multi_actions": 9,
    "brome": 18,
    "electrolyse_sel": 18,
    "filtration_min_hiver": 30,
    "contenance_piscine": 5,
    "debit_pompe": 5,
}