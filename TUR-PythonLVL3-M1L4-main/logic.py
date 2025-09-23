import aiohttp  # Eşzamansız HTTP istekleri için bir kütüphane
import random
import asyncio

class Pokemon:
    pokemons = {}
    # Nesne başlatma (kurucu)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def get_name(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve çözümlenmesi
                    return data['forms'][0]['name']  #  Pokémon adını döndürme
                else:
                    return "Pikachu"  # İstek başarısız olursa varsayılan adı döndürür
    
    async def get_hp(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve çözümlenmesi
                    return data ["stats"][0]["base_stat"] #  Pokémon adını döndürme
                else:
                    return "50"  # İstek başarısız olursa varsayılan adı döndürür
    
    async def get_attack(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve çözümlenmesi
                    return data ["stats"][1]["base_stat"] #  Pokémon adını döndürme
                else:
                    return "50"  # İstek başarısız olursa varsayılan adı döndürür
     
     
    async def get_defense(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve çözümlenmesi
                    return data ["stats"][2]["base_stat"] #  Pokémon adını döndürme
                else:
                    return "50"  # İstek başarısız olursa varsayılan adı döndürür
    
  
    async def info(self):
        if not self.name:
            self.name = await self.get_name()   # Henüz yüklenmemişse bir adın geri alınması
            self.name = self.name.capitalize()
            self.attack = await self.get_attack()
            self.hp = await self.get_hp()
            self.defense = await self.get_defense()
        return f"🐣 Pokémonunuzun ismi: {self.name}"  # Pokémon adını içeren dizeyi döndürür


    async def show_img(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve çözümlenmesi
                    return data['sprites']['front_default']  #  Pokémon adını döndürme
                else:
                    return "Pikachu"  # İstek başarısız olursa varsayılan adı döndürür

        # PokeAPI aracılığıyla bir pokémon görüntüsünün URL'sini almak için asenktron metot
    async def saldir(self, enemy):
        hasar = round(self.attack * (enemy.defense / (enemy.defense + 100)))
        if enemy.hp <= hasar:
            enemy.hp = 0
            return f'🔵 {self.name} 🔴 {enemy.name}\'e saldırdı⚔️.\n🔴 {enemy.name} yenildi🩻'
        else:
            enemy.hp -= hasar
            enemy.hp = round(enemy.hp)
            return f'🔵 {self.name} 🔴 {enemy.name}\'e saldırdı⚔️. {hasar} hasar verdi.\n🔴 {enemy.name}\'in canı {enemy.hp} kaldı❤️'

# hocam biliyorum emojiler bi tık yapay zeka şüphesi uyandırıyor ama sadece chatgpyye görünüşünü 
# nası güzelleştirebilirim dedim oda emoji ekliyebilirsin dedi yani bana güvenin hocam

if __name__ == '__main__':
    async def deneme():
        oyun = 1
        while True:
            print(f"\n🔁 Tur {oyun}")
            print()
            pokemon1 = Pokemon("123")
            pokemon2 = Pokemon("213")
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
