============================================================
                  MUD Torre Nera - README
============================================================

## **Introduzione**
Benvenuto in **MUD Torre Nera**, un gioco di ruolo testuale multiutente ispirato all'universo di "La Torre Nera".
Questo progetto è puramente *embrionale* ma offre un modello di esperienza di esplorazione, combattimento e interazione in un mondo che sarebbe potenzialmente ricco di ambientazioni e entità ostili.
Cercasi appassionati e sviluppatori che possano raccogliere questo modello per poterlo rendere davvero un MUD fantastico!

## **Funzionalità Introdotte**
- **Sistema di Classi Giocatore**: Quattro classi giocabili con statistiche uniche (Gunslinger, Taheen, Cantore Dossa, Ladro dei Nodi).
- **Generazione della Mappa**: Mappa del mondo generata in modo procedurale con vari tipi di terreno (pianura, montagna, acqua, foresta, deserto, rovine).
- **Comandi di Base**:
  - `map`: Visualizza una porzione della mappa in ASCII con una legenda.
  - `move <n|s|e|w>`: Muove il personaggio in una direzione specifica con possibilità di incontri casuali.
  - `look`: Fornisce descrizioni dettagliate dell'area circostante basate sul tipo di terreno e regione.
  - `attack <target>`: Attacca un bersaglio (giocatore o mob).
  - `skill <nome_skill>`: Usa una skill della propria classe.
  - `stats`: Mostra le statistiche del personaggio.
  - `say`, `shout`, `region`, `chat`: Comandi di comunicazione.
  - `quit`: Esci dal gioco.
- **Sistema di Combattimento**: Combattimenti sia PvE (contro mob) che PvP (contro altri giocatori) con gestione delle abilità e delle resistenze.
- **Database Persistente**: Utilizzo di SQLite per salvare e caricare i dati dei personaggi, stati delle quest, achievements e mob attivi.
- **Gestione degli Incontri Casuali**: Possibilità di incontrare mob casuali durante gli spostamenti con una percentuale di probabilità configurabile.
- **Descrizioni Dinamiche**: Descrizioni variegate delle aree basate sul tipo di terreno e regione per un'esperienza di esplorazione più immersiva.

## **Descrizione del Programma**
**MUD Torre Nera** è un server di gioco testuale che permette a più giocatori di connettersi simultaneamente e interagire in un mondo persistente. I giocatori possono creare e personalizzare il proprio personaggio scegliendo tra diverse classi, esplorare la mappa, combattere contro entità ostili, completare quest e interagire con altri giocatori tramite comandi di chat.

## **Come Utilizzarlo**

### **1. Requisiti di Sistema**
- **Python 3.11** o superiore
- **SQLite3**
- Sistema operativo: Linux (es. Debian) o Windows

### **2. Installazione**
## **1. **Clona il Repository**

   git clone https://github.com/tuo_username/mud_torre_nera.git
   cd mud_torre_nera
   
## **2. Installa le Dipendenze Assicurati di avere Python 3.11 installato. Installa eventuali pacchetti richiesti:

    pip install -r requirements.txt

    (Nota: crea un file requirements.txt se necessario con le dipendenze del progetto)

## **3. Configurazione

    Configura le Impostazioni Modifica il file config.py per impostare parametri come HOST, PORT, DATABASE_FILE, ecc.

    # config.py
    HOST = '127.0.0.1'
    PORT = 4000
    DATABASE_FILE = 'mud_game.db'
    INITIAL_MONEY = 100
    STARTING_REGION = "Deserto del Mohaine"
    DEFAULT_STAMINA = 100
    DEFAULT_MANA = 50

## **4. Inizializzazione del Database

    Avvia il Server Prima di avviare il server, assicurati che il database sia inizializzato:

    python3 server.py

    Il server eseguirà automaticamente init_db() per creare le tabelle necessarie e ensure_world_generated() per generare la mappa del mondo.

## **5. Connessione al Server

    Usa un Client Telnet Puoi connetterti al server utilizzando Telnet o un client Telnet compatibile.
        Su Linux/Debian:

        telnet 127.0.0.1 4000

        Su Windows: Usa un client Telnet come PuTTY o usa PyInstaller per creare un EXE a partire dal file client.py.

## ** 6. Creazione e Gestione del Personaggio

    Inserisci il Nome Al primo avvio, il server ti chiederà di inserire il nome del tuo personaggio. Se il nome non esiste, verrà creato un nuovo personaggio.
    Scegli la Classe Durante la creazione del personaggio, scegli una delle classi disponibili:
        Gunslinger: Pistolero veloce e preciso.
        Taheen: Ibrido uomo-uccello, versatile.
        Cantore Dossa: Cantore magico con poteri psichici.
        Ladro dei Nodi: Furtivo e abile con trappole.

## **7. Utilizzo dei Comandi

    help: Mostra l'elenco dei comandi disponibili.
    map: Visualizza una porzione della mappa del mondo.
    move <n|s|e|w>: Muovi il personaggio nella direzione specificata.
    look: Osserva l'area circostante e ottieni descrizioni dettagliate.
    attack <target>: Attacca un bersaglio.
    skill <nome_skill>: Usa una skill della tua classe.
    stats: Mostra le statistiche del tuo personaggio.
    say <msg>, shout <msg>, region <msg>, chat <canale> <msg>: Comandi di comunicazione.
    quit: Esci dal gioco.

Opzioni Disponibili

    Personalizzazione delle Abilità: Usa le abilità specifiche della tua classe durante i combattimenti.
    Interazione con Altri Giocatori: Utilizza i comandi di chat per comunicare con altri giocatori nella stessa regione o a livello globale.
    Esplorazione Dinamica: Muoviti attraverso diverse regioni del mondo, ognuna con caratteristiche uniche e potenziali incontri.
    Sistema di Combattimento Avanzato: Combatti contro mob ostili o altri giocatori, utilizzando attacchi fisici o abilità magiche.
    Persistenza dei Dati: Tutti i progressi e le modifiche al personaggio vengono salvati nel database, garantendo la continuità tra le sessioni di gioco.

## **Preparazione del Sistema
## **1. Installazione di Python e SQLite

    Python 3.11: Assicurati che Python 3.11 sia installato sul tuo sistema.

python3 --version

SQLite3: Verifica che SQLite3 sia installato.

    sqlite3 --version

## **2. Configurazione del Database

    Il server si occuperà automaticamente di creare e aggiornare il database alla prima esecuzione.
    Assicurati che il file di database (mud_game.db o quello specificato in config.py) sia accessibile e che il server abbia i permessi necessari per leggerlo e scriverlo.

## **3. Generazione della Mappa

    La mappa del mondo verrà generata automaticamente se non esiste già.
    Se desideri rigenerare la mappa, cancella la tabella world_map nel database e riavvia il server.

## **Prossimi Passi

Per rendere MUD Torre Nera funzionale, più ricco e coinvolgente, vorrei l'implementazione di:

    Sistema di Quest Avanzato: Implementare quest line con obiettivi multipli e ricompense.
    Interazione con NPC: Aggiungere personaggi non giocanti con cui i giocatori possono interagire.
    Magie e Abilità Più Variegate: Espandere il sistema di abilità con effetti più complessi e personalizzati.
    Sistema di Inventario Migliorato: Gestione avanzata degli oggetti, equipaggiamento e crafting.
    Interfaccia Client Migliorata: Sviluppare un client grafico o una web interface per una migliore esperienza utente.
    Sicurezza e Gestione delle Connessioni: Migliorare la gestione delle eccezioni e la sicurezza delle connessioni.
    Leaderboard e Classifiche: Implementare un sistema di classifiche per i giocatori basato su esperienza, missioni completate, ecc.
    Eventi Dinamici e Ambientazioni Speciali: Aggiungere eventi a tempo, boss statici e ambientazioni uniche.
    Supporto per Plugin o Moduli Esterni: Permettere estensioni modulari per aggiungere nuove funzionalità senza modificare il core del server.
    Backup e Ripristino del Database: Implementare meccanismi automatici di backup e ripristino per prevenire perdite di dati.
