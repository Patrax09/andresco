import discord # Importa la libreria discord.py, necessaria per interagire con Discord
from discord.ext import commands  # Importa il modulo commands per creare comandi del bot
import youtube_dl # Importa youtube_dl per gestire l'estrazione di audio da YouTube


# Imposta il prefisso per i comandi del bot
intents = discord.Intents.default() # Configura gli intenti di Discord necessari per ricevere eventi base dal server
intents.message_content = True # Abilita l'intento per leggere il contenuto dei messaggi
bot = commands.Bot(command_prefix="!", intents=intents)  # Crea un'istanza del bot con un prefisso di comando e gli intenti configurati


# Comando per far entrare il bot in un canale vocale
@bot.command() # Definisce un nuovo comando del bot
async def join(ctx): # Definisce il comando 'join', che fa entrare il bot in un canale vocale
    if ctx.author.voice:  # Controlla se l'autore del comando è in un canale vocale
        channel = ctx.author.voice.channel #salva dove lutente ha usato il comando
        await channel.connect() #il bot entra nel canale
    else:
        await ctx.send("Devi essere in un canale vocale per usare questo comando!") # Messaggio se l'utente non è in un canale vocale

# Comando per far uscire il bot dal canale vocale
@bot.command() # Definisce un nuovo comando del bot
async def leave(ctx):  # Definisce il comando 'leave', che fa uscire il bot dal canale vocale
    if ctx.voice_client:  # Controlla se il bot è connesso a un canale vocale
        await ctx.voice_client.disconnect() # Disconnette il bot dal canale vocale
    else:
        await ctx.send("Non sono in un canale vocale!")  # Messaggio se il bot non è in un canale vocale

# Comando per riprodurre una canzone
@bot.command() # Definisce un nuovo comando del bot
async def play(ctx, *, url):  # Definisce il comando 'play', che riproduce una canzone da un URL
    if not ctx.voice_client: # Controlla se il bot è connesso a un canale vocale
        await ctx.send("Devo essere in un canale vocale per riprodurre musica. Usa il comando !join.") # Messaggio se il bot non è connesso
        return

    # Configurazione per youtube_dl
    ydl_opts = {  # Opzioni di configurazione per youtube_dl
        'format': 'bestaudio/best', # Scarica il miglior formato audio disponibile
        'postprocessors': [{ # Configura il post-processamento
            'key': 'FFmpegExtractAudio', # Utilizza FFmpeg per estrarre l'audio
            'preferredcodec': 'mp3', # Codec preferito: MP3
            'preferredquality': '192', # Qualità preferita: 192kbps
        }],
    }
  with youtube_dl.YoutubeDL(ydl_opts) as ydl: # Crea un'istanza di youtube_dl con le opzioni configurate
        info = ydl.extract_info(url, download=False) # Estrae informazioni dal video senza scaricarlo
        url2 = info['formats'][0]['url'] # Ottiene l'URL diretto dell'audio
        ctx.voice_client.stop()  # Ferma qualsiasi audio in riproduzione
        ctx.voice_client.play(discord.FFmpegPCMAudio(url2), after=lambda e: print(f"Errore: {e}"))  # Riproduce l'audio usando FFmpeg
        await ctx.send(f"Sto riproducendo: {info['title']}") # Invia un messaggio con il titolo della canzone

# Comando per fermare la riproduzione
@bot.command() # Definisce un nuovo comando del bot
async def stop(ctx): # Definisce il comando 'stop', che ferma la riproduzione corrente
    if ctx.voice_client: # Controlla se il bot è connesso a un canale vocale
        ctx.voice_client.stop() # Ferma l'audio in riproduzione
    else:
        await ctx.send("Non c'\u00e8 musica da fermare!")  # Messaggio se non c'è musica da fermare

# Esegui il bot con il tuo token
bot.run("IL_TUO_TOKEN_DEL_BOT") # Avvia il bot utilizzando il token fornito



