import sqlite3
from config import DATABASE_FILE

# Definizione quest
QUESTS = {
    "corno_eld": {
        "name": "Trova il Corno di Eld",
        "description": "Roland ti chiede di ritrovare il leggendario Corno di Eld, nascosto nelle rovine di Lud.",
        "stages": ["Non iniziata", "In corso", "Completata"],
        "reward_exp": 200,
        "reward_item": "Corno di Eld"
    }
}

async def handle_quest_command(player, action, qid):
    if action == "info":
        return quest_info_command(player, qid)
    elif action == "start":
        return quest_start(player, qid)
    elif action == "complete":
        return quest_complete(player, qid)
    else:
        return "Azione quest non valida. Usa: quest start|info|complete <id>"

def quest_info_command(player, qid):
    if qid not in QUESTS:
        return "Quest sconosciuta."
    q = QUESTS[qid]
    return f"{q['name']}: {q['description']} Stadi: {', '.join(q['stages'])}"

def quest_start(player, qid):
    if qid not in QUESTS:
        return "Quest sconosciuta."
    if qid in player.quests:
        return "Hai già questa quest."
    player.quests.append(qid)
    save_quest_status(player.name, qid, "In corso")
    return f"Hai iniziato la quest: {QUESTS[qid]['name']}."

def quest_complete(player, qid):
    if qid not in QUESTS:
        return "Quest sconosciuta."
    if qid not in player.quests:
        return "Non hai questa quest attiva."
    # Con una logica più complessa si controllerebbero le condizioni
    # Supponiamo che il giocatore abbia già trovato l'oggetto
    player.exp += QUESTS[qid]["reward_exp"]
    player.inventory.append(QUESTS[qid]["reward_item"])
    save_quest_status(player.name, qid, "Completata")
    return f"Hai completato la quest {QUESTS[qid]['name']}! Ricevi {QUESTS[qid]['reward_exp']} EXP e {QUESTS[qid]['reward_item']}."

def save_quest_status(name, qid, status):
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO quest_status (name, quest_id, status) VALUES (?, ?, ?)",
                (name, qid, status))
    conn.commit()
    conn.close()

