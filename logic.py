from random import randint
import random
import requests
from datetime import datetime, timedelta

class Pokemon:
    pokemons = {}
    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):

        self.pokemon_trainer = pokemon_trainer   

        self.pokemon_number = randint(1,1000)
        self.img = self.get_img()
        self.name = self.get_name()
        self.first_ability = self.get_firstability()
        self.second_ability = self.get_secondability()

        self.level = 1          # уровень покемона
        self.satiety = 5        # сытость, максимум 10
        self.achievements = set()   # множество достижений покемона
        self.points = 0            # очки за победы покемона

        self.hp = randint(10,100)
        self.power = randint(3,30)
        self.last_feed_time = datetime.now()  # время последнего кормления
        
        Pokemon.pokemons[pokemon_trainer] = self

    # Метод для получения картинки покемона через API
    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['sprites']['other']['official-artwork']['front_default'])
        else:
            return "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png"
    
    # Метод для получения имени покемона через API
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['forms'][0]['name'])
        else:
            return "Pikachu"

    # Метод для получения названия 1-ой способности покемона через API
    def get_firstability(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['abilities'][0]['ability']['name']
        else:
            return "overgrow"

    def get_secondability(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            abilities = data['abilities']
            if len(abilities) > 1:
                return abilities[1]['ability']['name']
            else:
                return "Вторая способность отсутствует"
        else:
            return "unknown"

    def feed(self, feed_interval = 20, hp_increase = 10 ):
        current_time = datetime.now()  
        delta_time = timedelta(seconds=feed_interval)  
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Здоровье покемона увеличено. Текущее здоровье: {self.hp}"
        else:
            return f"Следующее время кормления покемона: {self.last_feed_time+delta_time}"

    def level_up(self):
        self.level += 1
        # Пример достижения на уровне 5
        if self.level == 5:
            self.achievements.add("Опытный тренер")
            print(f"{self.name} получил достижение 'Опытный тренер'!")

    def heal(self, amount=10):
        self.max_hp = 100  # Максимальное здоровье

        if self.hp == 0:
            return f"{self.name} не может быть вылечен — он выведен из боя!"
        self.hp += amount
        if self.hp > self.max_hp:  # Максимум HP
            self.hp = self.max_hp
        return f"{self.name} восстановил {amount} HP. Текущее здоровье: {self.hp}."

    def attack(self, enemy):
        if isinstance(enemy, Wizard): # Проверка на то, что enemy является типом данных Wizard (является экземпляром класса Волшебник)
            chance = randint(1,5)    
            if chance == 1:
                return "Покемон-волшебник применил щит в сражении"
            
        # Выполнение атаки
        if enemy.hp > self.power: 
            enemy.hp -= self.power
            result = f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}"
        else:
            enemy.hp = 0
            self.points += 1
            result = f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}!"

        # Восстановление здоровья после боя
        if self.hp > 0:
            result += "\n" + self.heal(10)
        if enemy.hp > 0:
            result += "\n" + enemy.heal(10)

        return result
        
    # Метод класса для получения информации
    def info(self):
        return f"Имя твоего покемона: {self.name} , значение здоровья: {self.hp}, значение силы: {self.power}, первая способность твоего покемона: {self.first_ability} , вторая способность твоего покемона: {self.second_ability} ."
        
    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img


class Wizard(Pokemon):
    def __init__(self, pokemon_trainer):    # Инициализация объекта (конструктор)
        super().__init__(pokemon_trainer)

        self.hp = random.randint(30,100)
        self.power = random.randint(3,15)

    def attack(self, enemy):
        return super().attack(enemy)

    def super(self, enemy):
        if isinstance(enemy, Fighter): # Проверка на то, что enemy является типом данных Fighter (является экземпляром класса Боец)
            chance = randint(1,5)    
            if chance == 1:
                return "Покемон-боец применил супер-атаку в сражении"
                
            else:
                self.attack(enemy)

        else:
            self.attack(enemy)

        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}"
        else:
            enemy.hp = 0
            self.points += 1
            return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}! "

    def feed(self):
        return super().feed(hp_increase=20)  # Увеличение сытости (здоровья)       

    def info(self):
        return 'У тебя покемон-волшебник!' + super().info()


class Fighter(Pokemon):
    def __init__(self, pokemon_trainer):    # Инициализация объекта (конструктор)
        super().__init__(pokemon_trainer)
            
        self.hp = random.randint(15,70)   # Инициализация атрибутов покемона-бойца
        self.power = random.randint(6,30)

    def attack(self, enemy):
        return super().attack(enemy)
        
    def super(self, enemy):
        self.super_power = random.randint(5,15)
        self.power += self.super_power
        result = super().attack(enemy)
        self.power -= self.super_power
        return result + f"\nБоец применил супер-атаку силой:{self.super_power} "

    def feed(self):
        return super().feed(hp_increase=20)  # Увеличение сытости (здоровья)
    
    def info(self):
        return 'У тебя покемон-боец!' + super().info()  

        
    

