from DataBase.dbModels import ThreeThousenWords, NowThreeThousenWords, User


class Logic3000():
    @staticmethod
    async def repeat(
            *,
            user_telegram_id: int
    ):
        words = await NowThreeThousenWords.get_words(
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
        await NowThreeThousenWords.plus_true_e_r(
            word=word
        )


    @staticmethod
    async def off_true_e_r(
            *,
            word
    ):
        await NowThreeThousenWords.off_true_e_r(
            word=word
        )

    @staticmethod
    async def plus_true_r_e(
            *,
            word
    ):
        await NowThreeThousenWords.plus_true_r_e(
            word=word
        )

    @staticmethod
    async def off_true_r_e(
            *,
            word
    ):
        await NowThreeThousenWords.off_true_r_e(
            word=word
        )

    @staticmethod
    async def delete_know_word(
            *,
            word,
            key: bool = False
    ):
        threshold = await NowThreeThousenWords.get_threshold(
            word=word
        )
        if threshold or key:
            await NowThreeThousenWords.delete_word(
                word=word
            )
            user = await User.get_user(
                user_telegram_id=word.user_telegram_id
            )
            word_2 = await ThreeThousenWords.get_word(
                word_id=user.number_3000 + 1
            )
            await User.plus_number_3000(
                user_telegram_id=word.user_telegram_id
            )
            await NowThreeThousenWords.add_word(
                english=word_2.english,
                russian=word_2.russian,
                user_telegram_id=word.user_telegram_id
            )