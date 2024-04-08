from aiogram import Router, types
from aiogram import F
from aiogram.enums import ParseMode

from DataBase.bdLogic.Logic500 import Logic500
from DataBase.bdLogic.mainLogic import LogicMain
from Bot.markup.create_markup import inline_keyboard_callback

router500 = Router()

@router500.callback_query(F.data == '500words')
async def words500(callback: types.CallbackQuery):
    await callback.message.delete()

    await LogicMain.clean_cache_1(
        user_telegram_id=callback.from_user.id
    )
    await LogicMain.clean_cache_2(
        user_telegram_id=callback.from_user.id
    )
    await LogicMain.from_now_to_cache(
        user_telegram_id=callback.from_user.id,
        key_db='500'
    )

    await callback.message.answer(
        '500 базовых слов\n\
        Выберете режим для продолжения:',
        reply_markup= inline_keyboard_callback(
            btns={
                'Повторить': 'repeat_500',
                'А-Р': 'E_R_500',
                'Р-А': 'R_E_500',
                'Назад в меню': 'menu'
            },
            sizes=(3,1)
        )
    )

@router500.callback_query(F.data == 'repeat_500')
async def repeat_500(callback: types.CallbackQuery):
    await callback.message.delete()

    words_list = await Logic500.repeat(
        user_telegram_id=callback.from_user.id
    )

    await callback.message.answer(
        words_list,
        reply_markup=inline_keyboard_callback(
            btns={
                'Назад': '500words',
                'Назад к меню': 'menu'
            },
            sizes=(2,)
        )
    )


@router500.callback_query((F.data == 'E_R_500') | (F.data == 'true_E_R_500') | (F.data == 'false_E_R_500')\
                          | (F.data == 'know_E_R_500'))
async def E_R_500(callback: types.CallbackQuery):
    await callback.message.delete()

    if callback.data == 'true_E_R_500':
        word = await LogicMain.get_first_cache_1(
            user_telegram_id=callback.from_user.id
        )
        await Logic500.plus_true_e_r(
            word=word
        )
        await LogicMain.delite_word_cache_1(
            word=word
        )
        await Logic500.delete_know_word(
            word=word
        )
    elif callback.data == 'false_E_R_500':
        word = await LogicMain.get_first_cache_1(
            user_telegram_id=callback.from_user.id
        )
        await Logic500.off_true_e_r(
            word=word
        )
        await LogicMain.add_word_to_cache_2(
            word=word
        )
        await LogicMain.delite_word_cache_1(
            word=word
        )
        await Logic500.delete_know_word(
            word=word
        )
    elif callback.data == 'know_E_R_500':
        word = await LogicMain.get_first_cache_1(
            user_telegram_id=callback.from_user.id
        )
        await Logic500.delete_know_word(
            word=word,
            key=True
        )
        await LogicMain.delite_word_cache_1(
            word=word
        )

    word = await LogicMain.get_first_cache_1(
        user_telegram_id=callback.from_user.id
    )

    if word:
        await callback.message.answer(
            f'{word.english} <span class="tg-spoiler">{word.russian}</span>',
            parse_mode=ParseMode.HTML,
            reply_markup=inline_keyboard_callback(
                btns={
                    'Я правильно ответил': 'true_E_R_500',
                    'Я ошибся': 'false_E_R_500',
                    'Я уже знаю это слово': 'know_E_R_500',
                    'Назад': '500words',
                    'Назад к меню': 'menu'
                },
                sizes=(2,3)
            )
        )
    else:
        if await LogicMain.get_first_cache_2(
            user_telegram_id=callback.from_user.id
        ):
            await LogicMain.clean_cache_1(
                user_telegram_id=callback.from_user.id
            )
            await LogicMain.from_now_to_cache(
                user_telegram_id=callback.from_user.id,
                key_db='cache'
            )
            await LogicMain.clean_cache_2(
                user_telegram_id=callback.from_user.id
            )

            await callback.message.answer(
                'Отлтчно\n'
                'Но были ошибки\n'
                'Предлагаю еще раз пройти(только со словами в которых были ошибки)',
                reply_markup=inline_keyboard_callback(
                    btns={
                        'Ещё раз А-Р': 'E_R_500',
                        'Назад': '500words',
                        'Назад к меню': 'menu'
                    },
                    sizes=(1,2)
                )
            )
        else:
            await LogicMain.from_now_to_cache(
                user_telegram_id=callback.from_user.id,
                key_db='500'
            )

            await callback.message.answer(
                'Молодец, всё правильно\n'
                'Для закрепления результата предлагаю тебе пройти Р-А',
                reply_markup=inline_keyboard_callback(
                    btns={
                        'Р-А': 'R_E_500',
                        'Назад': '500words',
                        'Назад к меню': 'menu'
                    },
                    sizes=(1,2)
                )
            )

@router500.callback_query((F.data == 'R_E_500') | (F.data == 'true_R_E_500') | (F.data == 'false_R_E_500')\
                          | (F.data == 'know_R_E_500'))
async def R_E_500(callback: types.CallbackQuery):
    await callback.message.delete()

    if callback.data == 'true_R_E_500':
        word = await LogicMain.get_first_cache_1(
            user_telegram_id=callback.from_user.id
        )
        await Logic500.plus_true_r_e(
            word=word
        )
        await LogicMain.delite_word_cache_1(
            word=word
        )

        await Logic500.delete_know_word(
            word=word
        )
    elif callback.data == 'false_R_E_500':
        word = await LogicMain.get_first_cache_1(
            user_telegram_id=callback.from_user.id
        )
        await Logic500.off_true_r_e(
            word=word
        )
        await LogicMain.add_word_to_cache_2(
            word=word
        )
        await LogicMain.delite_word_cache_1(
            word=word
        )

        await Logic500.delete_know_word(
            word=word
        )
    elif callback.data == 'know_R_E_500':
        word = await LogicMain.get_first_cache_1(
            user_telegram_id=callback.from_user.id
        )
        await Logic500.delete_know_word(
            word=word,
            key=True
        )
        await LogicMain.delite_word_cache_1(
            word=word
        )

    word = await LogicMain.get_first_cache_1(
            user_telegram_id=callback.from_user.id
    )

    if word:
        await callback.message.answer(
            f'{word.russian} <span class="tg-spoiler">{word.english}</span>',
            parse_mode=ParseMode.HTML,
            reply_markup=inline_keyboard_callback(
                btns={
                    'Я правильно ответил': 'true_R_E_500',
                    'Я ошибся': 'false_R_E_500',
                    'Я уже знаю это слово': 'know_R_E_500',
                    'Назад': '500words',
                    'Назад к меню': 'menu'
                },
                sizes=(2,3)
            )
        )
    else:
        if await LogicMain.get_first_cache_2(
                user_telegram_id=callback.from_user.id
        ):
            await LogicMain.clean_cache_1(
                 user_telegram_id=callback.from_user.id
            )
            await LogicMain.from_now_to_cache(
                user_telegram_id=callback.from_user.id,
                key_db='cache'
            )
            await LogicMain.clean_cache_2(
                user_telegram_id=callback.from_user.id
            )

            await callback.message.answer(
                'Отлтчно\n'
                'Но были ошибки\n'
                'Предлагаю еще раз пройти(только со словами в которых были ошибки)',
                reply_markup=inline_keyboard_callback(
                    btns={
                        'Ещё раз Р-А': 'R_E_500',
                        'Назад': '500words',
                        'Назад к меню': 'menu'
                    },
                    sizes=(1, 2)
                )
            )
        else:
            await LogicMain.from_now_to_cache(
                user_telegram_id=callback.from_user.id,
                key_db='500'
            )

            await callback.message.answer(
                'Молодец, всё правильно\n'
                'Для закрепления результата предлагаю тебе пройти А-Р',
                reply_markup=inline_keyboard_callback(
                    btns={
                        'А-Р': 'E_R_500',
                        'Назад': '500words',
                        'Назад к меню': 'menu'
                    },
                    sizes=(1, 2)
                )
            )