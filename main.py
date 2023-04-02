import openai
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
# Установка ключа API OpenAI
openai.api_key = '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'
# Configure logging
logging.basicConfig(level=logging.INFO)
# Initialize bot and dispatcher
bot = Bot(token="6009195588:AAHFuZVcGMWNqXoNSOdsdUhNXUweb7HTMGs")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

def generate_response(input_text):
    if input_text == "":
        return
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user",
                   "content":
                       input_text}]
    )
    answer = (response.choices[0])['message']['content']
    return answer
# States
class AskOpenAI(StatesGroup):
    wait_for_input = State()

class Translation(StatesGroup):
    waiting_for_command = State()
    waiting_for_translation = State()
    waiting_for_bot = State()

# Start command
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('/start'))
    await message.reply(
        "Привет! Я связываю OpenAI с ботом. \n\n"
        "Отправь мне свой вопрос, я попробую ответить на него с помощью OpenAI.", reply_markup=keyboard
    )
    await AskOpenAI.wait_for_input.set()
# Dialogue with OpenAI
@dp.message_handler(state=AskOpenAI.wait_for_input, content_types=types.ContentTypes.TEXT)
async def send_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['input'] = message.text
    print(data)
    output = generate_response(data['input'])
    print(output)
    await message.answer(output)

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)





