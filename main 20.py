import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Токен вашего бота
TOKEN = '7992067256:AAGwVmfRSKrU9zMFAThanaPOUF-cF5dIpN0'

# ID чата для сообщений
CHAT_ID = -1002339077130

# Создаём экземпляр бота
bot = telebot.TeleBot(TOKEN)

# Хранилище ID сообщений для удаления
bot_data = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()

    # Добавление кнопки "Услуги"
    button1 = InlineKeyboardButton("🔧 Услуги", callback_data="services")
    markup.add(button1)

    # Добавление кнопок "Отзывы" и "Связь"
    row2 = [
        InlineKeyboardButton("⭐ Отзывы", url="https://t.me/KwokzsReviews"),
        InlineKeyboardButton("📞 Связь", url="https://t.me/kwokzs")
    ]
    markup.add(*row2)

    # Добавление кнопки "Обратиться"
    button3 = InlineKeyboardButton("✉️ Обратиться", callback_data="contact")
    markup.add(button3)

    with open('welcome_image.jpg', 'rb') as photo_file:
        sent_message = bot.send_photo(
            message.chat.id,
            photo_file,
            caption="*Добро пожаловать в официального бота Квукза!* \n\n"
                    "_Здесь вы сможете ознакомиться с услугами Квукза. "
                    "Для просмотра доступных предложений используйте кнопки ниже._",
            parse_mode='Markdown',
            reply_markup=markup
        )

        bot_data[message.chat.id] = sent_message.message_id

# Обработчик нажатия на кнопку "Обратиться"
@bot.callback_query_handler(func=lambda call: call.data == "contact")
def contact_request(call):
    chat_id = call.message.chat.id

    if chat_id in bot_data:
        try:
            bot.delete_message(chat_id, bot_data[chat_id])
        except:
            pass  

    # Запросить у пользователя сообщение
    msg = bot.send_message(
        chat_id,
        "Пожалуйста, напишите, что вас интересует или с каким вопросом вы хотите обратиться."
    )

    # Сохраняем информацию о том, что теперь ожидаем сообщение от пользователя
    bot_data[chat_id] = msg.message_id

    # Обработчик для получения сообщения пользователя
    @bot.message_handler(func=lambda message: message.chat.id == chat_id)
    def handle_user_message(message):
        # Пересылаем сообщение в чат с нужным ID
        bot.forward_message(CHAT_ID, chat_id, message.message_id)

        # Отправляем сообщение о том, что запрос получен
        bot.send_message(chat_id, "Спасибо за ваше сообщение! Мы скоро с вами свяжемся.")

        # Удаляем исходное сообщение пользователя
        bot.delete_message(chat_id, message.message_id)

        # Удаляем сообщение с запросом
        bot.delete_message(chat_id, bot_data[chat_id])

        # Снимаем ожидание сообщения
        del bot_data[chat_id]

# Обработчик нажатия на кнопку "Услуги"
@bot.callback_query_handler(func=lambda call: call.data == "services")
def show_services(call):
    chat_id = call.message.chat.id

    if chat_id in bot_data:
        try:
            bot.delete_message(chat_id, bot_data[chat_id])
        except:
            pass  

    services_markup = InlineKeyboardMarkup(row_width=2)
    services_markup.add(
        InlineKeyboardButton("👮 Деф", callback_data="def"),
        InlineKeyboardButton("🛠 Сносер", callback_data="snoser"),
        InlineKeyboardButton("🔒 Приватка", callback_data="privatka"),
        InlineKeyboardButton("✏️ Эдит", callback_data="edit")
    )

    text = (
        "*Раздел услуг Квукза*\n\n"
        "Здесь представлены все актуальные предложения от *Квукза*. "
        "Ознакомьтесь с доступными вариантами и выберите подходящий.\n\n"
        "📌 *Для получения подробной информации* — воспользуйтесь кнопками ниже.\n\n"
        "Для получения подробной информации используйте кнопки ниже."
    )

    with open('services_image.jpg', 'rb') as photo_file:
        sent_message = bot.send_photo(
            chat_id,
            photo_file,
            caption=text,
            parse_mode="Markdown",
            reply_markup=services_markup
        )

    bot_data[chat_id] = sent_message.message_id

# Обработчик нажатия на кнопку "Сносер"
@bot.callback_query_handler(func=lambda call: call.data == "snoser")
def snoser_service(call):
    chat_id = call.message.chat.id

    if chat_id in bot_data:
        try:
            bot.delete_message(chat_id, bot_data[chat_id])
        except:
            pass  

    snoser_markup = InlineKeyboardMarkup()
    snoser_markup.add(InlineKeyboardButton("❌ Выйти", callback_data="exit"))
    snoser_markup.add(InlineKeyboardButton("💳 Оплатить", url="t.me/send?start=IVE1ZB5nFwFa"))  

    text = (
        "*Сносер для Telegram – навсегда за $6*\n\n"
        "Хочешь научиться сносить аккаунты в Telegram? Я предоставляю инструмент и полное обучение для сноса аккаунтов жертв, который работает до 3 лет от леги. С этим сносером ты сможешь безопасно и эффективно удалять аккаунты без следов.\n\n"
        "**Цена:** *$6 за доступ навсегда.*\n\n"
        "Что ты получаешь:\n"
        "- Рабочий сносер для Telegram, действующий до 3 лет от леги\n"
        "- Полное обучение, как пользоваться инструментом для успешного сноса\n"
        "- Доступ к инструкциям и материалам для сноса аккаунтов\n\n"
        "Как получить доступ:\n"
        "1. **Оплати услугу** (*$6*).\n"
        "2. После оплаты напиши [@kwokzs](https://t.me/kwokzs), и я отправлю тебе ссылку на сносер, обучение и все нужные материалы.\n"
        "3. Получи доступ навсегда и начинай использовать сносер.\n\n"
        "*Не пишите по мелочам до оплаты – все вопросы и детали можно обсудить только после получения доступа.*"
    )

    sent_message = bot.send_message(
        chat_id,
        text,
        parse_mode="Markdown",
        reply_markup=snoser_markup
    )

    bot_data[chat_id] = sent_message.message_id

# Обработчик нажатия на кнопку "Деф"
@bot.callback_query_handler(func=lambda call: call.data == "def")
def def_service(call):
    chat_id = call.message.chat.id

    if chat_id in bot_data:
        try:
            bot.delete_message(chat_id, bot_data[chat_id])
        except:
            pass  

    def_markup = InlineKeyboardMarkup()
    def_markup.add(InlineKeyboardButton("❌ Выйти", callback_data="exit"))
    def_markup.add(InlineKeyboardButton("💳 Оплатить", url="t.me/send?start=IVJ7z0kw29j4"))  

    text = (
        "*Деф от доксов и т.д. – защита навсегда за $8*\n\n"
        "Если тебя собираются доксить, угрожают сливом данных или хотят что-либо сделать, я возьму это на себя и дам тебе защиту. Это не временная мера — защита навсегда, никаких утечек и угроз не будет.\n\n"
        "**Цена:** *$8 за защиту.*\n\n"
        "Что входит:\n"
        "- **Защита от докса и деанона**\n"
        "- **Препятствование утечке личных данных**\n"
        "- **Остановка угроз и сливов**\n"
        "- **Защищаю твою личную информацию навсегда**\n\n"
        "Как заказать защиту:\n"
        "1. **Оплати услугу** (*$8*).\n"
        "2. **Напиши [@kwokzs](https://t.me/kwokzs)** с деталями угроз или атаки.\n"
        "3. Получи **защиту навсегда** и забудь об угрозах.\n\n"
        "*Не дефаю, если просто оскорбили или заскамили — защита только от реальных угроз, докса и деанона.*"
    )

    sent_message = bot.send_message(
        chat_id,
        text,
        parse_mode="Markdown",
        reply_markup=def_markup
    )

    bot_data[chat_id] = sent_message.message_id

# Обработчик нажатия на кнопку "Приватка"
@bot.callback_query_handler(func=lambda call: call.data == "privatka")
def privatka_service(call):
    chat_id = call.message.chat.id

    if chat_id in bot_data:
        try:
            bot.delete_message(chat_id, bot_data[chat_id])
        except:
            pass  

    privatka_markup = InlineKeyboardMarkup()
    privatka_markup.add(InlineKeyboardButton("❌ Выйти", callback_data="exit"))
    privatka_markup.add(InlineKeyboardButton("💳 Оплатить", url="t.me/send?start=IV0Dvo7bLkeY"))  

    text = (
        "*Приватка – $1*\n\n"
        "В приватке вы получите доступ к архиву старых софтов, сносов, мануалов и паспортов. Все материалы собраны для тех, кто ищет полезные ресурсы.\n\n"
        "**Цена:** *$1 за доступ.*\n\n"
        "Что вас ждет в приватке:\n"
        "- Старые версии софтов\n"
        "- Старые сносеры\n"
        "- Мануалы\n"
        "- Паспортные данные\n\n"
        "Как получить доступ:\n"
        "1. **Оплатите услугу** (*$1*).\n"
        "2. Напишите [@kwokzs](https://t.me/kwokzs), чтобы получить ссылку на материалы.\n"
        "3. Получите полный доступ к архиву и начните пользоваться ресурсами.\n\n"
        "*Не пишите до оплаты по мелочам.*"
    )

    sent_message = bot.send_message(
        chat_id,
        text,
        parse_mode="Markdown",
        reply_markup=privatka_markup
    )

    bot_data[chat_id] = sent_message.message_id

# Обработчик нажатия на кнопку "Эдит"
@bot.callback_query_handler(func=lambda call: call.data == "edit")
def edit_service(call):
    chat_id = call.message.chat.id

    if chat_id in bot_data:
        try:
            bot.delete_message(chat_id, bot_data[chat_id])
        except:
            pass  

    edit_markup = InlineKeyboardMarkup()
    edit_markup.add(InlineKeyboardButton("❌ Выйти", callback_data="exit"))
    edit_markup.add(InlineKeyboardButton("💳 Оплатить", url="t.me/send?start=IVOEJ4WMgGuo"))  

    text = (
        "*Редактирование контента – $2.50*\n\n"
        "После оплаты отправьте материалы (текст или изображение) [@kwokzs](https://t.me/kwokzs). Я быстро и качественно отредактирую их, исправлю ошибки или улучшу качество.\n\n"
        "**Цена:** *$2.50 за одну работу.*\n\n"
        "Как оформить заказ:\n"
        "1. Оплатите услугу.\n"
        "2. Напишите [@kwokzs](https://t.me/kwokzs) с материалами для редактирования.\n"
        "3. Получите готовую работу в кратчайшие сроки.\n\n"
        "*Не пишите до оплаты по мелочам.*"
    )

    sent_message = bot.send_message(
        chat_id,
        text,
        parse_mode="Markdown",
        reply_markup=edit_markup
    )

    bot_data[chat_id] = sent_message.message_id

# Обработчик нажатия на кнопку "Выйти"
@bot.callback_query_handler(func=lambda call: call.data == "exit")
def exit_to_services(call):
    show_services(call)  

bot.polling()
