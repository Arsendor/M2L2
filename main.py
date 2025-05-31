import telebot 
from random import randint
from config import token
from logic import Pokemon, Wizard, Fighter

bot = telebot.TeleBot(token) 


SUPER_POKEMON_CHANCE = 10  # 10% шанс получить супер-покемона

@bot.message_handler(commands=['go'])
def go(message):
    username = message.from_user.username
    if username not in Pokemon.pokemons:
        chance = randint(1, 100)
        if chance <= SUPER_POKEMON_CHANCE:
            # Получаем либо Wizard, либо Fighter
            if randint(0, 1) == 0:
                pokemon = Wizard(username)
            else:
                pokemon = Fighter(username)
            bot.send_message(message.chat.id, f"Тебе достался супер-покемон: {pokemon.name}!")
        else:
            pokemon = Pokemon(username)
            bot.send_message(message.chat.id, f"Тебе достался покемон: {pokemon.name}!")

        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")

@bot.message_handler(commands=['attack'])
def attack(message):
    # Проверяем, что команда отправлена в ответ на сообщение другого пользователя
    if not message.reply_to_message:
        bot.reply_to(message, "Чтобы атаковать, ответь командой /attack на сообщение противника.")
        return

    attacker = message.from_user.username
    defender = message.reply_to_message.from_user.username

    if attacker not in Pokemon.pokemons:
        bot.reply_to(message, "У тебя нет покемона, чтобы атаковать.")
        return

    if defender not in Pokemon.pokemons:
        bot.reply_to(message, "У противника нет покемона.")
        return

    attacker_pokemon = Pokemon.pokemons[attacker]
    defender_pokemon = Pokemon.pokemons[defender]

    result = attacker_pokemon.attack(defender_pokemon)

    # Восстановление здоровья после боя, если живы
    if attacker_pokemon.hp > 0:
        result += "\n" + attacker_pokemon.heal(10)
    if defender_pokemon.hp > 0:
        result += "\n" + defender_pokemon.heal(10)

    bot.send_message(message.chat.id, result)

@bot.message_handler(commands=['heal'])
def heal(message):
    username = message.from_user.username
    if username not in Pokemon.pokemons:
        bot.reply_to(message, "У тебя нет покемона, которого можно вылечить.")
        return

    pokemon = Pokemon.pokemons[username]
    result = pokemon.heal(10)
    bot.send_message(message.chat.id, result)

@bot.message_handler(commands=['info'])
def info(message):
    username = message.from_user.username
    if username in Pokemon.pokemons.keys():
        pok = Pokemon.pokemons[username]
        bot.send_message(message.chat.id, pok.info())
    else:
        bot.reply_to(message, "У тебя ещё нет покемона. Напиши /go, чтобы создать одного!")

@bot.message_handler(commands=['feed'])
def feed_pok(message):
    username = message.from_user.username
    if username in Pokemon.pokemons:
        result = Pokemon.pokemons[username].feed()
        bot.send_message(message.chat.id, result)
    else:
        bot.reply_to(message, "Сначала создай покемона командой /go")


bot.infinity_polling(none_stop=True)