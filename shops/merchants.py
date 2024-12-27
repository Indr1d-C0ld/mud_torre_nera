import sqlite3
from config import DATABASE_FILE
from items.misc_items import MISC_ITEMS
from items.weapons import WEAPONS

ALL_ITEMS = {}
ALL_ITEMS.update(MISC_ITEMS)
ALL_ITEMS.update(WEAPONS)

async def handle_shop_command(player, action, item):
    # Per semplicità, supponiamo un solo mercante nella regione
    merchant = get_merchant_in_region(player.region)
    if not merchant:
        return "Non ci sono mercanti qui."
    if action == "buy":
        price = get_item_price(merchant["id"], item)
        if price is None:
            return "Questo mercante non vende quell'oggetto."
        if player.money < price:
            return "Non hai abbastanza denaro."
        player.money -= price
        player.inventory.append(item)
        return f"Hai acquistato {item} per {price} monete."
    elif action == "sell":
        if item not in player.inventory:
            return "Non possiedi questo oggetto."
        price = get_item_price(merchant["id"], item)
        if price is None:
            # se l'oggetto non è nel listino, vendi a metà
            price = 10
        player.inventory.remove(item)
        player.money += price // 2
        return f"Hai venduto {item} per {price//2} monete."
    else:
        return "Azione negozio non valida (usa buy o sell)."

def get_merchant_in_region(region):
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, name, region FROM merchants WHERE region=?", (region,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "name": row[1], "region": row[2]}
    return None

def get_item_price(merchant_id, item_name):
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute("SELECT price FROM merchant_items WHERE merchant_id=? AND item_name=?", (merchant_id,item_name))
    row = cur.fetchone()
    conn.close()
    if row:
        return row[0]
    return None

