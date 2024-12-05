from aiogram import types, Dispatcher
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import F
from config import quiz_data
from database import update_quiz_index, get_quiz_index, get_quiz_result, save_quiz_result,reset_stats

def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_quiz, Command("quiz"))
    dp.message.register(cmd_stats, Command("stats"))
    dp.message.register(cmd_quiz, F.text == "Начать игру")
    dp.callback_query.register(right_answer, F.data == "right_answer")
    dp.callback_query.register(wrong_answer, F.data == "wrong_answer")

async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

async def cmd_quiz(message: types.Message):
    user_id = message.from_user.id
    await reset_stats(user_id)
    await message.answer("Давайте начнем квиз!")
    await new_quiz(message)

async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    await update_quiz_index(user_id, current_question_index)
    await get_question(message, user_id)

async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    question_data = quiz_data[current_question_index]
    correct_index = question_data['correct_option']
    options = question_data['options']

    kb = generate_options_keyboard(options, options[correct_index])
    await message.answer(f"{question_data['question']}", reply_markup=kb)

def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()
    for option in answer_options:
        builder.add(
            types.InlineKeyboardButton(
                text=option,
                callback_data="right_answer" if option == right_answer else "wrong_answer"
            )
        )
    builder.adjust(1)
    return builder.as_markup()

async def right_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id, reply_markup=None)
    user_id = callback.from_user.id
    current_question_index = await get_quiz_index(user_id)
    correct_answers, total_questions = await get_quiz_result(callback.from_user.id)
    correct_answers += 1
    await callback.message.answer("Верно!")
    current_question_index += 1
    await update_quiz_index(user_id, current_question_index)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, user_id)
        await save_quiz_result(callback.from_user.id, correct_answers, total_questions)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")
        total_questions = len(quiz_data)
        await save_quiz_result(callback.from_user.id, correct_answers, total_questions)
        await callback.message.answer(f"Ваш результат: {correct_answers} из {total_questions}.")

async def wrong_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id, reply_markup=None)
    user_id = callback.from_user.id
    current_question_index = await get_quiz_index(user_id)
    correct_option = quiz_data[current_question_index]['correct_option']
    await callback.message.answer(f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")
    current_question_index += 1
    await update_quiz_index(user_id, current_question_index)


    if current_question_index < len(quiz_data):
        await get_question(callback.message, user_id)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")
        correct_answers, total_questions = await get_quiz_result(callback.from_user.id)
        total_questions = len(quiz_data)
        await save_quiz_result(callback.from_user.id, correct_answers, total_questions)
        await callback.message.answer(f"Ваш результат: {correct_answers} из {total_questions}.")



async def cmd_stats(message: types.Message):
    user_id = message.from_user.id
    correct_answers, total_questions = await get_quiz_result(user_id)
    
    if total_questions > 0:
        await message.answer(f"Ваша статистика:\nПравильные ответы: {correct_answers}\nВсего вопросов: {total_questions}")
    else:
        await message.answer("Вы еще не проходили квиз.")
