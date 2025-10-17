import aiohttp
import random
import asyncio
from datetime import datetime
from discord import ui, ButtonStyle
from collections import defaultdict


class Question:
    def __init__(self, text, answer_id, *options):
        self.__text = text
        self.__answer_id = answer_id
        self.options = list(options)

    @property
    def text(self):
        return self.__text

    def shuffle_options(self):
        combined = list(enumerate(self.options))
        random.shuffle(combined)
        for new_index, (old_index, _) in enumerate(combined):
            if old_index == self.__answer_id:
                self.__answer_id = new_index
        self.options = [option for _, option in combined]

    def gen_buttons(self):
        butonlar = []
        for indeks, cevap in enumerate(self.options):
            if indeks == self.__answer_id:
                butonlar.append(ui.Button(label=cevap, style=ButtonStyle.primary, custom_id=f'correct_{indeks}'))
            else:
                butonlar.append(ui.Button(label=cevap, style=ButtonStyle.primary, custom_id=f'wrong_{indeks}'))
        return butonlar

quiz_questions = [
    Question("Ash'in ilk Pokémon'u hangisidir?", 0, "Pikachu", "Charmander", "Bulbasaur", "Squirtle"),
    Question("Pikachu hangi türdendir?", 1, "Normal", "Elektrik", "Uçan", "Çelik"),
    Question("Charmander evrimleştiğinde ne olur?", 2, "Charjabug", "Charbroil", "Charmeleon", "Charizard"),
    Question("Bulbasaur’un sırtındaki bitki nedir?", 0, "Tohum", "Mantar", "Ağaç", "Çiçek"),
    Question("Ash'in ilk rakibi kimdir?", 1, "Misty", "Gary", "Brock", "May"),
    Question("Team Rocket'in ünlü sloganı hangi kelimeyle biter?", 3, "Başarı!", "Patlama!", "Kaçış!", "Meowth, doğru bildin!"),
    Question("Pokédex ne işe yarar?", 0, "Pokémonları tanımlar", "Pokémonları yakalar", "Pokéball üretir", "Eğitmenleri arar"),
    Question("Pokéball ne işe yarar?", 1, "Saldırı yapar", "Pokémon yakalar", "Can doldurur", "Eğitmen çağırır"),
    Question("Pokémon evrim geçirdiğinde ne olur?", 0, "Yeni bir forma dönüşür", "Zayıflar", "Tür değiştirir", "İsmini kaybeder"),
    Question("Pikachu’nun evrimleşmiş hali kimdir?", 2, "Pichu", "Plusle", "Raichu", "Emolga"),
    Question("Ash’in ilk rozetini aldığı lider kimdir?", 1, "Misty", "Brock", "Lt. Surge", "Erika"),
    Question("Su tipi Pokémon’lar hangi tipe karşı güçlüdür?", 0, "Ateş", "Elektrik", "Bitki", "Toprak"),
    Question("Ateş tipi Pokémon’lar hangi tipe karşı zayıftır?", 2, "Çelik", "Kaya", "Su", "Hayalet"),
    Question("Ash’in Kanto’daki en sadık Pokémon’u kimdir?", 0, "Pikachu", "Snorlax", "Onix", "Pidgeot"),
    Question("Pokémon dünyasında 'Gym' nedir?", 3, "Mağaza", "Kütüphane", "Ev", "Spor salonu (arena)"),
    Question("Pokémon evrimini genellikle ne tetikler?", 0, "Seviye artışı", "Eğitmen seviyesi", "Pokéball", "Renk değişimi"),
    Question("Pokémon Center’da kim görev yapar?", 1, "Team Rocket", "Hemşire Joy", "Profesör Oak", "Ash’in annesi"),
    Question("Pokémon savaşında kazanan ne elde eder?", 2, "Yeni Pokémon", "Pokéball", "Deneyim puanı", "Rozet"),
    Question("Pidgey hangi tip Pokémon’dur?", 3, "Elektrik", "Su", "Kaya", "Uçan"),
    Question("Pokémon evrim taşlarından biri nedir?", 1, "Hava Taşı", "Ateş Taşı", "Karanlık Taşı", "Gölge Taşı"),
    Question("Eevee toplamda kaç farklı evrime sahip olabilir? (8. nesil itibarıyla)", 2, "5", "6", "8", "10"),
    Question("Pikachu hangi bölgede ilk kez tanıtılmıştır?", 0, "Kanto", "Johto", "Hoenn", "Sinnoh"),
    Question("Pokémon Ligi’ni kazanmak için ne gerekir?", 3, "Pokédex", "Birkaç taş", "Tüm Pokémonlar", "Tüm rozetler"),
    Question("Ash’in annesinin adı nedir?", 1, "Erika", "Delia", "Joy", "May"),
    Question("Team Rocket üyelerinden biri olmayan kimdir?", 2, "Jessie", "James", "Brock", "Meowth"),
    Question("Ash’in ilk yol arkadaşı kimdir?", 1, "Gary", "Misty", "May", "Serena"),
    Question("Profesör Oak hangi konuda uzmandır?", 0, "Pokémon araştırmaları", "Gym savaşları", "Pokéball üretimi", "Moda"),
    Question("Pokémon dünyasındaki para birimi nedir?", 1, "Yen", "PokéDolar", "Altın", "Token"),
    Question("Pokémon yumurtaları genellikle nasıl bulunur?", 2, "Savaşta", "PokéMart’ta", "Yetiştiricilerde", "Ligde"),
    Question("Ash’in Alola bölgesindeki Pokémonlarından biri kimdir?", 0, "Rowlet", "Totodile", "Chimchar", "Grookey"),
    Question("Pokémon’un türünü ne belirler?", 1, "Seviyesi", "DNA’sı", "Eğitmeni", "Yaşadığı bölge"),
    Question("Kanto bölgesinde kaç Gym vardır?", 2, "6", "7", "8", "9"),
    Question("Ash’in Charizard’ı neden onu dinlememişti?", 0, "Çok kibirliydi", "Küsmüştü", "Hasta olmuştu", "Saldırı öğrenmemişti"),
    Question("Pokémon ‘Shiny’ formu ne demektir?", 3, "Dev form", "Mega evrim", "Gizli güç", "Farklı renkli form"),
    Question("Pokémon oyunlarında ‘Starter Pokémon’ neyi ifade eder?", 1, "Yedek Pokémon", "Başlangıç Pokémon’u", "Efsanevi Pokémon", "Rakip Pokémon’u"),
    Question("Su tipi Pokémon’lara karşı hangi tip avantajlıdır?", 2, "Kaya", "Yer", "Bitki", "Çelik"),
    Question("Ash’in Pikachu’su Raichu olmayı neden reddetmiştir?", 0, "Kendi kimliğini korumak istemiştir", "Taş kırılmıştır", "Oak izin vermemiştir", "Ash istememiştir"),
    Question("Pokémon savaşlarında hangi hareket türü vardır?", 1, "Karmaşık", "Fiziksel", "Yazılı", "Sesli"),
    Question("Pokémon evrenindeki efsanevi kuşlardan biri kimdir?", 0, "Articuno", "Pidgey", "Spearow", "Doduo"),
    Question("Pokémon oyunlarının sloganı nedir?", 2, "Hepsini eğit!", "Hepsini izle!", "Hepsini yakala!", "Hepsini kazan!"),
    Question("Pikachu’nun sevdiği yiyecek nedir?", 1, "Elma", "Ketchup", "Balık", "Çilek"),
    Question("Pokémon animesinde ‘Meowth’ neden konuşabilir?", 2, "Büyü yaptı", "İnsan oldu", "Kendi kendine konuşmayı öğrendi", "Bilgisayara bağlandı"),
    Question("Ash hangi şehirden gelir?", 0, "Pallet Town", "Cerulean City", "Viridian City", "Saffron City"),
    Question("Pokémon filmlerinde sıkça görülen efsanevi Pokémon kimdir?", 3, "Zubat", "Mewtwo", "Lucario", "Mewtwo"),
    Question("Ash’in ilk yakaladığı vahşi Pokémon kimdir?", 1, "Caterpie", "Caterpie", "Weedle", "Pidgeotto"),
    Question("Pokémon dünyasında 'Legendary' ne anlama gelir?", 0, "Efsanevi Pokémon", "Yeni başlayan Pokémon", "Süper taş", "Düşük seviyeli Pokémon"),
    Question("Pikachu’nun ön evrimi kimdir?", 2, "Raichu", "Plusle", "Pichu", "Minun"),
    Question("Ash’in Kanto’daki su Pokémon’u kimdir?", 0, "Squirtle", "Poliwag", "Lapras", "Totodile"),
    Question("Pokémon evrimini engellemek için ne yapılır?", 3, "Savaşılır", "Taş atılır", "Yumurtlatılır", "B tuşuna basılır"),
    Question("Pokémon Go hangi yılda çıktı?", 1, "2014", "2016", "2018", "2020"),
    Question("Efsanevi Pokémonlardan biri olmayan hangisidir?", 0, "Snorlax", "Mew", "Zapdos", "Lugia"),
    Question("Ash’in en çok kullandığı cümlelerden biri nedir?", 2, "Pes edelim!", "Eve dönelim!", "Hepsini yakalayacağım!", "Yavaş gidelim!"),
    Question("Pokémon savaşında 'HP' neyi gösterir?", 0, "Can puanı", "Deneyim", "Güç", "Zorluk"),
    Question("Pokémon 'EXP' nedir?", 3, "Enerji", "Saldırı", "Evrim", "Deneyim puanı"),
    Question("Pokémon evrim taşlarından biri olmayan hangisidir?", 2, "Ateş Taşı", "Su Taşı", "Renk Taşı", "Yıldırım Taşı"),
    Question("Ash’in Unova Pokémonlarından biri kimdir?", 1, "Totodile", "Oshawott", "Charmander", "Mudkip"),
    Question("Pokémon oyunlarında 'TM' ne işe yarar?", 3, "Evrim sağlar", "Pokémon yakalar", "Gizli güç verir", "Pokémon’a hareket öğretir"),
    Question("‘Ditto’ hangi özelliğiyle bilinir?", 0, "Diğer Pokémon’lara dönüşebilmesi", "Görünmez olması", "Taş yemesi", "Zamanı durdurması"),
    Question("Pokémon dünyasında 'Elite Four' nedir?", 2, "Efsanevi grup", "Araştırma takımı", "En güçlü dört eğitmen", "Pokémon Ligi taşları"),
    Question("Ash’in ‘Greninja’sının özel formu nedir?", 3, "Mega Greninja", "Super Greninja", "Dark Greninja", "Ash-Greninja"),
    Question("Pokémon ‘Mega Evolution’ özelliği hangi nesilde tanıtıldı?", 1, "5. nesil", "6. nesil", "7. nesil", "8. nesil"),
    Question("Pokémonların uyum içinde yaşadığı bölge hangisidir?", 2, "Johto", "Hoenn", "Alola", "Unova"),
    Question("‘Legendary Birds’ hangi üç Pokémon’dan oluşur?", 0, "Articuno, Zapdos, Moltres", "Lugia, Ho-Oh, Latias", "Mew, Mewtwo, Celebi", "Regi üçlüsü"),
    Question("Pokémon evrenindeki ilk efsanevi Pokémon hangisidir?", 3, "Zapdos", "Lugia", "Celebi", "Mew"),
    Question("‘Pokémon Stadium’ hangi platformda çıkmıştır?", 1, "Game Boy", "Nintendo 64", "DS", "Switch"),
    Question("‘Pokémon Sword and Shield’ hangi bölgede geçer?", 2, "Alola", "Unova", "Galar", "Kalos"),
    Question("Ash kaç yaşındadır?", 0, "10", "12", "13", "15"),
    Question("‘Pokémon’ kelimesi hangi iki kelimenin birleşimidir?", 3, "Pocket + Toy", "Power + Monster", "Pocket + Pet", "Pocket + Monster"),
    Question("Pokémon oyunlarındaki rakip karakterin klasik ismi nedir?", 1, "James", "Blue", "Silver", "Hop"),
    Question("Ash’in Kanto’daki uçan Pokémon’u kimdir?", 2, "Zapdos", "Articuno", "Pidgeot", "Staraptor"),
    Question("Pokémon oyunlarında ‘HM’ ne işe yarar?", 0, "Özel hareket öğretir (örneğin Surf)", "Pokémon çağırır", "Savaş başlatır", "Kayıt açar"),
    Question("Ash’in Kalos Pokémonlarından biri kimdir?", 2, "Totodile", "Cyndaquil", "Froakie", "Turtwig"),
    Question("Pokémon oyunlarında bitkisel Pokémon tipi hangisidir?", 3, "Ground", "Fairy", "Bug", "Grass"),
    Question("Pokémonların yakalandığı aletin adı nedir?", 0, "Pokéball", "GreatBox", "MonsterDisk", "CaptureCube"),
    Question("‘Pokémon Yellow’ oyunu hangi Pokémon’a odaklanır?", 1, "Charmander", "Pikachu", "Bulbasaur", "Meowth"),
    Question("‘Pokémon Snap’ oyununda amaç nedir?", 3, "Savaşmak", "Pokémon yakalamak", "Eğitmen olmak", "Fotoğraf çekmek"),
    Question("Pokémonlar hangi dilde kendi isimlerini söyler?", 2, "İngilizce", "Japonca", "Kendi isimleriyle", "Sembollerle"),
    Question("Ash’in Kanto’daki çim Pokémon’u kimdir?", 0, "Bulbasaur", "Treecko", "Chikorita", "Turtwig"),
    Question("Pokémon dünyasındaki en büyük yaratıklardan biri kimdir?", 2, "Gyarados", "Snorlax", "Wailord", "Steelix"),
    Question("Pokémon savaşlarında ‘Critical Hit’ ne demektir?", 1, "Başarısız saldırı", "Ekstra güçlü vuruş", "Yan etki", "Savunma düşüşü"),
    Question("Pokémon’un doğduğu yer genelde neresidir?", 0, "Yumurta", "Deniz", "Mağara", "Pokéball"),
    Question("Ash’in Pokémon Ligi’ni kazandığı bölge hangisidir?", 3, "Kanto", "Johto", "Sinnoh", "Alola"),
    Question("Pokémon oyunlarında kullanılan bisikletin amacı nedir?", 1, "Dekor", "Hızlı seyahat", "Saldırı", "Pokémon taşıma"),
    Question("Pokémon oyunlarındaki ana hedef nedir?", 2, "Zengin olmak", "Dost bulmak", "Tüm Pokémonları yakalamak", "Gym kurmak"),
    Question("‘Pokémon Scarlet and Violet’ hangi bölgeyi temel alır?", 0, "Paldea", "Sinnoh", "Johto", "Kalos"),
    Question("Pokémon dünyasında ‘Shiny Charm’ ne işe yarar?", 1, "Seviyeyi artırır", "Shiny yakalama şansını artırır", "Hız kazandırır", "Deneyim puanı verir"),
    Question("Ash’in Galar Pokémonlarından biri kimdir?", 2, "Piplup", "Rowlet", "Dracovish", "Totodile"),
    Question("Pokémon evriminde kullanılan taşlardan biri olmayan hangisidir?", 3, "Thunder Stone", "Fire Stone", "Water Stone", "Iron Stone"),
    Question("‘Pokémon Legends: Arceus’ hangi Pokémon’a odaklanır?", 0, "Arceus", "Dialga", "Palkia", "Darkrai"),
    Question("‘Pokémon’un yaratıcısı kimdir?", 2, "Shigeru Miyamoto", "Satoshi Kon", "Satoshi Tajiri", "Ken Sugimori"),
    Question("‘Pokémon Center’larda Pokémon’ları kim iyileştirir?", 1, "Profesör Oak", "Hemşire Joy", "Officer Jenny", "Delia"),
    Question("‘Pokémon Battle Frontier’ nedir?", 0, "Zorlu savaş meydanları serisi", "Efsanevi Pokémon yuvası", "Yeni şehir", "Pokéball laboratuvarı"),
    Question("Pokémon filmlerinde ‘Lucario’ hangi Pokémon’la bağ kurar?", 3, "Ash", "Misty", "Brock", "Sir Aaron"),
    Question("Pokémon dünyasında ‘Efsanevi Üçlü Köpekler’ kimlerdir?", 2, "Mew, Mewtwo, Celebi", "Zapdos, Moltres, Articuno", "Raikou, Entei, Suicune", "Lugia, Ho-Oh, Celebi"),
    Question("‘Pokémon’ animesinin Japonca orijinal adı nedir?", 1, "Pocket Friends", "Pocket Monsters", "PikaShow", "Monster World")
]

random.shuffle(quiz_questions)


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
            self.name = (await self.get_name()).capitalize()
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
        if not hasattr(self, 'last_feed_epoch'):
            self.last_feed_epoch = 0

        now = asyncio.get_event_loop().time()
        elapsed = now - self.last_feed_epoch

        if elapsed < feed_interval:
            return f"{self.name}'i tekrar beslemek için {round(feed_interval - elapsed, 1)} saniye beklemelisin⏳"

        self.hp += hp_increase
        self.last_feed_time = datetime.now()
        self.last_feed_epoch = now
        return f"{self.name} iyileşti. Mevcut sağlık: {self.hp}"

class Fighter(Pokemon):
    async def info(self):
        base_info = await super().info()
        return base_info + f"\n✨ Özel Güç bonusuyla extra hasar"
    async def feed(self, feed_interval=20, hp_increase=10):
        hp_increase += random.randint(1, 20)
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
        return base_info + "\n🛡️ %25 ihtimalle sıfır hasar alma"
    async def feed(self, feed_interval=20, hp_increase=10):
        feed_interval -= random.randint(1, 15)
        return await super().feed(feed_interval, hp_increase)

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
                await asyncio.sleep(2)
            print()
            cevap = input("🔁 Tekrar başlatmak için q yaz: ")
            if cevap.lower() != "q":
                break
            oyun += 1

    asyncio.run(deneme())