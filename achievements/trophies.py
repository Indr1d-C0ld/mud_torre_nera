import sqlite3
from config import DATABASE_FILE

TROPHIES = {
    "uccidi_re_rosso": {
        "name": "Sconfitta del Re Rosso",
        "description": "Hai sconfitto il Re Rosso, colui che minaccia la Torre Nera.",
        "condition": lambda player: player.exp >= 1000 # semplificato
    },
    "raggiungi_torre": {
        "name": "Alla Base della Torre",
        "description": "Hai raggiunto la Torre Nera stessa.",
        "condition": lambda player: player.region == "End-World" # semplificato
    }
}

async def check_achievements(player):
    for ach_id, ach in TROPHIES.items():
        if ach_id not in player.achievements and ach["condition"](player):
            player.achievements.append(ach_id)
            await player.send(f"Hai sbloccato un Trofeo: {ach['name']}")
            save_achievement(player.name, ach_id)

def save_achievement(name, ach_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO achievements (name, achievement_id, unlocked) VALUES (?, ?, ?)",
                (name, ach_id, 1))
    conn.commit()
    conn.close()

