import discord
from discord.ext import commands
from datetime import datetime, timedelta
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

bosses = {
    "kharzul": (7, 8),
    "vescrya": (7, 8),
    "yellow": (10, 11),
    "blue": (10, 11),
    "reddragon": (12, 12),
    "bogar": (2, 3),
    "moltragon": (1, 2),
    "dreadhorn": (1, 2),
    "muggron": (7, 8),
}

@bot.event
async def on_ready():
    print(f'Bot online como {bot.user}')

@bot.command()
async def boss(ctx, nome=None, servidor=None):

    if nome is None or servidor is None:
        await ctx.send("Use: /boss nome servidor")
        return

    nome = nome.lower()

    if nome not in bosses:
        await ctx.send("Boss não encontrado.")
        return

    min_h, max_h = bosses[nome]

    agora = datetime.now()

    min_spawn = agora + timedelta(hours=min_h)
    max_spawn = agora + timedelta(hours=max_h)

    mensagem = (
        f"🔥 {nome.upper()} [{servidor.upper()}]\n\n"
        f"☠️ Morto às {agora.strftime('%H:%M')}\n\n"
        f"⏳ Próximo spawn:\n"
        f"{min_spawn.strftime('%H:%M')} ~ {max_spawn.strftime('%H:%M')}"
    )

    await ctx.send(mensagem)

TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
