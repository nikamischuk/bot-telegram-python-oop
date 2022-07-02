import random  # Для генерації випадковості питань
import datetime  # Для дати та часу складання тесту
import time  # Для обрахунку часу, за який було написано тест

import telebot
from telebot.types import ReplyKeyboardRemove
# import PyTelegramBotAPI


# Ініціалізуємо бота, передавши йому токен, який було отримано від BotFather
# (так як бот навчальний, то просто вставлено токен в сирому вигляді)
bot = telebot.TeleBot('5526919454:AAH9qgaFG7qoyaEe5CJYdyLxCn_pfPAgbMk')


class Question:
    """
    Клас, який реалізує сутність питання
    """
    def __init__(self, question, answer_options, right_id):
        """
        Конструктор екземпляру класу Question
        :param question: текст самого запитання
        :param answer_options: масив із 4х варіантів відповіді
        :param right_id: індекс правильного варіанту відповіді
        """
        self.question = question
        self.answer_options = answer_options
        self.right_id = right_id


# Створимо список із 10 запитань, в кожному з яких 4 варіанти відповіді
list_questions = [Question('Яка типізація використовується мовою Python?',
                           ['Статична', 'Динамічна', 'Локальна', 'Змішана'], 1),
                  Question('Як перетворити строку s = “SOME STRING” в “some string” ?',
                           ['s.char()', 's.upper()', 's.title()', 's.lower()'], 3),
                  Question('Яка інструкція використовується для примусової генерації винятків?',
                           ['raise', 'catch', 'break', 'except'], 0),
                  Question('Як дізнатись довжину рядка s = “Some string” ?',
                           ['s.length', 'len(s)', 's.len', 'length(s)'], 1),
                  Question('Методи, що не можуть змінювати ані стан класу, ані його примірників?',
                           ['Динамічні', 'Методи класу', 'Статичні', 'Методи примірника'], 2),
                  Question('Функція, за допомогою якої можна отримати список всіх атрибутів і методів певного класу?',
                           ['super()', 'str()', 'dir()', 'mro()'], 2),
                  Question('Принцип ООП, згідно з яким складнісь реалізації програмного компонента '
                           'повинна бути захована за його інтерфейсом',
                           ['Наслідування', 'Поліморфізм', 'Абстракція', 'Інкапсуляція'], 3),
                  Question('Який метод необхідно застосувати до списку, щоб в результаті утворилася строка з елементів '
                           'початкового списку через роздільник?',
                           ['join()', 'split()', 'filter()', 'format()'], 0),
                  Question('Яка функція використовується для перетворення Jinja2 шаблону '
                           'в html-сторінку у Flask-додатках?',
                           ['print_template()', 'render_template()', 'render_html()', 'print_html()'], 1),
                  Question("В якому об'єкті зберігаються значення між запитами окремого користувача до Flask-додатку?",
                           ['session', 'request', 'current_app', 'cookie'], 0)]

# Індекс в масиві поточного запитання
current_question_id = 0
# Індекс правильного варіанту відповіді в поточному екземплярі питання
current_right = list_questions[current_question_id].right_id
# Прапорець, який сигналізує про те чи надана користувачем відповідь на запитання
current_reply = False
# Лічильник, який рахує к-сть правильних відповідей
counter_right_answers = 0


# Функція, для генерації рандомної послідовності питань.
# В результаті отримуємо масив з 10 елементів, в якому випадково розміщені цифри від 0 до 9.
def generate_random_numbers():
    arr = []
    while len(arr) < 10:
        number = random.randint(0, 9)
        # Якщо згенероване число уже є в списку, то перегенеровуємо його
        while number in arr:
            number = random.randint(0, 9)

        arr.append(number)
    return arr


# Функція, яка генерує клавіатуру з 4 кнопок, використаємо ReplyKeyboardMarkup(),
# щоб кнопки були розміщені під текстбоксом для введення пофідомлення
# приймає власне питання
def create_keyboard(data):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton(data.answer_options[0], callback_data='0'))
    keyboard.row(telebot.types.InlineKeyboardButton(data.answer_options[1], callback_data='1'))
    keyboard.row(telebot.types.InlineKeyboardButton(data.answer_options[2], callback_data='2'))
    keyboard.row(telebot.types.InlineKeyboardButton(data.answer_options[3], callback_data='3'))
    return keyboard


# Функція створення нового повідомлення з питанням.
# Приймає номер питання по порядку, індекс у списку з питаннями та повідомлення
def create_message(i, number, message):
    bot.send_message(message.chat.id, f'{i}. {list_questions[number].question}',
                     reply_markup=create_keyboard(list_questions[number]))


# Обробка команд - start,help. Головна функція, в якій, власне, тестування
@bot.message_handler(['start', 'help'])
def main(message):
    # Масив з випадковими номерами питанб, наприклад [2, 5, 0, 7...]
    arr = generate_random_numbers()

    # Починаємо відлік часу початку проходження тестування
    start = time.time()

    # В циклі проходимо 10 разів для 10 питань відповідно
    for i in range(10):
        # Створюємо нове повідомлення,
        # і в ролі питання буде питання з індексом поточного елементу у масиві випадкових чисел
        create_message(i + 1, arr[i], message)

        # Для того, щоб звертатись до змінних оголошених вище
        global current_reply
        global current_right
        global current_question_id

        # Визначаємо поточні повідомлення та правильну відповідь
        current_question_id = arr[i]
        current_right = list_questions[current_question_id].right_id

        # Позначаємо, що користувач іще не відповів на питання
        current_reply = False

        # Нічого не робимо, поки користувач не дасть відповід на питання
        while not current_reply:
            pass

    # Запамятовуємо час закінчення тестування
    end = time.time()

    # Відправляємо повідомлення з результатами та видаляємо клавіатуру
    bot.send_message(message.chat.id, f'🏆 Проходження вікторини завершено! \n\nУвага! Ваші результати:'
                                      f'\nОцінка: {counter_right_answers} із 10'
                                      f'\nДата та час проходження: '
                                      f'{datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}'
                                      f'\nЧас проходження вікторини: {int((end - start) // 60)} хв. '
                                      f'{int((end - start) % 60)} с.', reply_markup=ReplyKeyboardRemove())
    # Посилання на питання робимо недійсними
    current_question_id = None
    current_right = None


# Обробник на кнопки. Якщо натиснута правильна, то повідмляємо про це та інкрементимо к-сть правильних відповідей
# (Якщо використовувати InlineKeyboard)
@bot.callback_query_handler(lambda q: int(q.data) == current_right)
def callback_button(message: telebot.types.CallbackQuery):
    bot.send_message(message.message.chat.id, '✅ Правильно! Молодець!')

    # Дозволяємо надіслати наступне повідомдення
    global current_reply
    current_reply = True

    global counter_right_answers
    counter_right_answers += 1


# Обробник на кнопки. Аналогчно попередньому, але тепер, коли відповідь неправильна
# (Якщо використовувати InlineKeyboard)
@bot.callback_query_handler(lambda q: int(q.data) != current_right)
def callback_button(message: telebot.types.CallbackQuery):
    bot.send_message(message.message.chat.id, '❌ Неправильно! Будь уважнішим!')

    # Дозволяємо надіслати наступне повідомдення
    global current_reply
    current_reply = True


# Реалізовано можливість надсилання відповіді просто текстом
@bot.message_handler()
def callback_text(message: telebot.types.Message):
    global current_reply
    global current_right
    global current_question_id

    # Якщо введений текст співпадає з правильною відповіддю то повідомляємо про це та інкрементуємо значення
    # Інакше просто повідомляємо
    if message.text.lower() == list_questions[current_question_id].answer_options[current_right].lower():
        bot.reply_to(message, f'✅ Правильна відповідь!')
        global counter_right_answers
        counter_right_answers += 1
    else:
        bot.reply_to(message, '❌ Неправильна відповідь!')

    # Дозволяємо надіслати наступне повідомдення
    global current_reply
    current_reply = True


# Для того, щоб бот працював неперервно
bot.polling(non_stop=True)
