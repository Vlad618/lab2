import os
import django
import random
from PIL import Image, ImageDraw, ImageFont

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from main.models import Game, Category, ModAuthor, Mod
from django.core.files import File
from io import BytesIO

def create_placeholder_image(text, filename):
    # Create a colorful gradient-like placeholder
    width, height = 800, 450
    color1 = (random.randint(0, 100), random.randint(0, 100), random.randint(150, 255))
    color2 = (random.randint(0, 50), random.randint(0, 50), random.randint(50, 150))
    
    image = Image.new('RGB', (width, height), color1)
    draw = ImageDraw.Draw(image)
    
    # Simple pattern
    for i in range(0, width, 20):
        draw.line([(i, 0), (width - i, height)], fill=color2, width=1)
    
    # Add text (using default font since we might not have custom ones easily accessible)
    draw.text((width//2 - 50, height//2), text, fill=(255, 255, 255))
    
    temp_thumb = BytesIO()
    image.save(temp_thumb, 'JPEG')
    temp_thumb.seek(0)
    return temp_thumb

def populate():
    print("Clearing old data...")
    Mod.objects.all().delete()
    Game.objects.all().delete()
    Category.objects.all().delete()
    ModAuthor.objects.all().delete()

    print("Creating Games...")
    witcher = Game.objects.create(name="The Witcher 3: Wild Hunt", genre="RPG")
    skyrim = Game.objects.create(name="TES V: Skyrim", genre="RPG")
    minecraft = Game.objects.create(name="Minecraft", genre="Sandbox")
    cyberpunk = Game.objects.create(name="Cyberpunk 2077", genre="Action RPG")
    gtav = Game.objects.create(name="Grand Theft Auto V", genre="Action")

    print("Creating Categories...")
    cats = {
        "graphics": Category.objects.create(name="Графіка"),
        "gameplay": Category.objects.create(name="Геймплей"),
        "quests": Category.objects.create(name="Квести"),
        "characters": Category.objects.create(name="Персонажі"),
        "weapons": Category.objects.create(name="Зброя"),
        "tools": Category.objects.create(name="Інструменти")
    }

    print("Creating Authors...")
    authors = [
        ModAuthor.objects.create(name="MasterModder", experience=10),
        ModAuthor.objects.create(name="VisualArtist", experience=5),
        ModAuthor.objects.create(name="ScriptKing", experience=8),
        ModAuthor.objects.create(name="CyberWizard", experience=3),
    ]

    mods_data = [
        {
            "name": "The Witcher 3 HD Reworked Project",
            "desc": "Найкращий графічний мод для Відьмака 3, що оновлює текстури до 4K якості.",
            "price": 0.00,
            "game": witcher,
            "cat": cats["graphics"],
            "author": authors[1]
        },
        {
            "name": "Combat Evolved",
            "desc": "Повне переосмислення бойової системи: нові анімації, складніші вороги та баланс.",
            "price": 150.00,
            "game": witcher,
            "cat": cats["gameplay"],
            "author": authors[0]
        },
        {
            "name": "SkyUI",
            "desc": "Повне оновлення інтерфейсу Skyrim для зручного керування інвентарем на ПК.",
            "price": 0.00,
            "game": skyrim,
            "cat": cats["tools"],
            "author": authors[2]
        },
        {
            "name": "Beyond Skyrim: Bruma",
            "desc": "Величезне доповнення, що дозволяє відвідати місто Брума в провінції Сіроділ.",
            "price": 450.00,
            "game": skyrim,
            "cat": cats["quests"],
            "author": authors[0]
        },
        {
            "name": "Optifine HD",
            "desc": "Оптимізація графіки та підтримка шейдерів для Minecraft.",
            "price": 0.00,
            "game": minecraft,
            "cat": cats["graphics"],
            "author": authors[2]
        },
        {
            "name": "The Twilight Forest",
            "desc": "Новий вимір з власними босами, данжами та унікальними предметами.",
            "price": 200.00,
            "game": minecraft,
            "cat": cats["quests"],
            "author": authors[0]
        },
        {
            "name": "Better Vehicle Handling",
            "desc": "Виправляє фізику автомобілів у Найт-Сіті, роблячи керування більш реалістичним.",
            "price": 80.00,
            "game": cyberpunk,
            "cat": cats["gameplay"],
            "author": authors[3]
        },
        {
            "name": "Appearance Change Unlocker",
            "desc": "Дозволяє змінювати зовнішність персонажа в будь-який момент гри.",
            "price": 40.00,
            "game": cyberpunk,
            "cat": cats["characters"],
            "author": authors[3]
        },
        {
            "name": "LSPD First Response",
            "desc": "Станьте офіцером поліції в Лос-Сантосі: патрулювання, арешти та погоні.",
            "price": 300.00,
            "game": gtav,
            "cat": cats["gameplay"],
            "author": authors[0]
        },
        {
            "name": "NaturalVision Evolved",
            "desc": "Найбільш реалістичний графічний мод для GTA V з підтримкою трасування променів.",
            "price": 500.00,
            "game": gtav,
            "cat": cats["graphics"],
            "author": authors[1]
        },
        {
            "name": "Medieval Weapon Pack",
            "desc": "Набір з 20 реалістичних середньовічних мечів та сокир.",
            "price": 120.00,
            "game": skyrim,
            "cat": cats["weapons"],
            "author": authors[1]
        },
        {
            "name": "Ciri Playable Character",
            "desc": "Можливість пройти всю гру Skyrim у ролі Цірі з Відьмака.",
            "price": 180.00,
            "game": skyrim,
            "cat": cats["characters"],
            "author": authors[2]
        }
    ]

    for m in mods_data:
        mod = Mod(
            name=m["name"],
            description=m["desc"],
            price=m["price"],
            game=m["game"],
            category=m["cat"],
            author=m["author"]
        )
        
        # Generate placeholder image
        img_io = create_placeholder_image(m["name"], f"{mod.name}.jpg")
        mod.image.save(f"{m['name'].replace(' ', '_')}.jpg", File(img_io), save=False)
        mod.save()
        print(f"Added: {mod.name}")

if __name__ == '__main__':
    populate()
    print("Database successfully populated!")
