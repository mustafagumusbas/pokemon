import aiohttp
import random
import asyncio
from datetime import datetime,timedelta

class Pokemon:
    pokemons = {}
    pcon = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        
        if pokemon_trainer not in Pokemon.pcon:
            Pokemon.pcon[pokemon_trainer] = 3
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]


    async def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['forms'][0]['name']
                else:
                    return "Pikachu"

    async def get_hp(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["stats"][0]["base_stat"]
                else:
                    return 50

    async def get_attack(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["stats"][1]["base_stat"]
                else:
                    return 50

    async def get_defense(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["stats"][2]["base_stat"]
                else:
                    return 50

    async def info(self):
        if not self.name:
            self.name = await self.get_name()
            self.name = self.name.capitalize()
            self.attack = await self.get_attack()
            self.hp = await self.get_hp()
            self.defense = await self.get_defense()
            self.last_feed_time = datetime.now()
        return f"🐣 Pokémonunuzun ismi: {self.name}\n❤️ HP: {self.hp}\n⚔️ Saldırı: {self.attack}\n🛡️ Savunma: {self.defense}"

    async def show_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['sprites']['front_default']
                else:
                    return None

    async def saldir(self, enemy):
        if self.hp <= 0:
            return f"{self.name} fiziksel ve mental açıdan çok yoruldu ⚰️"

        if isinstance(enemy, Wizard):
            sans = random.randint(1, 4)
            if sans == 1:
                return f"{enemy.name}, savaşta bir kalkan kullandı 🛡️!"

        hasar = round(self.attack * (enemy.defense / (enemy.defense + 100)))
        
        if enemy.hp <= hasar:
            enemy.hp = 0
            Pokemon.pcon[self.pokemon_trainer] += 2

            trainer = enemy.pokemon_trainer
            if trainer in Pokemon.pokemons:
                del Pokemon.pokemons[trainer]

            return (f"{self.name} {enemy.name}'e saldırdı⚔️.\n"
                    f"{enemy.name} yenildi🩻\n"
                    f"{enemy.name} hiçliğe karıştı🌌\n"
                    f"2 Pcon kazandınız 💰! Toplam: {Pokemon.pcon[self.pokemon_trainer]}")        
        else:
            enemy.hp -= hasar
            enemy.hp = round(enemy.hp)
            return f"{self.name} {enemy.name}'e saldırdı⚔️. {hasar} hasar verdi.\n{enemy.name}'in canı {enemy.hp} kaldı❤️"

    async def feed(self, feed_interval=20, hp_increase=10):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"{self.name} iyileşti. Mevcut sağlık: {self.hp}"
        else:
            return f"{self.name}'i şu zaman besleyebilirsiniz: {current_time+delta_time}"

class Fighter(Pokemon):
    async def info(self):
        base_info = await super().info()
        return base_info + f"\n✨ Özel Güç bonusuyla extra hasar"
    async def feed(self,feed_interval=20, hp_increase=10):
        hp_increase += random.randint(1,20)
        return await super().feed(feed_interval, hp_increase)
    
    
    async def saldir(self, enemy):
        super_guc = random.randint(10, 20)
        self.attack += super_guc
        sonuc = await super().saldir(enemy)
        self.attack -= super_guc
        return sonuc + f"\n{self.name} süper saldırı kullandı ✨. Eklenen güç: {super_guc}"


class Wizard(Pokemon):
    async def info(self):
        base_info = await super().info()
        return base_info + "\n🛡️  %25 ihtimalle sıfır hasar alma"
    async def feed(self,feed_interval=20, hp_increase=10):
        feed_interval -= random.randint(1,15)
        return await super().feed(feed_interval, hp_increase)






# hocam biliyorum emojiler bi tık yapay zeka şüphesi uyandırıyor ama sadece chatgpyye görünüşünü 
# nası güzelleştirebilirim dedim oda emoji ekliyebilirsin dedi yani bana güvenin hocam

if __name__ == '__main__':
    async def deneme():
        oyun = 1
        while True:
            print(f"\n🔁 Tur {oyun}")
            print()
            pokemon1 = Fighter("123")
            pokemon2 = Wizard("213")
            print(await pokemon1.info())
            print(await pokemon2.info())
            print()
            print("=================================================")
            print()
            while True:
                print(await pokemon1.saldir(pokemon2))
                if pokemon2.hp <= 0:
                    break
                print(await pokemon2.saldir(pokemon1))
                if pokemon1.hp <= 0:
                    break
                print()
                print("=================================================")
                print()
                await asyncio.sleep(21)
            print()
            cevap = input("🔁 Tekrar başlatmak için q yaz: ")
            if cevap.lower() != "q":
                break
            oyun += 1

    asyncio.run(deneme())
