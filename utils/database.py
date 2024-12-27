# utils/database.py

import sqlite3
from config import DATABASE_FILE

def init_db():
    """
    Inizializza il database, creando le tabelle se non esistono,
    e aggiunge eventuali colonne nuove con ALTER TABLE, in modo da
    mantenere lo schema aggiornato.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()

    #
    # 1) Tabella dei personaggi (characters)
    #
    cur.execute("""
    CREATE TABLE IF NOT EXISTS characters (
        name TEXT PRIMARY KEY,
        class TEXT,
        level INTEGER,
        exp INTEGER,
        hp INTEGER,
        max_hp INTEGER,
        x INTEGER,
        y INTEGER,
        money INTEGER,
        inventory TEXT,
        achievements TEXT,
        quests TEXT,
        region TEXT,
        stamina INTEGER,
        mana INTEGER
        -- NOTA: le colonne strength, intelligence e magic 
        -- verranno aggiunte via ALTER TABLE più sotto, se non esistono
    )
    """)

    # Aggiunta campi strength, intelligence, magic se mancanti
    try:
        cur.execute("ALTER TABLE characters ADD COLUMN strength INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    try:
        cur.execute("ALTER TABLE characters ADD COLUMN intelligence INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    try:
        cur.execute("ALTER TABLE characters ADD COLUMN magic INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass

    #
    # 2) Tabella world_map
    #
    cur.execute("""
    CREATE TABLE IF NOT EXISTS world_map (
        x INTEGER,
        y INTEGER,
        tile TEXT,
        region TEXT,
        PRIMARY KEY (x, y)
    )
    """)

    #
    # 3) Altre tabelle (leaderboard, quest_status, achievements, merchants, ecc.)
    #
    cur.execute("""
    CREATE TABLE IF NOT EXISTS leaderboard (
        name TEXT,
        score INTEGER,
        quests_completed INTEGER,
        achievements_unlocked INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS quest_status (
        name TEXT,
        quest_id TEXT,
        status TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS achievements (
        name TEXT,
        achievement_id TEXT,
        unlocked INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS merchants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        region TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS merchant_items (
        merchant_id INTEGER,
        item_name TEXT,
        price INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS active_mobs (
        x INTEGER,
        y INTEGER,
        mob_type TEXT,
        hp INTEGER,
        PRIMARY KEY (x, y)
    )
    """)

    # Chiude le modifiche
    conn.commit()
    conn.close()

def save_character(player):
    """
    Salva (o aggiorna) nel DB le informazioni del personaggio 'player'.
    Presuppone che la tabella 'characters' abbia le colonne indicate.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()

    # Convertiamo liste in stringhe (inventory, achievements, quests)
    inv_str = ",".join(player.inventory)
    ach_str = ",".join(player.achievements)
    que_str = ",".join(player.quests)

    cur.execute("""
    INSERT OR REPLACE INTO characters
    (name, class, level, exp, hp, max_hp, x, y, money, inventory,
     achievements, quests, region, stamina, mana, strength, intelligence, magic)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        player.name,
        player.class_name,
        player.level,
        player.exp,
        player.hp,
        player.max_hp,
        player.x,
        player.y,
        player.money,
        inv_str,
        ach_str,
        que_str,
        player.region,
        player.stamina,
        player.mana,
        player.strength,
        player.intelligence,
        player.magic
    ))

    conn.commit()
    conn.close()

def load_character(name):
    """
    Carica dal DB i dati di un personaggio con 'name'.
    Restituisce la tupla contenente i campi (o None se non esiste).
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            name, 
            class, 
            level, 
            exp, 
            hp, 
            max_hp, 
            x, 
            y, 
            money, 
            inventory, 
            achievements, 
            quests, 
            region, 
            stamina, 
            mana, 
            strength, 
            intelligence, 
            magic
        FROM characters 
        WHERE name=?
    """, (name,))
    row = cur.fetchone()
    conn.close()
    return row

def save_quest_status(name, qid, status):
    """
    Salva o aggiorna lo stato di una quest (quest_id) per un dato personaggio (name).
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO quest_status (name, quest_id, status)
        VALUES (?, ?, ?)
    """, (name, qid, status))
    conn.commit()
    conn.close()

def save_achievement(name, ach_id):
    """
    Segna un trofeo/achievement come sbloccato per un personaggio.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO achievements (name, achievement_id, unlocked) 
        VALUES (?, ?, 1)
    """, (name, ach_id))
    conn.commit()
    conn.close()

def save_active_mob(x, y, mob_type, hp):
    """
    Salva nella tabella 'active_mobs' un mob presente sulla mappa,
    a coordinate (x, y), di tipo 'mob_type' e con HP correnti.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO active_mobs (x, y, mob_type, hp)
        VALUES (?, ?, ?, ?)
    """, (x, y, mob_type, hp))
    conn.commit()
    conn.close()

def load_active_mobs():
    """
    Restituisce una lista di tuple (x, y, mob_type, hp) con i mob attivi.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute("SELECT x, y, mob_type, hp FROM active_mobs")
    mobs = cur.fetchall()
    conn.close()
    return mobs

