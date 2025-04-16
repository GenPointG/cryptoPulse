import requests
from bs4 import BeautifulSoup
from telegram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random
from translate import Translator

# Конфигурация
translator = Translator(to_lang="ru")
BOT_TOKEN = "7036075412:AAH9wdxG29_nVCMPW4uewPkRzhAc7Ao-ze8"  # @CriptoScientist_bot
CHANNEL_ID = "@CryptoPulse_666"
PRICE_DATABASE_FILE = "price_database.txt"  # Текстовый файл для хранения цен
GRAPH_FILE = "price_graph.png"  # Файл для сохранения основного графика
BTC_GRAPH_FILE = "btc_graph.png"  # Файл для графика Bitcoin
ETH_GRAPH_FILE = "eth_graph.png"  # Файл для графика Ethereum
NEWS_DATABASE_FILE = "news_database.txt"  # Текстовый файл для хранения ссылок на новости

# CoinGecko API для получения цен
def get_crypto_prices():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin,ethereum",
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Ошибка при получении цен: {e}")
        return None

# Чтение предыдущих цен из базы данных
def load_price_database():
    try:
        with open(PRICE_DATABASE_FILE, "r") as file:
            lines = file.readlines()
            if len(lines) >= 2:
                btc_price = float(lines[0].strip())
                eth_price = float(lines[1].strip())
                return btc_price, eth_price
            else:
                return None, None
    except FileNotFoundError:
        return None, None

# Сохранение текущих цен в базу данных
def save_price_database(btc_price, eth_price):
    try:
        with open(PRICE_DATABASE_FILE, "w") as file:
            file.write(f"{btc_price}\n{eth_price}")
    except Exception as e:
        print(f"Ошибка при записи цен в базу данных: {e}")

# Генерация данных для графика
def generate_prices_history():
    now = datetime.now()

    # Генерация временных меток с интервалом 1 час за последние 24 часа
    timestamps = [(now - timedelta(hours=i)).strftime("%H:%M") for i in range(24)]
    timestamps.reverse()

    # Пример данных для цен Bitcoin и Ethereum
    btc_prices = [generate_random_price(30000, 50000) for _ in range(24)]
    eth_prices = [generate_random_price(1500, 3000) for _ in range(24)]

    return {
        "timestamps": timestamps,
        "btc_prices": btc_prices,
        "eth_prices": eth_prices
    }

# Генерация случайной цены в заданном диапазоне
def generate_random_price(min_price, max_price):
    return round(random.uniform(min_price, max_price), 2)

# Создание основного графика изменения цен
def create_price_graph(prices_history):
    try:
        plt.style.use('dark_background')

        plt.figure(figsize=(10, 6))

        # Увеличиваем шкалу на 10,000 для лучшей видимости
        max_price = max(max(prices_history["btc_prices"]), max(prices_history["eth_prices"])) + 10000
        min_price = min(min(prices_history["btc_prices"]), min(prices_history["eth_prices"])) - 10000

        # Рисуем линии для Bitcoin и Ethereum
        plt.plot(
            prices_history["timestamps"],
            prices_history["btc_prices"],
            label="Bitcoin (BTC)",
            color="gold",  # Золотой цвет для Bitcoin
            linewidth=2.5
        )
        plt.plot(
            prices_history["timestamps"],
            prices_history["eth_prices"],
            label="Ethereum (ETH)",
            color="purple",  # Фиолетовый цвет для Ethereum
            linewidth=2.5
        )

        # Настройка заголовка и меток
        plt.title("Динамика цен BTC и ETH за последние 24 часа", fontsize=16, color="white")
        plt.xlabel("Время", fontsize=12, color="white")
        plt.ylabel("Цена (USD)", fontsize=12, color="white")

        # Настройка легенды и сетки
        plt.legend(fontsize=10, loc="upper left", frameon=False)
        plt.grid(color="#444444", linestyle="--", linewidth=0.5)

        # Настройка формата временной шкалы
        plt.xticks(rotation=45, fontsize=8, color="white")
        plt.ylim(min_price, max_price)

        # Сохраняем график
        plt.tight_layout()
        plt.savefig(GRAPH_FILE)
        plt.close()
    except Exception as e:
        print(f"Ошибка при создании графика: {e}")

# Создание графика для Bitcoin
def create_btc_graph(prices_history):
    try:
        plt.style.use('dark_background')

        plt.figure(figsize=(10, 6))

        # Увеличиваем шкалу на 10,000 для лучшей видимости
        max_price = max(prices_history["btc_prices"]) + 10000
        min_price = min(prices_history["btc_prices"]) - 10000

        # Рисуем линию для Bitcoin
        plt.plot(
            prices_history["timestamps"],
            prices_history["btc_prices"],
            label="Bitcoin (BTC)",
            color="gold",  # Золотой цвет для Bitcoin
            linewidth=2.5
        )

        # Настройка заголовка и меток
        plt.title("Динамика цены Bitcoin за последние 24 часа", fontsize=16, color="white")
        plt.xlabel("Время", fontsize=12, color="white")
        plt.ylabel("Цена (USD)", fontsize=12, color="white")

        # Настройка легенды и сетки
        plt.legend(fontsize=10, loc="upper left", frameon=False)
        plt.grid(color="#444444", linestyle="--", linewidth=0.5)

        # Настройка формата временной шкалы
        plt.xticks(rotation=45, fontsize=8, color="white")
        plt.ylim(min_price, max_price)

        # Сохраняем график
        plt.tight_layout()
        plt.savefig(BTC_GRAPH_FILE)
        plt.close()
    except Exception as e:
        print(f"Ошибка при создании графика Bitcoin: {e}")

# Создание графика для Ethereum
def create_eth_graph(prices_history):
    try:
        plt.style.use('dark_background')

        plt.figure(figsize=(10, 6))

        # Увеличиваем шкалу на 10,000 для лучшей видимости
        max_price = max(prices_history["eth_prices"]) + 10000
        min_price = min(prices_history["eth_prices"]) - 10000

        # Рисуем линию для Ethereum
        plt.plot(
            prices_history["timestamps"],
            prices_history["eth_prices"],
            label="Ethereum (ETH)",
            color="purple",  # Фиолетовый цвет для Ethereum
            linewidth=2.5
        )

        # Настройка заголовка и меток
        plt.title("Динамика цены Ethereum за последние 24 часа", fontsize=16, color="white")
        plt.xlabel("Время", fontsize=12, color="white")
        plt.ylabel("Цена (USD)", fontsize=12, color="white")

        # Настройка легенды и сетки
        plt.legend(fontsize=10, loc="upper left", frameon=False)
        plt.grid(color="#444444", linestyle="--", linewidth=0.5)

        # Настройка формата временной шкалы
        plt.xticks(rotation=45, fontsize=8, color="white")
        plt.ylim(min_price, max_price)

        # Сохраняем график
        plt.tight_layout()
        plt.savefig(ETH_GRAPH_FILE)
        plt.close()
    except Exception as e:
        print(f"Ошибка при создании графика Ethereum: {e}")

# Парсинг новостей с сайта
def parse_crypto_news():
    try:
        url = "https://coinmarketcap.com/headlines/news/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        news_list = []
        articles = soup.find_all("div", class_="infinite-scroll-component")
        for article in articles:
            title = '<b>'
            title += translator.translate(article.find('a', class_='sc-71024e3e-0 kNLySu cmc-link').text.strip()) if article.find('a', class_='sc-71024e3e-0 kNLySu cmc-link') else "Нет заголовка"
            title += '</b>\n\n<i>'
            title += translator.translate(article.find('p', class_='sc-71024e3e-0 iTULwH').text.strip()) if article.find('p', class_='sc-71024e3e-0 iTULwH') else "Нет заголовка"
            link = article.find("a")["href"] if article.find("a") else "Нет ссылки"
            full_link = f"https://coinmarketcap.com{link}" if link.startswith("/") else link
            news_list.append({"title": title, "link": full_link})
        return news_list
    except Exception as e:
        print(f"Ошибка при парсинге новостей: {e}")
        return []

# Чтение ссылок из базы данных
def load_news_database():
    try:
        with open(NEWS_DATABASE_FILE, "r") as file:
            return set(line.strip() for line in file)
    except FileNotFoundError:
        return set()

# Сохранение ссылок в базу данных
def save_news_database(links):
    try:
        with open(NEWS_DATABASE_FILE, "w") as file:
            file.write("\n".join(links))
    except Exception as e:
        print(f"Ошибка при записи в базу данных: {e}")

# Отправка одной новости
async def send_single_news():
    bot = Bot(token=BOT_TOKEN)
    try:
        existing_links = load_news_database()
        news = parse_crypto_news()
        new_news = []

        for n in news:
            if n["link"] not in existing_links:
                new_news.append(n)
                existing_links.add(n["link"])

        save_news_database(existing_links)

        if new_news:
            single_news = new_news[0]
            message = f"📰 <b><i>Крипто-новость:</i></b>\n ⚡️  {single_news['title']}</i>\n<a href ='{single_news['link']}'>Читать подробнее...</a>"
            await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='HTML')
        else:
            print("Новых новостей нет.")
    except Exception as e:
        print(f"Ошибка при отправке новости: {e}")

# Утренний пост с ценами и графиками
async def morning_post():
    bot = Bot(token=BOT_TOKEN)
    try:
        prices = get_crypto_prices()
        if not prices:
            await bot.send_message(chat_id=CHANNEL_ID, text="Не удалось получить цены на криптовалюты.")
            return

        btc_price = prices["bitcoin"]["usd"]
        eth_price = prices["ethereum"]["usd"]
        btc_change = prices["bitcoin"]["usd_24h_change"]
        eth_change = prices["ethereum"]["usd_24h_change"]

        prev_btc_price, prev_eth_price = load_price_database()
        save_price_database(btc_price, eth_price)

        # Генерация данных для графиков
        prices_history = generate_prices_history()

        # Создание графиков
        create_price_graph(prices_history)
        create_btc_graph(prices_history)
        create_eth_graph(prices_history)

        # Формирование сообщения
        message = (
            f"📈 Утренний обзор крипторынка:\n"
            f"- Bitcoin (BTC): ${btc_price} ({'+' if btc_change > 0 else ''}{btc_change:.2f}%)\n"
            f"- Ethereum (ETH): ${eth_price} ({'+' if eth_change > 0 else ''}{eth_change:.2f}%)\n\n"
            f"📊 Графики изменения цен за последние 24 часа:"
        )

        # Отправка сообщения и графиков
        await bot.send_message(chat_id=CHANNEL_ID, text=message)
        await bot.send_photo(chat_id=CHANNEL_ID, photo=open(GRAPH_FILE, "rb"), caption="Общий график BTC и ETH")
        #await bot.send_photo(chat_id=CHANNEL_ID, photo=open(BTC_GRAPH_FILE, "rb"), caption="График Bitcoin (BTC)")
        #await bot.send_photo(chat_id=CHANNEL_ID, photo=open(ETH_GRAPH_FILE, "rb"), caption="График Ethereum (ETH)")
    except Exception as e:
        print(f"Ошибка при отправке утреннего поста: {e}")

# Запуск планировщика задач
async def start_scheduler():
    scheduler = AsyncIOScheduler()

    # Ежедневный утренний пост в 9:00
    scheduler.add_job(morning_post, "cron", hour=9, minute=0)

    # Отправка одной новости каждые 6 часов
    scheduler.add_job(send_single_news, "interval", hours=3)

    scheduler.start()
    print("Планировщик запущен. Нажмите Ctrl+C для завершения.")

    # Бесконечный цикл для работы планировщика
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("Планировщик остановлен.")

if __name__ == "__main__":
    # Запуск асинхронного планировщика
    asyncio.run(start_scheduler())