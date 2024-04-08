from DataBase.dbModels import FiveHundredWords, NowFiveHundredWords, User


class Logic500():
    @staticmethod
    async def repeat(
            *,
            user_telegram_id: int
    ):
        words = await NowFiveHundredWords.get_words(
            user_telegram_id=user_telegram_id
        )
        words_list = ''
        for word in words:
            words_list = f'{words_list}{word.english} -- {word.russian}\n\n'
        return words_list

    @staticmethod
    async def plus_true_e_r(
            *,
            word
    ):
        await NowFiveHundredWords.plus_true_e_r(
            word=word
        )


    @staticmethod
    async def off_true_e_r(
            *,
            word
    ):
        await NowFiveHundredWords.off_true_e_r(
            word=word
        )

    @staticmethod
    async def plus_true_r_e(
            *,
            word
    ):
        await NowFiveHundredWords.plus_true_r_e(
            word=word
        )

    @staticmethod
    async def off_true_r_e(
            *,
            word
    ):
        await NowFiveHundredWords.off_true_r_e(
            word=word
        )

    @staticmethod
    async def delete_know_word(
            *,
            word,
            key: bool = False
    ):
        threshold = await NowFiveHundredWords.get_threshold(
            word=word
        )
        if threshold or key:
            await NowFiveHundredWords.delete_word(
                word=word
            )
            user = await User.get_user(
                user_telegram_id=word.user_telegram_id
            )
            word_2 = await FiveHundredWords.get_word(
                word_id=user.number_500 + 1
            )
            await User.plus_number_500(
                user_telegram_id=word.user_telegram_id
            )
            await NowFiveHundredWords.add_word(
                english=word_2.english,
                russian=word_2.russian,
                user_telegram_id=word.user_telegram_id
            )
