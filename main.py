import discord
from discord.ext import commands
from config import token
from logic import Pokemon, Fighter, Wizard, quiz_questions
import random
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

last_attack_time = {}
user_responses = {}

async def send_question(ctx_or_interaction, user_id):
    question = quiz_questions[user_responses[user_id]]
    buttons = question.gen_buttons()
    view = discord.ui.View()
    for button in buttons:
        view.add_item(button)

    if isinstance(ctx_or_interaction, commands.Context):
        await ctx_or_interaction.send(question.text, view=view)
    else:
        await ctx_or_interaction.followup.send(question.text, view=view)

@bot.event
async def on_ready():
    print(f'Giriş yapıldı: {bot.user.name}')


user_wrong_count = {}  

@bot.event
async def on_interaction(interaction):
    user_id = interaction.user.id
    author_name = interaction.user.name

    if user_id not in user_responses:
        await interaction.response.send_message("Lütfen /quiz komutunu kullanarak testi başlatın")
        return

    await interaction.response.defer()

    custom_id = interaction.data["custom_id"]
    question = quiz_questions[user_responses[user_id]] 

    if custom_id.startswith("correct"):
        Pokemon.pcon[author_name] = Pokemon.pcon.get(author_name, 0) + 1
        await interaction.followup.send(f"✅ Doğru cevap! Pcon'in: {Pokemon.pcon[author_name]}")
    elif custom_id.startswith("wrong"):
        correct_answer = question.options[question._Question__answer_id]  
        await interaction.followup.send(f"❌ Yanlış cevap! Doğru cevap: **{correct_answer}**")

        if user_id not in user_wrong_count:
            user_wrong_count[user_id] = 1
        else:
            user_wrong_count[user_id] += 1

        if user_wrong_count[user_id] % 3 == 0:
            Pokemon.pcon[author_name] = max(Pokemon.pcon.get(author_name, 0) - 1, 0)
            await interaction.followup.send(f"⚠️ 3 yanlış cevap verdiğiniz için 1 Pcon harcandı! Kalan Pcon: {Pokemon.pcon.get(author_name,0)}")

    user_responses[user_id] += 1

    if user_responses[user_id] >= MAX_QUESTIONS:
        await interaction.followup.send(f"🏁 Sınav bitti! Toplam Pcon'in: {Pokemon.pcon.get(author_name, 0)}")
    else:
        await send_question(interaction, user_id)


MAX_QUESTIONS = 5  

@bot.command()
async def quiz(ctx):
    author_name = ctx.author.name
    if author_name not in Pokemon.pcon:
                Pokemon.pcon[author_name] = 3
    if Pokemon.pcon.get(author_name, 0) >= 1:
        Pokemon.pcon[author_name] -= 1
        random.shuffle(quiz_questions)
        user_id = ctx.author.id

        if user_id in user_responses and user_responses[user_id] >= MAX_QUESTIONS:
            user_responses[user_id] = 0  

        if user_id not in user_responses:
            user_responses[user_id] = 0

        await send_question(ctx, user_id)
    else:
        await ctx.send("Yeterli Pconunuz yok💰")




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
async def feed(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons.keys():
        await ctx.send("😑")
    else:
        poke = Pokemon.pokemons[author]
        await ctx.send(await poke.feed())

@bot.command()
async def sil(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons.keys():
        await ctx.send("😑")
    else:
        if Pokemon.pcon[author] >= 1:
            Pokemon.pcon[author] -= 1
            del Pokemon.pokemons[author]
            await ctx.send(f"Pokemon Silindi 🗑️")
            await ctx.send(f"1 Pcon harcandı 💰 Kalan : {Pokemon.pcon[author]}")
        else:
            await ctx.send("Yeterli Pcon yok! Silmek için en az 1 Pcon gerekli 💰")

@bot.command()
async def inf(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons:
        await ctx.send("😑")
    else:
        poke = Pokemon.pokemons[author]
        await ctx.send(await poke.info())
        image_url = await poke.show_img(ctx)
        if image_url:
            embed = discord.Embed()
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)

@bot.command()
async def coin(ctx):
    author = ctx.author.name
    if author in Pokemon.pcon:
        await ctx.send(f" {author}, şu anda {Pokemon.pcon[author]} Pcon'in var 💰")
    else:
        await ctx.send(f" {author}, şu anda hiç Pcon'in yok 💰")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.strip() == "(╯°□°)╯︵ ┻━┻":
        await message.channel.send("┬─┬ノ( º _ ºノ)")
    await bot.process_commands(message)

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

@bot.command()
async def snorlax(ctx):
    role_name = "❀"
    has_role = discord.utils.get(ctx.author.roles, name=role_name)

    if not has_role:
        await ctx.send("Bu komutu kullanmak için ❀ rolüne sahip olman gerekiyor 🌸")
        return

    author = ctx.author.name

    if author in Pokemon.pokemons:
        await ctx.send("Zaten bir Pokémon'un var!")
        return

    sans = random.randint(1,5)
    if author not in Pokemon.pcon:
        Pokemon.pcon[author] = 3

    if sans==5 and Pokemon.pcon[author] >= 1:
        snorlax = Pokemon(author)
        snorlax.pokemon_number = 143
        snorlax.name = "Snorlax"
        snorlax.hp = 999
        snorlax.attack = 999
        snorlax.defense = 999
        snorlax.last_feed_time = asyncio.get_event_loop().time()

        Pokemon.pokemons[author] = snorlax
        Pokemon.pcon[author] = Pokemon.pcon.get(author, 3)

        file_path = r"..\pokemon\images\snorlax.jpeg"
        file = discord.File(file_path, filename="snorlax.jpeg")

        embed = discord.Embed(
            title="😴 Snorlax senin oldu!",
            description=(
                "🐼 **İsim:** Snorlax\n"
                "❤️ **HP:** 999\n"
                "⚔️ **Saldırı:** 999\n"
                "🛡️ **Savunma:** 999\n"
            ),
            color=discord.Color.green()
        )
        embed.set_image(url="attachment://snorlax.jpeg")

        await ctx.send(file=file, embed=embed)
        await ctx.send(f"{ctx.author.mention}, artık efsanevi Snorlax seninle! 🌙")
        Pokemon.pcon[author] -= 1
    else:
        if Pokemon.pcon[author] >= 1:
            Pokemon.pcon[author] -= 1
            await ctx.send("Snorlax uykusundan uyanamadı 😴")
        else:
            await ctx.send("Yeterli Pcon'unuz yok")

bot.run(token)

