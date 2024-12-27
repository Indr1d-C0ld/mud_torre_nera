# combat/combat_system.py (Aggiornato)

import random
from world.mobs import get_random_mob
from items.loot_tables import get_loot
from utils.database import save_character
from characters.skills import SKILLS

async def attack_command(player, target_name):
    if not target_name:
        mob = get_random_mob()
        return await engage_combat(player, mob)
    else:
        # Tentativo di PvP
        from utils.helpers import CONNECTED_PLAYERS
        target_player = next((p for p in CONNECTED_PLAYERS if p.name.lower() == target_name.lower()), None)
        if target_player and target_player is not player:
            return await engage_pvp(player, target_player)
        else:
            return "Non c'è nessun giocatore con quel nome."

async def engage_combat(player, mob):
    combat_log = []
    combat_log.append(f"Incontri un {mob.name}! {mob.description}")
    while mob.is_alive() and player.hp > 0:
        # Turno del giocatore
        combat_log.append(f"Tuo HP: {player.hp}/{player.max_hp}")
        combat_log.append(f"{mob.name} HP: {mob.hp}/{mob.max_hp}")
        combat_log.append("Cosa vuoi fare? (attaccare, usare <abilità>, fuggire)")
        # Gestione input del giocatore
        # Placeholder: supponiamo che il giocatore scelga di attaccare
        action = "attaccare"  # Placeholder per demo
        if action == "attaccare":
            damage = player.strength + random.randint(0, 5)
            actual_damage = mob.receive_damage(damage, "physical")
            combat_log.append(f"Hai attaccato {mob.name} per {actual_damage} danni.")
        elif action.startswith("usare"):
            _, skill_name = action.split(" ", 1)
            res = await use_skill(player, skill_name)
            combat_log.append(res)
        elif action == "fuggire":
            combat_log.append("Hai tentato di fuggire!")
            return "\n".join(combat_log)
        # Turno del mob
        if mob.is_alive():
            # Decidi se il mob usa un'abilità o attacca normalmente
            if mob.abilities and random.random() < 0.3:  # 30% di probabilità di usare un'abilità
                ability = random.choice(mob.abilities)
                res = await mob.use_ability(ability.name, player)
                combat_log.append(res)
            else:
                damage = mob.attack + random.randint(0, 5)
                actual_damage = player.receive_damage(damage, "physical")
                combat_log.append(f"{mob.name} ti ha attaccato per {actual_damage} danni.")
    # Fine del combattimento
    if player.hp <= 0:
        player.dead = True
        combat_log.append(f"{mob.name} ti ha sconfitto! Permadeath attivo.")
    elif not mob.is_alive():
        player.exp += mob.exp
        loot = get_loot(mob.name)
        if loot:
            player.inventory.append(loot)
            combat_log.append(f"Hai ucciso {mob.name}! Ottieni {mob.exp} EXP e raccogli {loot}.")
        combat_log.append("Combatto concluso.")
    save_character(player)
    return "\n".join(combat_log)

async def engage_pvp(attacker, defender):
    combat_log = []
    combat_log.append(f"{attacker.name} sta attaccando {defender.name}!")
    while defender.hp > 0 and attacker.hp > 0:
        # Turno dell'attaccante
        damage = attacker.strength + random.randint(0, 5)
        actual_damage = defender.receive_damage(damage, "physical")
        combat_log.append(f"Hai attaccato {defender.name} per {actual_damage} danni.")
        # Turno del difensore
        if defender.hp > 0:
            damage = defender.attack + random.randint(0, 5)
            actual_damage = attacker.receive_damage(damage, "physical")
            combat_log.append(f"{defender.name} ti ha attaccato per {actual_damage} danni.")
    if attacker.hp <= 0:
        attacker.dead = True
        combat_log.append(f"{defender.name} ti ha sconfitto! Permadeath attivo.")
    elif defender.hp <= 0:
        attacker.exp += defender.exp
        loot = get_loot(defender.name)
        if loot:
            attacker.inventory.append(loot)
            combat_log.append(f"Hai sconfitto {defender.name} e raccogli {loot}.")
        combat_log.append("Combatto concluso.")
    save_character(attacker)
    save_character(defender)
    return "\n".join(combat_log)

