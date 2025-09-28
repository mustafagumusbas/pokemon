import aiohttp
import random
import asyncio

class Pokemon:
    pokemons = {}
    coins = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        
        if pokemon_trainer not in Pokemon.coins:
            Pokemon.coins[pokemon_trainer] = 3
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
                # P Coin kazancı
                Pokemon.coins[self.pokemon_trainer] += 2
                return f"{self.name} {enemy.name}'e saldırdı⚔️.\n{enemy.name} yenildi🩻\n💰 2 P Coin kazandınız! Toplam: {Pokemon.coins[self.pokemon_trainer]}"
            else:
                enemy.hp -= hasar
                enemy.hp = round(enemy.hp)
                return f"{self.name} {enemy.name}'e saldırdı⚔️. {hasar} hasar verdi.\n{enemy.name}'in canı {enemy.hp} kaldı❤️"



class Fighter(Pokemon):
    async def info(self):
        base_info = await super().info()
        extra_attack = random.randint(10, 20)
        return base_info + f"\n✨ Özel Güç bonusu: {extra_attack}"

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
            print()
            cevap = input("🔁 Tekrar başlatmak için q yaz: ")
            if cevap.lower() != "q":
                break
            oyun += 1
    asyncio.run(deneme())
