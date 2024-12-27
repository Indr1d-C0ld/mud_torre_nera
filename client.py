# client.py

import asyncio
import sys
import os
import platform

# Configurazione del server MUD
HOST = '127.0.0.1'
PORT = 4000

# Abilitazione dei codici ANSI su Windows
def enable_ansi_windows():
    if os.name == 'nt':
        import ctypes
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE = -11
        mode = ctypes.c_ulong()
        kernel32.GetConsoleMode(handle, ctypes.byref(mode))
        mode.value |= 0x0004  # ENABLE_VIRTUAL_TERMINAL_PROCESSING
        kernel32.SetConsoleMode(handle, mode)

async def read_from_server(reader):
    while True:
        data = await reader.readline()
        if not data:
            print("Connessione chiusa dal server.")
            sys.exit(0)
        # Decodifica il messaggio
        msg = data.decode('utf-8', errors='replace').rstrip('\r\n')
        # Stampa direttamente il messaggio (contiene già eventuali colori ANSI)
        print(msg)

async def write_to_server(writer):
    # Legge input da stdin (utente)
    loop = asyncio.get_event_loop()
    while True:
        # Usa run_in_executor per non bloccare l'evento asincrono
        command = await loop.run_in_executor(None, sys.stdin.readline)
        if not command:
            break
        command = command.rstrip('\r\n')
        if command.lower() in ['exit', 'quit']:
            print("Disconnessione...")
            writer.close()
            await writer.wait_closed()
            sys.exit(0)
        writer.write((command + '\n').encode('utf-8'))
        await writer.drain()

async def main():
    enable_ansi_windows()
    print(f"Connessione al MUD {HOST}:{PORT}...")
    try:
        reader, writer = await asyncio.open_connection(HOST, PORT)
    except ConnectionRefusedError:
        print("Connessione fallita. Assicurati che il server sia in esecuzione.")
        sys.exit(1)
    print("Connesso! Digita i comandi. 'quit' per uscire.")
    
    # Esegui due task in parallelo: lettura dal server e scrittura da utente
    read_task = asyncio.create_task(read_from_server(reader))
    write_task = asyncio.create_task(write_to_server(writer))

    await asyncio.gather(read_task, write_task)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interruzione da tastiera.")
        sys.exit(0)

