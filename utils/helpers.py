# utils/helpers.py

import asyncio

CONNECTED_PLAYERS = []

def register_player(player):
    CONNECTED_PLAYERS.append(player)

def unregister_player(player):
    if player in CONNECTED_PLAYERS:
        CONNECTED_PLAYERS.remove(player)

async def broadcast_message(message):
    for p in CONNECTED_PLAYERS:
        await p.send(message)

def get_players_in_region(region):
    return [p for p in CONNECTED_PLAYERS if p.region == region]

