# utils/commands.py

import random
import sqlite3
from config import DATABASE_FILE
from utils.helpers import CONNECTED_PLAYERS, get_players_in_region
from communication.chat import handle_chat_command
from world.area_generator import show_area
from world.mobs import get_random_mob
from combat.combat_system import engage_combat, attack_command
from characters.skills import use_skill
from utils.database import save_character

# Descrizioni di base per le tile e le regioni, usate da look_command
tile_descriptions = {
    '.': "Pianura sconfinata, l'erba è bassa e il vento soffia piano.",
    '^': "Montagne e rocce alte, il terreno è impervio.",
    '~': "Acqua o paludi fangose, devi muoverti con cautela.",
    '*': "Una fitta foresta, gli alberi coprono la visuale.",
    'd': "Sabbia e caldo torrido: sei in un deserto ostile.",
    '#': "Ruderi antichi, pieni di detriti e strutture crollate."
}

region_descriptions = {
    "Deserto del Mohaine": "Un vasto deserto che si estende per miglia, con sabbia e calore soffocante.",
    "Foresta Nera": "Alberi secolari e un'oscurità palpabile fra i rami, si sentono strani versi.",
    "Città di Lud": "Una città in rovina, con architetture decadenti e vecchi macchinari arrugginiti.",
    "Calla Bryn Sturgis": "Un villaggio pacifico con campi fertili e gente ospitale, ma i Lupi non sono lontani.",
    "End-World": "Terra desolata ai confini della realtà, dove la Torre Nera si avvicina."
}

def look_command(player):
    """
    Fornisce una descrizione basata sia sulla tile che sulla regione, 
    così che l'esplorazione non risulti vuota.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute("SELECT tile, region FROM world_map WHERE x=? AND y=?", (player.x, player.y))
    row = cur.fetchone()
    conn.close()

    if row:
        tile, region = row
        tile_desc = tile_descriptions.get(tile, "Un terreno indefinito.")
        region_desc = region_descriptions.get(region, "Un'area sconosciuta.")
        return (f"Sembra di essere in {region}. {region_desc}\n"
                f"Terreno: {tile_desc}")
    else:
        return "Non riesci a capire bene dove ti trovi... Oltre i confini della mappa?"

async def player_move(player, direction):
    """
    Gestisce lo spostamento del personaggio in una delle 4 direzioni (n, s, e, w)
    e prevede la possibilità di incontri casuali.
    """
    old_x, old_y = player.x, player.y

    if direction == 'n':
        player.y -= 1
    elif direction == 's':
        player.y += 1
    elif direction == 'w':
        player.x -= 1
    elif direction == 'e':
        player.x += 1
    else:
        return "Direzione non valida (usa n, s, e, w)."

    # Verifica di non uscire dalla mappa (supponendo 80x80 di default)
    if player.x < 0:
        player.x = 0
        return "Non puoi andare oltre, c'è un baratro invalicabile."
    if player.x >= 80:
        player.x = 79
        return "Ti fermi davanti a un canyon invalicabile."
    if player.y < 0:
        player.y = 0
        return "Non puoi spingerti più a nord, ci sono montagne invalicabili."
    if player.y >= 80:
        player.y = 79
        return "Il terreno a sud è troppo ostile per proseguire."

    move_msg = f"Ti muovi verso {direction.upper()} (da {old_x},{old_y} a {player.x},{player.y})."

    # Chance di incontro casuale, ad esempio 20%
    if random.random() < 0.20:
        mob = get_random_mob()
        # Inizia subito il combattimento con il mob
        encounter_msg = f"Mentre ti sposti, incontri un {mob.name}!"
        result = await engage_combat(player, mob)
        # Salva lo stato del personaggio dopo il combattimento
        save_character(player)
        return move_msg + "\n" + encounter_msg + "\n" + result

    return move_msg

async def parse_command(player, command):
    """
    Interpreta il comando testuale inserito dal giocatore
    e restituisce un output stringa (o None) da inviare al giocatore.
    """
    if player.dead:
        return "Sei morto. Non puoi fare nulla."

    if not command.strip():
        return None

    cmd_parts = command.split()
    base = cmd_parts[0].lower()
    args = cmd_parts[1:]

    if base == "help":
        return ("Comandi disponibili:\n"
                "- help: mostra questo elenco\n"
                "- say <msg>, shout <msg>, region <msg>, chat <canale> <msg>: comunicazioni\n"
                "- map: mostra la mappa ASCII\n"
                "- look: osserva l'area circostante\n"
                "- move <n|s|e|w>: muoviti in una direzione\n"
                "- attack <target>: attacca un bersaglio (player o mob)\n"
                "- skill <nome_skill>: usa una skill della tua classe\n"
                "- stats: mostra le tue statistiche\n"
                "- quit: esci dal gioco")

    elif base == "say":
        msg = " ".join(args)
        return await handle_chat_command(player, "say", msg)

    elif base == "shout":
        msg = " ".join(args)
        return await handle_chat_command(player, "shout", msg)

    elif base == "region":
        msg = " ".join(args)
        return await handle_chat_command(player, "region", msg)

    elif base == "chat":
        # chat <canale> <messaggio>
        if len(args) < 2:
            return "Uso: chat <canale> <messaggio>"
        channel = args[0]
        msg = " ".join(args[1:])
        return await handle_chat_command(player, channel, msg)

    elif base == "map":
        # Mostra un'area più ampia intorno al giocatore
        # Ad esempio 13x13 => view=6
        return show_area(player.x, player.y, width=80, height=80, view=6)

    elif base == "look":
        return look_command(player)

    elif base == "move":
        if not args:
            return "Uso: move <n|s|e|w>"
        direction = args[0].lower()
        return await player_move(player, direction)

    elif base == "attack":
        # es. "attack RandallFlagg"
        target_name = args[0] if args else None
        return await attack_command(player, target_name)

    elif base == "stats":
        # Mostra statistiche del PG
        return (f"Nome: {player.name}\n"
                f"Classe: {player.class_name}\n"
                f"Livello: {player.level} (EXP: {player.exp})\n"
                f"HP: {player.hp}/{player.max_hp}\n"
                f"Stamina: {player.stamina}\n"
                f"Mana: {player.mana}\n"
                f"Denaro: {player.money}\n"
                f"Inventario: {', '.join(player.inventory)}\n"
                f"Achievements: {', '.join(player.achievements)}\n"
                f"Quests: {', '.join(player.quests)}")

    elif base == "skill":
        # Usa una skill della classe del PG
        if not args:
            return "Uso: skill <nome_skill>"
        skill_name = " ".join(args).lower()
        result = await use_skill(player, skill_name)
        return result

    elif base == "quit":
        await player.send("Arrivederci!")
        player.writer.close()
        return None

    else:
        return "Comando sconosciuto."

