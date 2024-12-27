# communication/chat.py

from utils.helpers import CONNECTED_PLAYERS, get_players_in_region
import asyncio

async def handle_chat_command(player, cmd, msg):
    cmd = cmd.lower()
    if cmd == "say":
        # Chat locale (per ora stessa regione)
        region_players = get_players_in_region(player.region)
        for p in region_players:
            if p is not player:
                await p.send(f"{player.name} dice: {msg}")
        return f"Hai detto: {msg}"
    elif cmd == "shout":
        # Globale
        for p in CONNECTED_PLAYERS:
            if p is not player:
                await p.send(f"{player.name} grida: {msg.upper()}!!!")
        return f"Hai gridato: {msg.upper()}!!!"
    elif cmd == "region":
        # Messaggio a tutti nella regione
        region_players = get_players_in_region(player.region)
        for p in region_players:
            if p is not player:
                await p.send(f"[Regione] {player.name}: {msg}")
        return f"Hai inviato in Regione: {msg}"
    else:
        # Canali personalizzati: 'chat <canale> <msg>'
        # Canali fittizi: 'tower' canale sulla Torre Nera (globale)
        channel = cmd
        for p in CONNECTED_PLAYERS:
            if p is not player:
                await p.send(f"[{channel}] {player.name}: {msg}")
        return f"Hai parlato sul canale {channel}: {msg}"

