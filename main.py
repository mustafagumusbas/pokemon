import discord
from discord.ext import commands
from config import token
from logic import Pokemon, Fighter, Wizard
import random
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

last_attack_time = {}

@bot.event
async def on_ready():
    print(f'Giriş yapıldı: {bot.user.name}')

@bot.command()
async def go(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons.keys():
        psec = random.randint(1,3)
        if psec == 1:
            pokemon = Pokemon(author)
            await ctx.send("Size Sıradan Pokemon denk geldi")
        if psec == 2:
            pokemon = Fighter(author)
            await ctx.send("Size Savaşçı Pokemon denk geldi")
        if psec == 3:
            pokemon = Wizard(author)
            await ctx.send("Size Büyücü Pokemon denk geldi")

        await ctx.send(await pokemon.info())
        image_url = await pokemon.show_img()
        if image_url:
            embed = discord.Embed()
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Pokémonun görüntüsü yüklenemedi!")
    else:
        await ctx.send("Zaten kendi Pokémonunuzu oluşturdunuz!")

@bot.command()
async def sil(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons.keys():
        await ctx.send("😑")
    else:
        if Pokemon.coins[author] >= 1:
            Pokemon.coins[author] -= 1
            del Pokemon.pokemons[author]
            await ctx.send(f"Pokemon Silindi 🗑️")
            await ctx.send(f"1 Pcon harcandı 💰 Kalan : {Pokemon.coins[author]}")
        else:
            await ctx.send("Yeterli Pcon yok! Silmek için en az 1 Pcon gerekli 💰")


@bot.command()
async def attack(ctx):
    author = ctx.author.name
    now = asyncio.get_event_loop().time()

    if author in last_attack_time:
        elapsed = now - last_attack_time[author]
        if elapsed < 3:  
            await ctx.send(f"Tekrar saldırman için 3 saniye beklemen gerekiyor. {round(3 - elapsed, 1)} saniye kaldı⏳")
            return

    last_attack_time[author] = now

    target = ctx.message.mentions[0] if ctx.message.mentions else None
    if target:
        if target.name in Pokemon.pokemons and ctx.author.name in Pokemon.pokemons:
            enemy = Pokemon.pokemons[target.name]
            attacker = Pokemon.pokemons[ctx.author.name]
            result = await attacker.saldir(enemy)
            await ctx.send(result)
        else:
            await ctx.send("Savaş için her iki tarafın da Pokémon sahibi olması gerekir!")
    else:
        await ctx.send("Saldırmak istediğiniz kullanıcıyı etiketleyerek belirtin.")

bot.run(token)
