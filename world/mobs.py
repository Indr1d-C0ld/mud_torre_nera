# world/mobs.py

import random
from items.loot_tables import get_loot
# Se usi abilità dei personaggi, potresti importare anche i relativi moduli, ma fai attenzione agli import circolari.
# from characters.skills import Skill  # Solo se serve

class Mob:
    """
    Classe base per tutte le entità ostili nel MUD.
    """
    def __init__(self, name, description, strength, intelligence, magic, abilities, resistances, hp, attack, exp):
        """
        :param name: Nome del mob (es. "Randall Flagg")
        :param description: Descrizione del mob
        :param strength: Forza fisica
        :param intelligence: Intelligenza
        :param magic: Potere magico
        :param abilities: Lista di oggetti Ability (abilità speciali)
        :param resistances: Dizionario {tipo_danno: valore_resistenza} (es. {"physical": 10, "magical": 30})
        :param hp: Punti ferita iniziali
        :param attack: Attacco base
        :param exp: Esperienza rilasciata alla morte
        """
        self.name = name
        self.description = description
        self.strength = strength
        self.intelligence = intelligence
        self.magic = magic
        self.abilities = abilities
        self.resistances = resistances
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.exp = exp

        # Se il mob dovesse aver bisogno di mana o stamina propri, puoi aggiungerli qui
        # es. self.mana = 100, self.stamina = 100, ecc.

    def is_alive(self):
        """Ritorna True se il mob ha ancora HP > 0."""
        return self.hp > 0

    def receive_damage(self, damage, damage_type):
        """
        Riduce gli HP del mob in base alle resistenze.
        :param damage: Danno in ingresso
        :param damage_type: Tipo di danno ("physical", "magical", ecc.)
        :return: Danno effettivamente inflitto dopo la resistenza
        """
        resistance_value = self.resistances.get(damage_type, 0)
        actual_damage = max(damage - resistance_value, 0)
        self.hp -= actual_damage
        return actual_damage

    def perform_attack(self, target):
        """
        Esegue un attacco base fisico contro il target.
        :param target: L'entità o il giocatore bersaglio
        :return: Danno inflitto
        """
        return target.receive_damage(self.attack, "physical")

    async def use_ability(self, ability_name, target):
        """
        Tenta di usare un'abilità denominata ability_name contro il target.
        Di default, se l'abilità non è trovata, restituisce un messaggio di errore.
        Questa funzione può essere sovrascritta nelle classi figlie per logiche speciali.
        """
        ability = next((a for a in self.abilities if a.name.lower() == ability_name.lower()), None)
        if ability:
            return await ability.execute(self, target)
        else:
            return f"{self.name} non conosce l'abilità {ability_name}."


class Ability:
    """
    Classe che rappresenta un'abilità speciale (fisica, magica o utility).
    """
    def __init__(self, name, ability_type, cost, description):
        """
        :param name: Nome dell'abilità
        :param ability_type: Tipo di abilità ("physical", "magia", "utility")
        :param cost: Costo in risorse (mana o stamina) - se implementato
        :param description: Descrizione testuale dell'abilità
        """
        self.name = name
        self.ability_type = ability_type
        self.cost = cost
        self.description = description

    async def execute(self, caster, target):
        """
        Esegue l'abilità, applicando il suo effetto su `target`.
        :param caster: Chi sta usando l'abilità (mob)
        :param target: Bersaglio dell'abilità (giocatore o altro)
        :return: Messaggio descrittivo dell'effetto
        """
        # Esempio generico di esecuzione (dovrai personalizzare se necessario)
        # Se l'abilità è "physical", applichiamo un danno in base a caster.strength
        # Se "magia", usiamo caster.magic, ecc.
        # Se "utility", potremmo teletrasportare, curare, etc.
        msg = f"{caster.name} usa {self.name} su {target.name} (Effetto generico non implementato)."
        return msg


# -------------------------------------------------------------------
# Di seguito le classi dei vari Mob ispirati a "La Torre Nera".
# L'ordine è importante: devono apparire DOPO Mob e Ability.
# -------------------------------------------------------------------

class RandallFlagg(Mob):
    def __init__(self):
        abilities = [
            Ability("Illusione", "magia", 20, "Crea illusioni che confondono il nemico."),
            Ability("Controllo Mentale", "magia", 30, "Controlla temporaneamente un nemico."),
            Ability("Teletrasporto", "utility", 25, "Si teletrasporta a breve distanza.")
        ]
        resistances = {
            "physical": 5,
            "magical": 20
        }
        super().__init__(
            name="Randall Flagg",
            description="Un potente mago e antagonista principale, noto come il Signore della Macchina.",
            strength=50,
            intelligence=90,
            magic=100,
            abilities=abilities,
            resistances=resistances,
            hp=300,
            attack=25,
            exp=500
        )

    async def use_ability(self, ability_name, target):
        # Esempio di override se vuoi implementare logiche speciali
        ability = next((a for a in self.abilities if a.name.lower() == ability_name.lower()), None)
        if ability:
            # Qui puoi gestire diversamente each ability
            return await ability.execute(self, target)
        else:
            return f"{self.name} non conosce l'abilità {ability_name}."


class CrimsonKing(Mob):
    def __init__(self):
        abilities = [
            Ability("Manipolazione della Realtà", "magia", 25, "Altera la realtà circostante."),
            Ability("Evocazione Oscura", "magia", 30, "Evoca creature oscure per combattere."),
            Ability("Controllo degli Elementi", "magia", 20, "Controlla fuoco, acqua, aria e terra.")
        ]
        resistances = {
            "physical": 50,
            "magical": 100
        }
        super().__init__(
            name="Re Cremisi",
            description="La principale minaccia alla Torre Nera, un'entità che vuole distruggerla.",
            strength=100,
            intelligence=90,
            magic=150,
            abilities=abilities,
            resistances=resistances,
            hp=1000,
            attack=50,
            exp=1000
        )


class LowMen(Mob):
    def __init__(self):
        abilities = [
            Ability("Attacco Base", "physical", 0, "Attacco corpo a corpo con armi leggere.")
        ]
        resistances = {
            "physical": 10,
            "magical": 5
        }
        super().__init__(
            name="Low Men",
            description="Servitori umani del Re Cremisi, corrotti e vendicativi.",
            strength=30,
            intelligence=50,
            magic=20,
            abilities=abilities,
            resistances=resistances,
            hp=100,
            attack=15,
            exp=20
        )


class Taheen(Mob):
    def __init__(self):
        abilities = [
            Ability("Attacco Fisico Potente", "physical", 0, "Attacchi fisici devastanti."),
            Ability("Resistenza Fisica", "physical", 0, "Alta resistenza ai danni fisici.")
        ]
        resistances = {
            "physical": 30,
            "magical": 0
        }
        super().__init__(
            name="Taheen",
            description="Grandi animali corazzati e predatori che abitano il deserto.",
            strength=80,
            intelligence=20,
            magic=0,
            abilities=abilities,
            resistances=resistances,
            hp=200,
            attack=35,
            exp=50
        )


class GuardianTorre(Mob):
    def __init__(self):
        abilities = [
            Ability("Barriera Magica", "magia", 20, "Crea barriere magiche."),
            Ability("Attacco Magico Potente", "magia", 25, "Attacchi magici ad alto danno."),
            Ability("Teletrasporto", "utility", 15, "Si teletrasporta rapidamente.")
        ]
        resistances = {
            "physical": 40,
            "magical": 40
        }
        super().__init__(
            name="Guardian della Torre",
            description="Entità magiche incaricate di proteggere la Torre Nera.",
            strength=70,
            intelligence=90,
            magic=100,
            abilities=abilities,
            resistances=resistances,
            hp=500,
            attack=30,
            exp=300
        )


class ScreamingEagle(Mob):
    def __init__(self):
        abilities = [
            Ability("Attacco Aereo", "physical", 0, "Attacchi rapidi dall'aria."),
            Ability("Volo Veloce", "utility", 0, "Si muove rapidamente sopra il campo di battaglia.")
        ]
        resistances = {
            "physical": 15,
            "magical": 0
        }
        super().__init__(
            name="Screaming Eagle",
            description="Vasti uccelli predatori usati come veicoli o per il combattimento aereo.",
            strength=50,
            intelligence=30,
            magic=0,
            abilities=abilities,
            resistances=resistances,
            hp=150,
            attack=25,
            exp=40
        )


class ThePusher(Mob):
    def __init__(self):
        abilities = [
            Ability("Manipolazione Mentale", "magia", 20, "Induce paura e confusione nei nemici."),
            Ability("Illusione", "magia", 15, "Crea illusioni per disorientare gli avversari."),
            Ability("Controllo delle Emozioni", "magia", 25, "Manipola le emozioni per indebolire i nemici.")
        ]
        resistances = {
            "physical": 5,
            "magical": 25
        }
        super().__init__(
            name="The Pusher",
            description="Creature che utilizzano l'inganno e la manipolazione psicologica.",
            strength=20,
            intelligence=80,
            magic=60,
            abilities=abilities,
            resistances=resistances,
            hp=80,
            attack=10,
            exp=30
        )


class TheKeeper(Mob):
    def __init__(self):
        abilities = [
            Ability("Incantesimi di Protezione", "magia", 20, "Crea scudi magici."),
            Ability("Rilevazione Intrusi", "magia", 15, "Rileva presenze di intrusi nelle vicinanze."),
            Ability("Manipolazione Tempo-Spazio", "magia", 25, "Altera il tempo e lo spazio.")
        ]
        resistances = {
            "physical": 25,
            "magical": 30
        }
        super().__init__(
            name="The Keeper",
            description="Guardiani enigmatici che custodiscono segreti e passaggi verso la Torre.",
            strength=50,
            intelligence=100,
            magic=90,
            abilities=abilities,
            resistances=resistances,
            hp=400,
            attack=20,
            exp=250
        )


class Screamer(Mob):
    def __init__(self):
        abilities = [
            Ability("Attacco Sonoro", "magia", 20, "Urla potenti che infliggono danni mentali."),
            Ability("Manipolazione Percezioni", "magia", 15, "Altera le percezioni dei nemici.")
        ]
        resistances = {
            "physical": 0,
            "magical": 30
        }
        super().__init__(
            name="Screamer",
            description="Entità spettrali che emettono urla potenti per disorientare i nemici.",
            strength=10,
            intelligence=60,
            magic=80,
            abilities=abilities,
            resistances=resistances,
            hp=120,
            attack=15,
            exp=35
        )


class WastelanderCorrupt(Mob):
    def __init__(self):
        abilities = [
            Ability("Combattimento Corpo a Corpo", "physical", 0, "Combattimento diretto con armi."),
            Ability("Utilizzo di Armi", "physical", 0, "Abilità nell'uso di varie armi.")
        ]
        resistances = {
            "physical": 15,
            "magical": 5
        }
        super().__init__(
            name="Wastelander Corrupt",
            description="Ex alleati diventati traditori sotto l'influenza del Re Cremisi.",
            strength=60,
            intelligence=60,
            magic=20,
            abilities=abilities,
            resistances=resistances,
            hp=180,
            attack=30,
            exp=40
        )

# Funzione di utilità per generare un mob casuale (ad esempio, durante incontri random)
def get_random_mob():
    """
    Restituisce un'istanza di una delle classi Mob definite sopra.
    """
    mob_classes = [
        RandallFlagg,
        CrimsonKing,
        LowMen,
        Taheen,
        GuardianTorre,
        ScreamingEagle,
        ThePusher,
        TheKeeper,
        Screamer,
        WastelanderCorrupt
    ]
    chosen_class = random.choice(mob_classes)
    return chosen_class()

