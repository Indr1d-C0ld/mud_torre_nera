# world/area_generator.py

import random
import sqlite3
from config import MAP_WIDTH, MAP_HEIGHT, DATABASE_FILE

# Esempio: aumentiamo le dimensioni di default
# Puoi portarle, ad esempio, a 80x80 o 100x100
DEFAULT_MAP_WIDTH = 80
DEFAULT_MAP_HEIGHT = 80

# Possibili “terrain tile” più variegati
# . = pianura
# ^ = montagna/rocce
# ~ = acqua
# * = foresta
# d = deserto
# # = ruderi / rovine
TILES = ['.', '.', '.', '^', '^', '~', '*', '*', 'd', '#']

# Suddivisione macroscopica in regioni
REGIONS = [
    "Deserto del Mohaine",
    "Foresta Nera",
    "Città di Lud",
    "Calla Bryn Sturgis",
    "End-World"
]

def ensure_world_generated():
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM world_map")
    count = cur.fetchone()[0]
    if count == 0:
        generate_world(conn, DEFAULT_MAP_WIDTH, DEFAULT_MAP_HEIGHT)
    conn.close()

def generate_world(conn, width, height):
    """
    Genera una mappa di dimensioni (width x height) e la memorizza in world_map.
    """
    cur = conn.cursor()
    # Pulizia eventuale (se si rigenera).
    cur.execute("DELETE FROM world_map")

    for y in range(height):
        for x in range(width):
            tile = random.choice(TILES)

            # Logica semplificata per assegnare regioni in base a x,y
            # (Volendo, potresti fare una suddivisione per "fasce" o generazione più complessa)
            if x < width * 0.25:
                region = "Foresta Nera"
            elif x > width * 0.75:
                region = "Città di Lud"
            elif y < height * 0.25:
                region = "End-World"
            elif y > height * 0.75:
                region = "Calla Bryn Sturgis"
            else:
                region = "Deserto del Mohaine"

            cur.execute("INSERT INTO world_map (x, y, tile, region) VALUES (?, ?, ?, ?)",
                        (x, y, tile, region))
    conn.commit()

def show_area(x, y, width=80, height=80, view=6):
    """
    Mostra un'area (2*view+1) x (2*view+1) intorno a (x,y).
    Di default, 'view=6' creerà una mappa 13x13. Aumentalo per mappe più estese.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()

    # Legenda
    out = "LEGGENDA: .=pianura, ^=montagna, ~=acqua, *=foresta, d=deserto, #=rovine\n"
    out += f"Mappa (visione {2*view+1}x{2*view+1}):\n"

    min_x = x - view
    max_x = x + view
    min_y = y - view
    max_y = y + view

    for row in range(min_y, max_y + 1):
        line = ""
        for col in range(min_x, max_x + 1):
            cur.execute("SELECT tile FROM world_map WHERE x=? AND y=?", (col, row))
            r = cur.fetchone()
            if r:
                char = r[0]
                # Se è la posizione del giocatore, segniamo con una @
                if col == x and row == y:
                    char = '@'
                line += char
            else:
                # Fuori dai limiti della mappa
                line += "?"
        out += line + "\n"

    conn.close()
    return out

