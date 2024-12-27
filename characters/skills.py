# characters/skills.py (Aggiornato)

import asyncio
import random
from utils.database import save_character

class Skill:
    def __init__(self, name, ability_type, cost, description, effect):
        self.name = name
        self.ability_type = ability_type  # "physical", "magia", "utility"
        self.cost = cost  # mana or stamina cost
        self.description = description
        self.effect = effect  # Funzione che applica l'effetto

    async def execute(self, caster, target):
        if self.ability_type == "physical":
            damage = caster.strength + random.randint(5, 15)
            actual_damage = target.receive_damage(damage, "physical")
            return f"Hai usato {self.name} su {target.name}, infliggendo {actual_damage} danni fisici."
        elif self.ability_type == "magia":
            if self.name == "Canto Cura":
                heal = 30
                caster.hp = min(caster.max_hp, caster.hp + heal)
                return f"Hai usato {self.name}, recuperando {heal} HP."
            elif self.name == "Canto Terrore":
                # Riduci temporaneamente l'attacco del nemico
                target.attack = max(target.attack - 10, 0)
                return f"Hai usato {self.name}, riducendo l'attacco di {target.name}!"
        elif self.ability_type == "utility":
            if self.name == "Piazza Trappola":
                # Implementa la logica della trappola
                # Placeholder
                return f"Hai piazzato una trappola nell'area."
        return "Effetto dell'abilità non implementato."

SKILLS = {
    "gunslinger": {
        "tiro rapido": Skill(
            name="Tiro Rapido",
            ability_type="physical",
            cost=10,
            description="Un attacco veloce e preciso.",
            effect=None  # Implementare l'effetto specifico
        ),
        "doppio colpo": Skill(
            name="Doppio Colpo",
            ability_type="physical",
            cost=20,
            description="Esegui due attacchi consecutivi.",
            effect=None
        )
    },
    "taheen": {
        "urlo assordante": Skill(
            name="Urlo Assordante",
            ability_type="magia",
            cost=15,
            description="Emette un urlo potente che infligge danni magici.",
            effect=None
        ),
        "artigli": Skill(
            name="Artigli",
            ability_type="physical",
            cost=10,
            description="Attacchi con artigli affilati.",
            effect=None
        )
    },
    "cantore_dossa": {
        "canto cura": Skill(
            name="Canto Cura",
            ability_type="magia",
            cost=10,
            description="Recupera una quantità di HP.",
            effect=None
        ),
        "canto terrore": Skill(
            name="Canto Terrore",
            ability_type="magia",
            cost=15,
            description="Induce paura nei nemici, riducendo la loro efficacia.",
            effect=None
        )
    },
    "ladro_dei_nodi": {
        "piazza trappola": Skill(
            name="Piazza Trappola",
            ability_type="utility",
            cost=5,
            description="Posiziona una trappola nell'area.",
            effect=None
        ),
        "colpo furtivo": Skill(
            name="Colpo Furtivo",
            ability_type="physical",
            cost=15,
            description="Un attacco potente e nascosto.",
            effect=None
        )
    }
}

async def use_skill(player, skill_name):
    cls_skills = SKILLS.get(player.class_name, {})
    skill = cls_skills.get(skill_name.lower())
    if not skill:
        return "Non conosci questa abilità."

    # Controlla costi
    if skill.ability_type == "magia" and player.mana < skill.cost:
        return "Non hai abbastanza mana."
    if skill.ability_type == "physical" and player.stamina < skill.cost:
        return "Non hai abbastanza stamina."

    # Deduce il costo
    if skill.ability_type == "magia":
        player.mana -= skill.cost
    elif skill.ability_type == "physical":
        player.stamina -= skill.cost

    # Esegui l'abilità
    # Dovrai implementare la logica per selezionare il target effettivo
    # Placeholder: supponiamo che il target sia un mob casuale
    from world.mobs import get_random_mob
    target = get_random_mob()
    result = await skill.execute(player, target)
    save_character(player)
    return result

