import discord
import os
import random

# Cargar variables de entorno
TOKEN =os.getenv("DISCORD_TOKEN")

# Crear cliente
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Roles del juego
roles = ["Mafioso", "Ciudadano", "Doctor", "Detective"]

partidas = {}

@client.event
async def on_ready():
    print(f'|* Bot conectado como {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!mafia crear'):
        try:
            num_jugadores = int(message.content.split()[2])
            partidas[message.channel.id] = {"jugadores": [], "roles": roles, "creador": message.author.id, "num_jugadores": num_jugadores}
            await message.channel.send(f"Se ha creado una partida de Mafia para {num_jugadores} jugadores. Usa `!mafia unirme` para participar.")
        except (IndexError, ValueError):
            await message.channel.send("Uso: !mafia crear <número de jugadores>")

    elif message.content.startswith('!mafia unirme'):
        if message.channel.id in partidas:
            partida = partidas[message.channel.id]
            if len(partida["jugadores"]) < partida["num_jugadores"]:
                partida["jugadores"].append(message.author.id)
                await message.channel.send(f"{message.author.mention} se ha unido. Jugadores actuales: {len(partida['jugadores'])}/{partida['num_jugadores']}")

                if len(partida["jugadores"]) == partida["num_jugadores"]:
                    await asignar_roles(message.channel.id)
            else:
                await message.channel.send("La partida ya está llena.")
        else:
            await message.channel.send("No hay una partida creada en este canal.")

async def asignar_roles(channel_id):
    partida = partidas[channel_id]
    random.shuffle(partida["roles"])
    for i, jugador_id in enumerate(partida["jugadores"]):
        jugador = client.get_user(jugador_id)
        rol = partida["roles"][i % len(partida["roles"])]
        await jugador.send(f"Tu rol es {rol}. Durante la noche, usa `!matar <nombre>` para eliminar a alguien en secreto.")
    await client.get_channel(channel_id).send("Todos los roles han sido asignados. ¡Que comience el juego!")

client.run(TOKEN)
