import discord
from discord.ext import commands
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

FUSO = ZoneInfo("America/Sao_Paulo")
CARGO = "<@&1275524067901968571>"
CANAL_ALERTA = "alerta-boss"

tarefas_alerta = []

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
    "muggron": (3, 4)
}

async def alerta(channel, nome, servidor, abrir):
    try:
        agora = datetime.now(FUSO)
        horario_alerta = abrir - timedelta(minutes=10)
        espera = (horario_alerta - agora).total_seconds()

        if espera > 0:
            await asyncio.sleep(espera)

        await channel.send(
f"""
{CARGO}

⚠️ **{nome.upper()} [{servidor.upper()}]**

Faltam **10 minutos** para abrir a janela.
"""
        )

    except asyncio.CancelledError:
        return


@bot.event
async def on_ready():
    print(f"Bot online como {bot.user}")


@bot.command()
async def testealerta(ctx):
    canal = discord.utils.get(ctx.guild.text_channels, name=CANAL_ALERTA)

    if not canal:
        await ctx.send("❌ Canal alerta-boss não encontrado.")
        return

    await ctx.send("✅ Teste iniciado. Aguarde 10 segundos.")

    await asyncio.sleep(10)

    await canal.send(
f"""
{CARGO}

🚨 **TESTE FUNCIONANDO**

Se essa mensagem apareceu, o canal de alerta está correto.
"""
    )


@bot.command()
async def desligartodos(ctx):
    total = len(tarefas_alerta)

    for tarefa in tarefas_alerta:
        tarefa.cancel()

    tarefas_alerta.clear()

    await ctx.send(
f"""
🛑 Todos os timers/alertas foram desligados.

Alertas cancelados: {total}
"""
    )


@bot.command()
async def boss(ctx, nome=None, servidor=None):
    if not nome or not servidor:
        await ctx.send("Use: `!boss kharzul s1`")
        return

    nome = nome.lower()
    servidor = servidor.lower()

    if nome not in bosses:
        await ctx.send("❌ Boss não encontrado.")
        return

    min_h, max_h = bosses[nome]

    agora = datetime.now(FUSO)
    abrir = agora + timedelta(hours=min_h)
    fechar = agora + timedelta(hours=max_h)

    canal = discord.utils.get(ctx.guild.text_channels, name=CANAL_ALERTA)

    if canal:
        tarefa = asyncio.create_task(alerta(canal, nome, servidor, abrir))
        tarefas_alerta.append(tarefa)
        status_alerta = f"✅ Alerta agendado em #{CANAL_ALERTA}"
    else:
        status_alerta = f"❌ Canal #{CANAL_ALERTA} não encontrado"

    await ctx.send(
f"""
{CARGO}

🔥 **{nome.upper()} [{servidor.upper()}]**

☠️ Morto:
**{agora.strftime('%H:%M')}**

⏳ Spawn:
**{abrir.strftime('%H:%M')} ~ {fechar.strftime('%H:%M')}**

🔔 Alerta:
**{(abrir - timedelta(minutes=10)).strftime('%H:%M')}**

{status_alerta}
"""
    )


TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
