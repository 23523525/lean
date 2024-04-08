from aiogram import Router, types
from aiogram import F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from DataBase.bdLogic.selfLogic import LogicSelf
from DataBase.bdLogic.mainLogic import LogicMain
from Bot.markup.create_markup import inline_keyboard_callback

self_router = Router()


class ChoiceGroup(StatesGroup):
    group_name = State()
    processing = State()
    message = State()
    english = State()
    russian = State()
    finish = State()

@self_router.callback_query((F.data == 'self_words') | (F.data == 'self_words_delete'))
async def self_words(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    if callback.data == 'self_words_delete':
        data = await state.get_data()
        await data['message'].delete()
        await state.clear()

    groups = await LogicSelf.get_groups(
        user_telegran_id=callback.from_user.id
    )
    btns = {
        'Добавить группу': 'add_group',
        'Назад в меню': 'menu'
    }

    for i in groups:
        btns[i.name] = i.name

    await callback.message.answer(
        'Свои слова\n'
        'Учтите, что "свои слова" не будут автоматически удаляться по мере изучения,\n' 
        'Выберете группу слов:',
        reply_markup=inline_keyboard_callback(
            btns=btns,
            sizes=(2,)
        )
    )

    await state.set_state(ChoiceGroup.group_name)

class AddGroup(StatesGroup):
    group_name = State()
    message = State()

@self_router.callback_query(F.data == 'add_group')
async def add_group(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()

    msg = await callback.message.answer(
        'Введите название группы которую нужно создать'
    )
    await state.update_data(message=msg)
    await state.set_state(AddGroup.group_name)


@self_router.message(AddGroup.group_name,F.text)
async def add_group_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await data['message'].delete()
    await message.delete()

    await LogicSelf.add_group(
        group_name=message.text,
        user_telegarm_id=message.from_user.id
    )

    await message.answer(
        f'Группа {message.text} успешно создана',
        reply_markup=inline_keyboard_callback(
            btns={
                'Далее': 'self_words',
                'Назад к меню': 'menu'
            },
            sizes=(2,)
        )
    )
    await state.clear()

@self_router.callback_query(ChoiceGroup.group_name, F.data)
async def self_group(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(group_name=callback.data)

    await callback.message.delete()

    await LogicMain.clean_cache_1(
        user_telegram_id=callback.from_user.id
    )
    await LogicMain.clean_cache_2(
        user_telegram_id=callback.from_user.id
    )
    await LogicMain.from_now_to_cache(
        user_telegram_id=callback.from_user.id,
        key_db='self',
        group_name=callback.data
    )

    await callback.message.answer(
        f'Группа "{callback.data}"\n\
        Выберете режим для продолжения:',
        reply_markup=inline_keyboard_callback(
            btns={
                'Повторить': 'repeat_self',
                'А-Р': 'E_R_self',
                'Р-А': 'R_E_self',
                'Добавить слово': 'add_word_self',
                'Удалить группу': 'delete_group',
                'Назад в меню': 'menu'
            },
            sizes=(3,2,1)
        )
    )

    await state.set_state(ChoiceGroup.processing)

@self_router.callback_query(F.data == 'repeat_self')
async def repeat_self(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()

    now_group_data = await state.get_data()

    word_list = await LogicSelf.repeat(
        user_telegarm_id=callback.from_user.id,
        group_name=now_group_data['group_name']
    )

    await callback.message.answer(
        word_list,
        reply_markup=inline_keyboard_callback(
            btns={
                'Назад': 'self_words',
                'Назад к меню': 'menu'
            },
            sizes=(2,)
        )
    )

@self_router.callback_query(ChoiceGroup.processing, F.data == 'add_word_self')
async def add_word_self(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()

    await callback.message.answer(
        'Нажмите "Готово" когда добавите все слова',
        reply_markup=inline_keyboard_callback(
            btns={
                'Готово': 'self_words_delete'
            }
        )
    )
    msg = await callback.message.answer(
        'Введите слово на английском'
    )

    await state.update_data(message=msg)
    await state.set_state(ChoiceGroup.english)


@self_router.message(ChoiceGroup.english, F.text)
async def add_english(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await data['message'].delete()
    await message.delete()
    await state.update_data(english=message.text)

    msg = await message.answer(
        f'Слово: {message.text}\n'
        'Введите слово на русском'
    )

    await state.update_data(message=msg)
    await state.set_state(ChoiceGroup.russian)

@self_router.message(ChoiceGroup.russian, F.text)
async def add_russian(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await data['message'].delete()
    await message.delete()

    await LogicSelf.add_word(
        group_name=data['group_name'],
        english=data['english'],
        russian=message.text,
        user_telegram_id=message.from_user.id
    )

    msg = await message.answer(
        f'Слово {data['english'], message.text} успешно добавлено'
        f'Введите следующее слово на английском'
    )
    await state.update_data(message=msg)
    await state.set_state(ChoiceGroup.english)

@self_router.callback_query(ChoiceGroup.processing, (F.data == 'E_R_self') | (F.data == 'true_E_R_self')\
                            | (F.data == 'false_E_R_self') | (F.data == 'delete_word_self_E_R'))
async def E_R_self(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()

    if callback.data == 'true_E_R_self':
        word = await LogicMain.get_first_cache_1(
            user_telegram_id=callback.from_user.id
        )
        await LogicMain.delite_word_cache_1(
            word=word
        )
    elif callback.data == 'false_E_R_self':
        word = await LogicMain.get_first_cache_1(
            user_telegram_id=callback.from_user.id
        )
        await LogicMain.add_word_to_cache_2(
            word=word
        )
        await LogicMain.delite_word_cache_1(
            word=word
        )
    elif callback.data == 'delete_word_self_E_R':
        word = await LogicMain.get_first_cache_1(
            user_telegram_id=callback.from_user.id
        )
        await LogicMain.delite_word_cache_1(
            word=word
        )
        await LogicSelf.delete_word(
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
                    'Я правильно ответил': 'true_E_R_self',
                    'Я ошибся': 'false_E_R_self',
                    'Удалить это слово': 'delete_word_self_E_R',
                    'Назад': 'self_words',
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
                        'Ещё раз А-Р': 'E_R_self',
                        'Назад': 'self_words',
                        'Назад к меню': 'menu'
                    },
                    sizes=(1, 2)
                )
            )
        else:
            data = await state.get_data()

            await LogicMain.from_now_to_cache(
                user_telegram_id=callback.from_user.id,
                key_db='self',
                group_name=data['group_name']
            )

            await callback.message.answer(
                'Молодец, всё правильно\n'
                'Для закрепления результата предлагаю тебе пройти Р-А',
                reply_markup=inline_keyboard_callback(
                    btns={
                        'Р-А': 'R_E_self',
                        'Назад': 'self_words',
                        'Назад к меню': 'menu'
                    },
                    sizes=(1, 2)
                )
            )
@self_router.callback_query(ChoiceGroup.processing, (F.data == 'R_E_self') | (F.data == 'true_R_E_self')\
                            | (F.data == 'false_R_E_self') | (F.data == 'delete_word_self_R_E'))
async def R_E_self(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()

    if callback.data == 'true_R_E_self':
        word = await LogicMain.get_first_cache_1(
            user_telegram_id=callback.from_user.id
        )
        await LogicMain.delite_word_cache_1(
            word=word
        )
    elif callback.data == 'false_R_E_self':
        word = await LogicMain.get_first_cache_1(
            user_telegram_id=callback.from_user.id
        )
        await LogicMain.add_word_to_cache_2(
            word=word
        )
        await LogicMain.delite_word_cache_1(
            word=word
        )
    elif callback.data == 'delete_word_self_R_E':
        word = await LogicMain.get_first_cache_1(
            user_telegram_id=callback.from_user.id
        )
        await LogicMain.delite_word_cache_1(
            word=word
        )
        await LogicSelf.delete_word(
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
                    'Я правильно ответил': 'true_R_E_self',
                    'Я ошибся': 'false_R_E_self',
                    'Удалить это слово': 'delete_word_self_R_E',
                    'Назад': 'self_words',
                    'Назад к меню': 'menu'
                },
                sizes=(2, 3)
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
                        'Ещё раз Р-А': 'R_E_self',
                        'Назад': 'self_words',
                        'Назад к меню': 'menu'
                    },
                    sizes=(1, 2)
                )
            )
        else:
            data = await state.get_data()

            await LogicMain.from_now_to_cache(
                user_telegram_id=callback.from_user.id,
                key_db='self',
                group_name=data['group_name']
            )

            await callback.message.answer(
                'Молодец, всё правильно\n'
                'Для закрепления результата предлагаю тебе пройти А-Р',
                reply_markup=inline_keyboard_callback(
                    btns={
                        'А-Р': 'E_R_self',
                        'Назад': 'self_words',
                        'Назад к меню': 'menu'
                    },
                    sizes=(1, 2)
                )
            )

@self_router.callback_query(ChoiceGroup.processing, F.data == 'delete_group')
async def delete_group(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()

    data = await state.get_data()

    await LogicSelf.delete_group(
        user_telegram_id=callback.from_user.id,
        group_name=data['group_name']
    )

    await callback.message.answer(
        'Группа и все слова в ней были удалены',
        reply_markup=inline_keyboard_callback(
            btns={
                'Далее': 'self_words',
                'Назад к меню': 'menu'
            }
        )
    )

    await state.clear()
























