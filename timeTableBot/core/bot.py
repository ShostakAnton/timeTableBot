import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from core import keyboards as kb
from accounts.models import Student
from core.models import Student_group
bot = Bot(token=os.environ.get("TOKEN"))
dp = Dispatcher(bot)


User_Choice = {}

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nВыбирете ваш факультет:", reply_markup=await kb.get_inline_kb_faculty())


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('faculty'))
async def process_callback_faculty(callback_query: types.CallbackQuery):
    User_Choice['faculty'] = callback_query.data.split("_")[-1]
    
    await bot.send_message(callback_query.from_user.id, "Выбирете ваш курс:", reply_markup= await kb.get_inline_kb_course())

    # delete msg
    #await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('course'))
async def process_callback_course(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    
    User_Choice['course'] = callback_query.data.split("_")[-1]
    
    inline_kb_direction = await kb.get_inline_kb_direction(User_Choice['faculty'], User_Choice['course'])
    await bot.send_message(callback_query.from_user.id, "Выбирете ваше направление:", reply_markup=inline_kb_direction)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('direction'))
async def process_callback_direction(callback_query: types.CallbackQuery):
    User_Choice['direction'] = callback_query.data.split("_")[-1]

    inline_kb_group = await kb.get_inline_kb_group(User_Choice['faculty'], User_Choice['course'], User_Choice['direction'])
    await bot.send_message(callback_query.from_user.id, "Выбирете вашу группу:", reply_markup=inline_kb_group)

    

from asgiref.sync import sync_to_async


@sync_to_async
def get_group_by_name(name):
    return Student_group.objects.get(name=name).id

@sync_to_async
def create_user(user_info, group_id):
    Student.objects.update_or_create(
        id=user_info['id'],
        defaults={
            "first_name":user_info['first_name'],
            "username":user_info['username'],
            "group_id":group_id
        }
    )

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('group'))
async def process_callback_group(callback_query: types.CallbackQuery):
    user_info = callback_query['from']
    group_id = await get_group_by_name(callback_query.data.split("_")[-1])

    await create_user(user_info, group_id)

    await bot.send_message(callback_query.from_user.id, 
        """Ваша группа сохранена. Вы будете получать напоминание о предстоящей паре за 10 мин до начала пары."""
    )