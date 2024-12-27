# server.py

import asyncio
import sqlite3
from config import HOST, PORT, DATABASE_FILE, INITIAL_MONEY, STARTING_REGION, DEFAULT_STAMINA, DEFAULT_MANA
from utils.database import init_db
from characters.creation import create_new_character, load_character_to_player
from utils.helpers import register_player, unregister_player
from utils.commands import parse_command
from utils.colors import RESET
from world.area_generator import ensure_world_generated

class PlayerConnection:
    """
    Rappresenta la connessione di un singolo giocatore.
    Contiene attributi del personaggio e metodi per l'interazione con il server.
    """
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
        self.client_address = writer.get_extra_info('peername')

        # Identificativi e stato di autenticazione
        self.name = None
        self.character_loaded = False
        self.authenticated = False

        # Flag di morte
        self.dead = False

        # Attributi del personaggio di base
        self.class_name = None
        self.level = 1
        self.exp = 0

        # Punti ferita
        self.hp = 100
        self.max_hp = 100

        # Risorse base
        self.money = 0
        self.inventory = []

        # Posizione
        self.x = 25
        self.y = 25
        self.region = STARTING_REGION

        # Achievements, quests
        self.achievements = []
        self.quests = []

        # Risorse di "energia"
        self.stamina = DEFAULT_STAMINA
        self.mana = DEFAULT_MANA

        # NUOVI ATTRIBUTI: Forza, Intelligenza, Magia
        self.strength = 0
        self.intelligence = 0
        self.magic = 0

        # Se desideri implementare resistenze per il giocatore
        self.resistances = {
            "physical": 0,  # Puoi modificare questi valori come preferisci
            "magical": 0
        }

    async def send(self, message):
        """
        Invia un messaggio testuale al client, terminandolo con \r\n.
        Usa writer.drain() per assicurarsi che i dati siano inviati su socket.
        """
        if self.dead:
            return
        try:
            self.writer.write((message + "\r\n").encode('utf-8'))
            await self.writer.drain()
        except ConnectionResetError:
            # Il client potrebbe essersi disconnesso bruscamente
            print(f"Connessione persa con {self.name if self.name else self.client_address}.")
            self.dead = True

    async def prompt_name(self):
        """
        Chiede il nome del giocatore all'avvio.
        """
        await self.send("Benvenuto in Mid-World, pellegrino. Inserisci il tuo nome:")
        try:
            data = await self.reader.readline()
            if not data:
                return False
            self.name = data.decode('utf-8').strip()
            return True
        except UnicodeDecodeError:
            await self.send("Nome non valido. Riprova.")
            return False

    def character_exists(self, name):
        """
        Controlla se esiste già un personaggio con questo nome nel database.
        """
        conn = sqlite3.connect(DATABASE_FILE)
        cur = conn.cursor()
        cur.execute("SELECT name FROM characters WHERE name=?", (name,))
        res = cur.fetchone()
        conn.close()
        return True if res else False

    async def authenticate(self):
        """
        Se il personaggio non esiste, lo crea;
        altrimenti carica i suoi dati.
        """
        if not self.character_exists(self.name):
            await self.send("Creazione nuovo personaggio...")
            await create_new_character(self)
        else:
            await self.send(f"Bentornato, {self.name}!")
            load_character_to_player(self, self.name)
        self.authenticated = True
        self.character_loaded = True

    async def main_loop(self):
        """
        Ciclo principale di ricezione comandi dal giocatore.
        """
        await self.send(f"Sei nel {self.region}. Un vento caldo soffia da ovest, portando con sé il ricordo della Torre Nera.")
        while True:
            try:
                data = await self.reader.readline()
                if not data:
                    break  # Il client ha chiuso la connessione
                try:
                    # Decodifica ignorando i byte non validi
                    command = data.decode('utf-8', errors='ignore').strip()
                except UnicodeDecodeError:
                    await self.send("Comando non valido. Usa caratteri standard.")
                    continue

                if command:
                    response = await parse_command(self, command)
                    if response:
                        await self.send(response)
            except ConnectionResetError:
                print(f"Connessione persa con {self.name if self.name else self.client_address}.")
                break
            except Exception as e:
                # Log di qualsiasi altra eccezione per debug
                print(f"Errore durante la gestione del comando da {self.name if self.name else self.client_address}: {e}")
                await self.send("Si è verificato un errore interno. Riprova più tardi.")
    
    def receive_damage(self, damage, damage_type):
        """
        Riduce i punti ferita (hp) del giocatore in base al danno e al tipo di danno.
        Considera le resistenze se definite.
        :param damage: Danno in ingresso
        :param damage_type: Tipo di danno ("physical", "magical", ecc.)
        :return: Danno effettivamente inflitto dopo la resistenza
        """
        resistance_value = self.resistances.get(damage_type, 0)
        actual_damage = max(damage - resistance_value, 0)
        self.hp -= actual_damage
        if self.hp <= 0:
            self.hp = 0
            self.dead = True
        return actual_damage

async def handle_client(reader, writer):
    """
    Coroutine che gestisce un singolo client: crea un PlayerConnection,
    esegue l'autenticazione e il loop principale, e poi chiude pulizia.
    """
    conn = PlayerConnection(reader, writer)

    # Prompt iniziale per il nome
    if not await conn.prompt_name():
        writer.close()
        return

    # Autenticazione/Caricamento personaggio
    await conn.authenticate()
    if conn.dead:
        await conn.send("Sei morto. Non puoi continuare.")
        writer.close()
        return

    # Registra il player nella lista dei connessi
    register_player(conn)

    try:
        # Ciclo principale di comandi
        await conn.main_loop()
    except ConnectionResetError:
        print(f"Connessione persa con {conn.name if conn.name else conn.client_address}.")
    finally:
        unregister_player(conn)
        writer.close()

async def main():
    """
    Punto di ingresso del server:
    - Inizializza il DB
    - Assicura la generazione della mappa
    - Avvia il server su (HOST, PORT)
    - Gestisce i client in arrivo con handle_client
    """
    init_db()               # Crea tabelle se non esistono
    ensure_world_generated()  # Genera la mappa se non esiste
    server = await asyncio.start_server(handle_client, HOST, PORT)
    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"Server avviato su {addrs}")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer interrotto da tastiera.")

