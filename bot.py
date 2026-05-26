import discord
from discord.ext import commands
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

FUSO = ZoneInfo("America/Sao_Paulo")

bosses = {
    "kharzul": (7, 8),
    "vescrya": (7, 8),
    "yellow": (10, 11),
    "blue": (10, 11),
    "reddragon": (12, 12),
    "red": (12, 12),
    "bogar": (2, 3),
    "moltragon": (1, 2),
    "dreadhorn": (1, 2),
    "muggron": (7, 8)
}

async def alerta(channel, nome, servidor, abrir, fechar):

    agora = datetime.now(FUSO)

    espera = (
        abrir
        - timedelta(minutes=10)
        - agora
    ).total_seconds()

    if espera > 0:
        await asyncio.sleep(espera)

    await channel.send(
        f"⚠️ {nome.upper()} [{servidor.upper()}]\n"
        f"Faltam 10 minutos para abrir."
    )

    agora = datetime.now(FUSO)

    espera = (
        fechar
        - timedelta(minutes=10)
        - agora
    ).total_seconds()

    if espera > 0:
        await asyncio.sleep(espera)

    await channel.send(
        f"🔴 {nome.upper()} [{servidor.upper()}]\n"
        f"Faltam 10 minutos para encerrar."
    )

@bot.event
async def on_ready():
    print(
        f"Bot online como {bot.user}"
    )

@bot.command()
async def testealerta(ctx):

    canal = discord.utils.get(
        ctx.guild.text_channels,
        name="alerta-boss"
    )

    if not canal:
        await ctx.send(
            "Canal alerta-boss não encontrado"
        )
        return

    await ctx.send(
        "Teste iniciado (10 segundos)"
    )

    await asyncio.sleep(10)

    await canal.send(
        "🚨 TESTE FUNCIONANDO"
    )

@bot.command()
async def boss(
    ctx,
    nome=None,
    servidor=None
):

    if not nome or not servidor:

        await ctx.send(
            "Use: !boss kharzul s1"
        )

        return

    nome = nome.lower()
    servidor = servidor.lower()

    if nome not in bosses:

        await ctx.send(
            "Boss não encontrado"
        )

        return

    min_h, max_h = bosses[nome]

    agora = datetime.now(FUSO)

    abrir = (
        agora
        + timedelta(
            hours=min_h
        )
    )

    fechar = (
        agora
        + timedelta(
            hours=max_h
        )
    )

    canal = discord.utils.get(
        ctx.guild.text_channels,
        name="alerta-boss"
    )

    if canal:

        asyncio.create_task(
            alerta(
                canal,
                nome,
                servidor,
                abrir,
                fechar
            )
        )

    await ctx.send(
        f"""
🔥 {nome.upper()} [{servidor.upper()}]

☠️ Morto:
{agora.strftime('%H:%M')}

⏳ Spawn:
{abrir.strftime('%H:%M')}
~
{fechar.strftime('%H:%M')}
"""
    )

TOKEN = os.getenv(
    "TOKEN"
)

bot.run(TOKEN)
