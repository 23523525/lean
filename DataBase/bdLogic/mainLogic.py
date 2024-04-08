from random import shuffle

from DataBase.dbModels import User, FiveHundredWords, NowFiveHundredWords, Cache, Cache_2, NowThreeThousenWords, \
    ThreeThousenWords, SelfWords


class LogicMain():
    @staticmethod
    async def start(
            *,
            user_telegram_id: int
    ):
        user = await User.get_user(user_telegram_id=user_telegram_id)
        if not user:
            await User.add_user(
                telegram_id=user_telegram_id
            )

            for i in range(1, 31):
                word = await FiveHundredWords.get_word(
                    word_id=i
                )
                await NowFiveHundredWords.add_word(
                    english=word.english,
                    russian=word.russian,
                    user_telegram_id=user_telegram_id
                )

                word = await ThreeThousenWords.get_word(
                    word_id=i
                )
                await NowThreeThousenWords.add_word(
                    english=word.english,
                    russian=word.russian,
                    user_telegram_id=user_telegram_id
                )

    @staticmethod
    async def clean_cache_1(
            *,
            user_telegram_id: int
    ):
        await Cache.clean(
            user_telegram_id=user_telegram_id
        )

    @staticmethod
    async def clean_cache_2(
            *,
            user_telegram_id: int
    ):
        await Cache_2.clean(
            user_telegram_id=user_telegram_id
        )

    @staticmethod
    async def from_now_to_cache(
            *,
            user_telegram_id: int,
            key_db: str,
            group_name: str = None
    ):
        if key_db == 'self':
            words = await SelfWords.get_first_30_words(
                user_telegram_id=user_telegram_id,
                group_name=group_name
            )
        else:
            if key_db == '500':
                now = NowFiveHundredWords
            elif key_db == '3000':
                now = NowThreeThousenWords
            elif key_db == 'self':
                now = SelfWords
            elif key_db == 'cache':
                now = Cache_2


            words = await now.get_words(
                user_telegram_id=user_telegram_id
            )

        shuffle(words)

        for word in words:
            await Cache.add_word(
                english=word.english,
                russian=word.russian,
                user_telegram_id=user_telegram_id
            )

    @staticmethod
    async def get_first_cache_1(
            *,
            user_telegram_id: int
    ):
        word = await Cache.get_word(
            user_telegram_id=user_telegram_id
        )
        return word

    @staticmethod
    async def get_first_cache_2(user_telegram_id: int):
        word = await Cache_2.get_word(
            user_telegram_id=user_telegram_id)
        return word

    @staticmethod
    async def delite_word_cache_1(
            *,
            word
    ):
        await Cache.delete_word(
            word=word
        )

    @staticmethod
    async def add_word_to_cache_2(
            *,
            word
    ):
        await Cache_2.add_word(
            english=word.english,
            russian=word.russian,
            user_telegram_id=word.user_telegram_id
        )