from DataBase.dbModels import Groups, SelfWords


class LogicSelf():
    @staticmethod
    async def get_groups(
            *,
            user_telegran_id: int
    ):
        groups = await Groups.get_groups(
            user_telegram_id=user_telegran_id
        )

        return groups

    @staticmethod
    async def add_group(
            *,
            group_name: str,
            user_telegarm_id: int
    ):
        await Groups.add_group(
            name=group_name,
            user_telegram_id=user_telegarm_id
        )

    @staticmethod
    async def add_word(
            *,
            group_name: str,
            english: str,
            russian: str,
            user_telegram_id: int
    ):
        await SelfWords.add_word(
            english=english,
            russian=russian,
            user_telegram_id=user_telegram_id,
            group_name=group_name
        )

    @staticmethod
    async def repeat(
            *,
            group_name: str,
            user_telegarm_id: int
    ):
        words = await SelfWords.get_first_30_words(
            user_telegram_id=user_telegarm_id,
            group_name=group_name
        )
        words_list = ''
        if words != []:
            for word in words:
                words_list = f'{words_list}{word.english} -- {word.russian}\n\n'
            return words_list
        else:
            return 'В этой группе ещё нет слов'

    @staticmethod
    async def delete_word(
            *,
            word
    ):
        await SelfWords.delete_word(
            word=word
        )

    @staticmethod
    async def delete_group(
            *,
            user_telegram_id: int,
            group_name: str
    ):
        words = await SelfWords.get_words(
            user_telegram_id=user_telegram_id,
            group_name=group_name
        )

        for word in words:
            await SelfWords.delete_word(
                word=word
            )

        await Groups.delete_group(
            user_telegram_id=user_telegram_id,
            group_name=group_name
        )



























