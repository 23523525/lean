from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from DataBase.bdLogic.mainLogic import LogicMain
from Bot.markup.create_markup import inline_keyboard_callback

main_router = Router()

@main_router.message(CommandStart())
async def start(message: types.Message):
    await message.delete()

    await LogicMain.start(
        user_telegram_id=message.from_user.id
    )

    await message.answer(
        'Бот находится в раннем доступе, баги это нормально'
    )
    await message.answer(
        'Привет, я Бот созданный для того, чтобы помочь тебе изучать английский.\n'
        'У меня есть несколько списков:\n'
        '      500 базовых слов\n'
        '      3000 базовых слов\n'
        'Ты также можешь добавлять свои слова/фразы\n'
        'Обучение идет по 30 слов, как только программа поймет что данное слово выучено она заменит его на новое\n'
        'Рекомендуется начать с 500 слов( параллельно можно учить свои слова), а дальше перейти на 3000\n'
        'В выпадающем меню нажми "Помощь" чтобы узнать про остальные функции',
        reply_markup=inline_keyboard_callback(
            btns={
                'Меню': 'menu'
            },
            sizes=(1,)
        )
    )


@main_router.callback_query(F.data == 'menu')
async def menu(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.message.delete()
    await callback.message.answer(
        'Меню:           ',
        reply_markup=inline_keyboard_callback(
            btns={
                '500 слов': '500words',
                '3000 слов': '3000words',
                'Свои слова': 'self_words',
                'Помощь': 'help'
            },
            sizes=(3,1)
        )
    )


@main_router.callback_query(F.data == 'help')
async def help(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        '500 слов -- базовые 500 слов\n'
        '     Повторить -- повторение слов\n'
        '     А-Р -- тест с английского на русский\n'
        '     Р-А -- тест с русского на английский\n\n'
        '3000 слов -- базовые 3000 слов\n'
        '     Повторить -- повторение слов\n'
        '     А-Р -- тест с английского на русский\n'
        '     Р-А -- тест с русского на английский\n\n'
        'Свои слова -- слова или фразы которые вы сами добавили\n'
        '     Повторить -- повторение слов\n'
        '     А-Р -- тест с английского на русский\n'
        '     Р-А -- тест с русского на английский\n'
        '     Добавить -- добавить новое слово в словарь',
        reply_markup=inline_keyboard_callback(
            btns={
                'Назад в меню': 'menu'
            },
            sizes=(1,)
        )

    )