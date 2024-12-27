# characters/creation.py

import sqlite3
from config import INITIAL_MONEY, DATABASE_FILE, DEFAULT_STAMINA, DEFAULT_MANA
from characters.classes import CLASSES
from utils.database import save_character, load_character

async def create_new_character(player):
    await player.send("Scegli una classe (gunslinger, taheen, cantore_dossa, ladro_dei_nodi):")
    data = await player.reader.readline()
    chosen_class = data.decode('utf-8').strip().lower()
    if chosen_class not in CLASSES:
        await player.send("Classe non valida, scelgo gunslinger di default.")
        chosen_class = "gunslinger"
    player.class_name = chosen_class
    player.hp = CLASSES[chosen_class]["hp"]
    player.max_hp = CLASSES[chosen_class]["hp"]
    player.money = INITIAL_MONEY
    player.inventory = []
    player.x, player.y = (25,25)
    player.level = 1
    player.exp = 0
    player.achievements = []
    player.quests = []
    player.region = "Deserto del Mohaine"
    player.stamina = DEFAULT_STAMINA
    player.mana = DEFAULT_MANA
    save_character(player)

def load_character_to_player(player, name):
    row = load_character(name)
    if row:
        player.name = row[0]
        player.class_name = row[1]
        player.level = row[2]
        player.exp = row[3]
        player.hp = row[4]
        player.max_hp = row[5]
        player.x = row[6]
        player.y = row[7]
        player.money = row[8]
        player.inventory = row[9].split(",") if row[9] else []
        player.achievements = row[10].split(",") if row[10] else []
        player.quests = row[11].split(",") if row[11] else []
        player.region = row[12]
        player.stamina = row[13]
        player.mana = row[14]

