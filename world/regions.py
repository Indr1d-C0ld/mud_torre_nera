import sqlite3
from config import DATABASE_FILE

region_descriptions = {
    "Deserto del Mohaine": "Un deserto sconfinato, sabbia ovunque, il sole brucia e lontano si vede un uomo in nero.",
    "Foresta Nera": "Una foresta oscura e minacciosa, le fronde degli alberi sembrano sussurrare antiche maledizioni.",
    "Città di Lud": "Le rovine di una grande città, un tempo prospera, ora popolata da bande violente e meccanismi arrugginiti.",
    "Calla Bryn Sturgis": "Un villaggio pacifico, circondato da campi e gente ospitale. Ma i Lupi di Thunderclap non sono lontani.",
    "End-World": "La fine del mondo conosciuto, terre desolate e creature innominabili, oltre c’è la Torre Nera."
}

def get_region_description(region, x, y):
    # Descrizione della regione + tile
    base_desc = region_descriptions.get(region, "Un luogo sconosciuto.")
    # Potremmo aggiungere ulteriori dettagli da DB, NPC vicini, ecc.
    return base_desc

