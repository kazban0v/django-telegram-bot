import sys
import os
import django
import telebot
from myproject.catalog.models import Product

# Добавление пути проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')  # Замените 'myproject' на имя вашего проекта
django.setup()

# Токен Telegram-бота
TOKEN = "7937515092:AAF2FhDyBOG_g4KqsrehJzENOB9joTbPhbg"  # Замените на токен вашего бота
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "Привет! Я бот для управления товарами.\n"
                          "Доступные команды:\n"
                          "/list_products - Список товаров\n"
                          "/product <id> - Информация о товаре\n"
                          "/add_product <название> <цена> <количество> - Добавить товар")

@bot.message_handler(commands=['list_products'])
def list_products(message):
    products = Product.objects.all()
    if products.exists():
        response = "\n".join([f"{p.id}: {p.name} - {p.price}₽ ({p.quantity} шт.)" for p in products])
    else:
        response = "Товаров пока нет в базе данных."
    bot.reply_to(message, response)

@bot.message_handler(commands=['product'])
def product_detail(message):
    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "Укажите ID товара: /product <id>")
            return
        product_id = int(args[1])
        product = Product.objects.get(id=product_id)
        response = (
            f"Название: {product.name}\n"
            f"Цена: {product.price}₽\n"
            f"Количество: {product.quantity} шт.\n"
            f"Дата добавления: {product.create_data.strftime('%Y-%m-%d %H:%M:%S')}"
        )
    except Product.DoesNotExist:
        response = "Товар с указанным ID не найден."
    except ValueError:
        response = "ID должен быть числом."
    bot.reply_to(message, response)

@bot.message_handler(commands=['add_product'])
def add_product(message):
    try:
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            bot.reply_to(message, "Использование: /add_product <название> <цена> <количество>")
            return
        data = args[1].split()
        if len(data) < 3:
            bot.reply_to(message, "Укажите все данные: название, цена, количество.")
            return
        name, price, quantity = data[0], float(data[1]), int(data[2])
        product = Product.objects.create(name=name, price=price, quantity=quantity)
        bot.reply_to(message, f"Товар '{product.name}' успешно добавлен в базу данных!")
    except ValueError:
        bot.reply_to(message, "Ошибка в данных. Убедитесь, что цена и количество введены корректно.")
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
