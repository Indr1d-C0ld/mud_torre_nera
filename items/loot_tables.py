import random
from items.weapons import WEAPONS
from items.misc_items import MISC_ITEMS

LOOT_TABLE = {
    "Mutante del Deserto": ["Pistola Scadente", "Pozione piccola"],
    "Ratto Parlatore": ["Pozione piccola"],
    "Taheen corrotto": ["Fucile a canne mozze", "Pozione piccola"]
}

def get_loot(monster_name):
    if monster_name in LOOT_TABLE:
        return random.choice(LOOT_TABLE[monster_name])
    return None

