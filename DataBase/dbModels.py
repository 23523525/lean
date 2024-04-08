import asyncio

from sqlalchemy import ForeignKey, select, BigInteger
from sqlalchemy.orm import Mapped, mapped_column,relationship

from DataBase.db import Base, engine
from DataBase.createSession import async_session


#-----------------------------------------------------------------------------------------------------------------------
# База юзеров
class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger,unique=True)
    number_500: Mapped[int] # курсор отображающий самое дальнее слово из 500 базовых слов которое сейчас в изучении
    number_3000: Mapped[int] # курсор отображающий самое дальнее слово из 3000 базовых слов которое сейчас в изучении

    # связи с остальными таблицами
    words500: Mapped[list['NowFiveHundredWords']] = relationship(back_populates='user')
    words3000: Mapped[list['NowThreeThousenWords']] = relationship(back_populates='user')
    words_self: Mapped[list['SelfWords']] = relationship(back_populates='user')
    cache: Mapped[list['Cache']] = relationship(back_populates='user')
    cache_2: Mapped[list['Cache_2']] = relationship(back_populates='user')
    groups: Mapped[list['Groups']] = relationship(back_populates='user')

    @staticmethod
    async def add_user(
            *,
            telegram_id: int
    ):
        try:
            async with async_session as session:
                user = User(
                    telegram_id=telegram_id,
                    number_500=30,
                    number_3000=30
                )
                session.add(user)
                await session.commit()
        except:
            pass

    @staticmethod
    async def plus_number_500(
            *,
            user_telegram_id
    ):
        try:
            async with async_session as session:
                user = await session.execute(
                    select(User).filter(
                        User.telegram_id == user_telegram_id
                    )
                )
                user = user.scalars().one()
                user.number_500 += 1
                await session.commit()
        except:
            pass

    @staticmethod
    async def plus_number_3000(
            *,
            user_telegram_id
    ):
        try:
            async with async_session as session:
                user = await session.execute(
                    select(User).filter(
                        User.telegram_id == user_telegram_id
                    )
                )
                user = user.scalars().one()
                user.number_3000 += 1
                await session.commit()
        except:
            pass

    @staticmethod
    async def get_user(
            *,
            user_telegram_id: int
    ):
        try:
            async with async_session as session:
                    user = await session.execute(select(User).filter(User.telegram_id == user_telegram_id))
                    return user.scalars().one()
        except:
            return False


#-----------------------------------------------------------------------------------------------------------------------
# База 500 слов
class FiveHundredWords(Base):
    __tablename__ = '500'
    id: Mapped[int] = mapped_column(primary_key=True)
    english: Mapped[str]
    russian: Mapped[str]

    @staticmethod
    async def add_word(
            *,
            english: str,
            russian: str
    ):
        try:
            async with async_session as session:
                word = FiveHundredWords(
                    english=english,
                    russian=russian
                )
                session.add(word)
                await session.commit()
        except:
            pass

    @staticmethod
    async def get_word(
            *,
            word_id: int
    ):
        try:
            async with async_session as session:
                    word = await session.execute(select(FiveHundredWords).filter(FiveHundredWords.id == word_id))
                    return word.scalars().one()
        except:
            pass


# Курсор определяющий 30 слов которые сейчас изучаются
class NowFiveHundredWords(Base):
    __tablename__ = 'now500'
    id: Mapped[int] = mapped_column(primary_key=True)
    english: Mapped[str]
    russian: Mapped[str]
    count_e_r: Mapped[int]
    count_r_e: Mapped[int]

    user_telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    user: Mapped['User'] = relationship(back_populates='words500')

    @staticmethod
    async def add_word(
            *,
            english: str,
            russian: str,
            user_telegram_id: int
    ):
        try:
            async with async_session as session:
                word = NowFiveHundredWords(
                    english=english,
                    russian=russian,
                    user_telegram_id=user_telegram_id,
                    count_e_r=0,
                    count_r_e=0
                )
                session.add(word)
                await session.commit()
        except:
            pass

    @staticmethod
    async def get_words(
            *,
            user_telegram_id: int
    ):
        try:
            async with async_session as session:
                words = await session.execute(
                    select(NowFiveHundredWords).join(User).filter(
                        User.telegram_id == user_telegram_id
                    )
                )
                return words.scalars().all()
        except:
            pass

    @staticmethod
    async def get_threshold(
            *,
            word
    ):
        try:
            async with async_session as session:
                word = await session.execute(
                    select(NowFiveHundredWords).filter(
                        NowFiveHundredWords.english == word.english,
                        NowFiveHundredWords.user_telegram_id == word.user_telegram_id
                    )
                )
                word = word.scalars().one()
                if word.count_e_r >= 5 and word.count_r_e >= 5:
                    return True
                else:
                    return False
        except:
            return False

    @staticmethod
    async def delete_word(
            *,
            word
    ):
        try:
            async with async_session as session:
                word = await session.execute(
                    select(NowFiveHundredWords).filter(
                        NowFiveHundredWords.english == word.english,
                        NowFiveHundredWords.user_telegram_id == word.user_telegram_id
                    )
                )
                word = word.scalars().one()
                await session.delete(word)
                await session.commit()
        except:
            pass

    @staticmethod
    async def plus_true_e_r(
            *,
            word
    ):
        try:
            async with async_session as session:
                word = await session.execute(
                    select(NowFiveHundredWords).filter(
                        NowFiveHundredWords.english == word.english,
                        NowFiveHundredWords.user_telegram_id == word.user_telegram_id
                    )
                )
                word = word.scalars().one()
                word.count_e_r += 1
                await session.commit()
        except:
            pass

    @staticmethod
    async def off_true_e_r(
            *,
            word
    ):
        try:
            async with async_session as session:
                word = await session.execute(
                    select(NowFiveHundredWords).filter(
                        NowFiveHundredWords.english == word.english,
                        NowFiveHundredWords.user_telegram_id == word.user_telegram_id
                    )
                )
                word = word.scalars().one()
                word.count_e_r = 0
                await session.commit()
        except:
            pass

    @staticmethod
    async def plus_true_r_e(
            *,
            word
    ):
        try:
            async with async_session as session:
                word = await session.execute(
                    select(NowFiveHundredWords).filter(
                        NowFiveHundredWords.english == word.english,
                        NowFiveHundredWords.user_telegram_id == word.user_telegram_id
                    )
                )
                word = word.scalars().one()
                word.count_r_e += 1
                await session.commit()
        except:
            pass

    @staticmethod
    async def off_true_r_e(
            *,
            word
    ):
        try:
            async with async_session as session:
                word = await session.execute(
                    select(NowFiveHundredWords).filter(
                        NowFiveHundredWords.english == word.english,
                        NowFiveHundredWords.user_telegram_id == word.user_telegram_id
                    )
                )
                word = word.scalars().one()
                word.count_r_e = 0
                await session.commit()
        except:
            pass


#-----------------------------------------------------------------------------------------------------------------------
# База 3000 слов
class ThreeThousenWords(Base):
    __tablename__ = '3000'
    id: Mapped[int] = mapped_column(primary_key=True)
    english: Mapped[str]
    russian: Mapped[str]

    @staticmethod
    async def add_word(
            *,
            english: str,
            russian: str
    ):
        try:
            async with async_session as session:
                word = ThreeThousenWords(
                    english=english,
                    russian=russian
                )
                session.add(word)
                await session.commit()
        except:
            pass

    @staticmethod
    async def get_word(
            *,
            word_id: int
    ):
        try:
            async with async_session as session:
                word = await session.execute(select(ThreeThousenWords).filter(ThreeThousenWords.id == word_id))
                return word.scalars().one()
        except:
            pass


# Курсор определяющий 30 слов которые сейчас изучаются
class NowThreeThousenWords(Base):
    __tablename__ = 'now3000'
    id: Mapped[int] = mapped_column(primary_key=True)
    english: Mapped[str]
    russian: Mapped[str]
    count_e_r: Mapped[int]
    count_r_e: Mapped[int]

    user_telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    user: Mapped['User'] = relationship(back_populates='words3000')

    @staticmethod
    async def add_word(
            *,
            english: str,
            russian: str,
            user_telegram_id: int
    ):
        try:
            async with async_session as session:
                word = NowThreeThousenWords(
                    english=english,
                    russian=russian,
                    user_telegram_id=user_telegram_id,
                    count_e_r=0,
                    count_r_e=0
                )
                session.add(word)
                await session.commit()
        except:
            pass

    @staticmethod
    async def get_words(
            *,
            user_telegram_id: int
    ):
        try:
            async with async_session as session:
                words = await session.execute(
                    select(NowThreeThousenWords).join(User).filter(
                        User.telegram_id == user_telegram_id
                    )
                )
                return words.scalars().all()
        except:
            pass

    @staticmethod
    async def get_threshold(
            *,
            word
    ):
        try:
            async with async_session as session:
                word = await session.execute(
                    select(NowThreeThousenWords).filter(
                        NowThreeThousenWords.english == word.english,
                        NowThreeThousenWords.user_telegram_id == word.user_telegram_id
                    )
                )
                word = word.scalars().one()
                if word.count_e_r >= 5 and word.count_r_e >= 5:
                    return True
                else:
                    return False
        except:
            return False

    @staticmethod
    async def delete_word(
            *,
            word
    ):
        try:
            async with async_session as session:
                word = await session.execute(
                    select(NowThreeThousenWords).filter(
                        NowThreeThousenWords.english == word.english,
                        NowThreeThousenWords.user_telegram_id == word.user_telegram_id
                    )
                )
                word = word.scalars().one()
                await session.delete(word)
                await session.commit()
        except:
            pass

    @staticmethod
    async def plus_true_e_r(
            *,
            word
    ):
        try:
            async with async_session as session:
                word = await session.execute(
                    select(NowThreeThousenWords).filter(
                        NowThreeThousenWords.english == word.english,
                        NowThreeThousenWords.user_telegram_id == word.user_telegram_id
                    )
                )
                word = word.scalars().one()
                word.count_e_r += 1
                await session.commit()
        except:
            pass

    @staticmethod
    async def off_true_e_r(
            *,
            word
    ):
        try:
            async with async_session as session:
                word = await session.execute(
                    select(NowThreeThousenWords).filter(
                        NowThreeThousenWords.english == word.english,
                        NowThreeThousenWords.user_telegram_id == word.user_telegram_id
                    )
                )
                word = word.scalars().one()
                word.count_e_r = 0
                await session.commit()
        except:
            pass

    @staticmethod
    async def plus_true_r_e(
            *,
            word
    ):
        try:
            async with async_session as session:
                word = await session.execute(
                    select(NowThreeThousenWords).filter(
                        NowThreeThousenWords.english == word.english,
                        NowThreeThousenWords.user_telegram_id == word.user_telegram_id
                    )
                )
                word = word.scalars().one()
                word.count_r_e += 1
                await session.commit()
        except:
            pass

    @staticmethod
    async def off_true_r_e(
            *,
            word
    ):
        try:
            async with async_session as session:
                word = await session.execute(
                    select(NowThreeThousenWords).filter(
                        NowFiveHundredWords.english == word.english,
                        NowThreeThousenWords.user_telegram_id == word.user_telegram_id
                    )
                )
                word = word.scalars().one()
                word.count_r_e = 0
                await session.commit()
        except:
            pass


#-----------------------------------------------------------------------------------------------------------------------
# База своих слов добавленных пользователем самостоятельно
class Groups(Base):
    __tablename__ = 'groups'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    user_telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    user: Mapped['User'] = relationship(back_populates='groups')

    words_self: Mapped[list['SelfWords']] = relationship(back_populates='group')

    @staticmethod
    async def add_group(
            *,
            name: str,
            user_telegram_id: int
    ):
        try:
            async with async_session as session:
                group = Groups(
                    name=name,
                    user_telegram_id=user_telegram_id
                )
                session.add(group)
                await session.commit()
        except Exception as e:
            print(e)

    @staticmethod
    async def delete_group(
            *,
            user_telegram_id: int,
            group_name: str
    ):
        try:
            async with async_session as session:
                group = await session.execute(
                    select(Groups).filter(
                        Groups.name == group_name,
                        Groups.user_telegram_id == user_telegram_id
                    )
                )
                group = group.scalars().one()
                await session.delete(group)
                await session.commit()
        except Exception as e:
            print(e)

    @staticmethod
    async def get_groups(
            *,
            user_telegram_id: int
    ):
        try:
            async with async_session as session:
                groups = await session.execute(
                    select(Groups).join(User).filter(
                        User.telegram_id == user_telegram_id
                    )
                )
                return groups.scalars().all()
        except:
            pass
# Курсор определяющий 30 слов которые сейчас изучаются
class SelfWords(Base):
    __tablename__ = 'now_self'
    id: Mapped[int] = mapped_column(primary_key=True)
    english: Mapped[str]
    russian: Mapped[str]
    count_e_r: Mapped[int]
    count_r_e: Mapped[int]

    group_name: Mapped[str] = mapped_column(ForeignKey('groups.name'))
    group: Mapped['Groups'] = relationship(back_populates='words_self')

    user_telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    user: Mapped['User'] = relationship(back_populates='words_self')

    @staticmethod
    async def add_word(
            *,
            english: str,
            russian: str,
            user_telegram_id: int,
            group_name: str
    ):
        try:
            async with async_session as session:
                word = SelfWords(
                    english=english,
                    russian=russian,
                    user_telegram_id=user_telegram_id,
                    count_e_r=0,
                    count_r_e=0,
                    group_name=group_name
                )
                session.add(word)
                await session.commit()
        except:
            pass

    @staticmethod
    async def get_first_30_words(
            *,
            user_telegram_id: int,
            group_name: str
    ):
        try:
            async with async_session as session:
                words = await session.execute(
                    select(SelfWords).join(Groups).filter(
                        Groups.name == group_name,
                        Groups.user_telegram_id == user_telegram_id
                    ).limit(30)
                )
                return words.scalars().all()
        except:
            pass

    @staticmethod
    async def get_words(
            *,
            user_telegram_id: int,
            group_name: str
    ):
        try:
            async with async_session as session:
                words = await session.execute(
                    select(SelfWords).join(Groups).filter(
                        Groups.name == group_name,
                        Groups.user_telegram_id == user_telegram_id
                    )
                )
                return words.scalars().all()
        except:
            pass

    @staticmethod
    async def delete_word(
            *,
            word
    ):
        try:
            async with async_session as session:
                word = await session.execute(
                    select(SelfWords).filter(
                        SelfWords.english == word.english,
                        SelfWords.user_telegram_id == word.user_telegram_id
                    )
                )
                word = word.scalars().one()
                await session.delete(word)
                await session.commit()
        except:
            pass

    @staticmethod
    async def plus_true_e_r(
            *,
            word
    ):
        try:
            async with async_session as session:
                word = await session.execute(
                    select(SelfWords).filter(
                        SelfWords.english == word.english,
                        SelfWords.user_telegram_id == word.user_telegram_id
                    )
                )
                word = word.scalars().one()
                word.count_e_r += 1
                await session.commit()
        except:
            pass

    @staticmethod
    async def off_true_e_r(
            *,
            word
    ):
        try:
            async with async_session as session:
                word = await session.execute(
                    select(SelfWords).filter(
                        SelfWords.english == word.english and SelfWords.user_telegram_id == word.user_telegram_id
                    )
                )
            word = word.scalars().one()
            word.count_e_r = 0
            await session.commit()
        except:
            pass

    @staticmethod
    async def plus_true_r_e(
            *,
            word
    ):
        try:
            async with async_session as session:
                word = await session.execute(
                    select(SelfWords).filter(
                        SelfWords.english == word.english and SelfWords.user_telegram_id == word.user_telegram_id
                    )
                )
                word = word.scalars().one()
                word.count_r_e += 1
                await session.commit()
        except:
            pass

    @staticmethod
    async def off_true_r_e(
            *,
            word
    ):
        try:
            async with async_session as session:
                word = await session.execute(
                    select(SelfWords).filter(
                        SelfWords.english == word.english and SelfWords.user_telegram_id == word.user_telegram_id
                    )
                )
            word = word.scalars().one()
            word.count_r_e = 0
            await session.commit()
        except:
            pass


#-----------------------------------------------------------------------------------------------------------------------
# база данных слов NOW
class Cache(Base):
    __tablename__ = 'cache'
    id: Mapped[int] = mapped_column(primary_key=True)
    english: Mapped[str]
    russian: Mapped[str]

    user_telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    user: Mapped['User'] = relationship(back_populates='cache')

    @staticmethod
    async def add_word(english: str, russian: str, user_telegram_id: int):
        try:
            async with async_session as session:
                word = Cache(english=english, russian=russian, user_telegram_id=user_telegram_id)
                session.add(word)
                await session.commit()
        except:
            pass

    @staticmethod
    async def get_words(
            *,
            user_telegram_id: int
    ):
        try:
            async with async_session as session:
                words = await session.execute(select(Cache).join(User).filter(User.telegram_id == user_telegram_id))
                return words.scalars().all()
        except:
            pass

    @staticmethod
    async def get_word(user_telegram_id: int):
        try:
            async with async_session as session:
                user = await session.execute(select(Cache).join(User).filter(User.telegram_id == user_telegram_id))
                return user.scalars().first()
        except:
            return False

    @staticmethod
    async def clean(
            *,
            user_telegram_id: int
    ):
        try:
            async with async_session as session:
                words = await Cache.get_words(
                    user_telegram_id=user_telegram_id
                )
                for i in words:
                    await session.delete(i)
                await session.commit()
        except:
            pass

    @staticmethod
    async def delete_word(
            *,
            word
    ):
        try:
            async with async_session as session:
                await session.delete(word)
                await session.commit()
        except:
            pass


class Cache_2(Base):
    __tablename__ = 'cache_2'
    id: Mapped[int] = mapped_column(primary_key=True)
    english: Mapped[str]
    russian: Mapped[str]

    user_telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    user: Mapped['User'] = relationship(back_populates='cache_2')

    @staticmethod
    async def add_word(
            *,
            english: str,
            russian: str,
            user_telegram_id: int
    ):
        try:
            async with async_session as session:
                word = Cache_2(english=english, russian=russian, user_telegram_id=user_telegram_id)
                session.add(word)
                await session.commit()
        except:
            pass

    @staticmethod
    async def get_words(
            *,
            user_telegram_id: str
    ):
        try:
            async with async_session as session:
                words = await session.execute(select(Cache_2).join(User).filter(User.telegram_id == user_telegram_id))
                return words.scalars().all()
        except:
            pass

    @staticmethod
    async def get_word(
            *,
            user_telegram_id: int
    ):
        try:
            async with async_session as session:
                words = await session.execute(select(Cache_2).join(User).filter(User.telegram_id == user_telegram_id))
                return words.scalars().first()
        except:
            return False

    @staticmethod
    async def clean(user_telegram_id: int):
        try:
            async with async_session as session:
                words = await Cache_2.get_words(
                    user_telegram_id=user_telegram_id
                )
                for i in words:
                    await session.delete(i)
                await session.commit()
        except:
            pass


#-----------------------------------------------------------------------------------------------------------------------
# функция для пересоздания баз данных
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

if __name__ == '__main__':

    asyncio.run(init_db())