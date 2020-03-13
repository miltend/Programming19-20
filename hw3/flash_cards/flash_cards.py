import json
import random
import re


class FlashCards():
    def __init__(self, path_to_file: str):
        """
        Прочитает пары слов из указанного файла в формате json.
        Создаст все требующиеся атрибуты.
        """

        with open(path_to_file, 'r') as f:
            self.__ru_en_words = json.loads(f.read())
        self._words = list(self.__ru_en_words)

    def play(self) -> str:
        """
        Выдает русские слова из словаря в рандомном порядке,
        сверяет введенный пользователем перевод с правильным
        (регистр введенного слова при этом не важен),
        пока слова в словаре не закончатся.
        Возвращает строку с количеством правильных ответов/общим количеством
        слов в словаре (см пример работы).
        """
        if len(self._words) == 0:
            return "Dictionary is empty!"
        i = 0
        corr_answers = 0
        random.shuffle(self._words)
        while i < len(self._words):
            rand_word = self._words[i]
            print(rand_word)
            user_inp = input().lower()
            if user_inp == self.__ru_en_words[rand_word]:
                corr_answers += 1
            i += 1
        return "Done! {} of {} words correct.".format(corr_answers, len(self.__ru_en_words))

    def add_word(self, russian: str, english: str) -> str:
        """
        Добавляет в словарь новую пару слов,
        если русского слова еще нет в словаре.
        Возвращает строку в зависимоти от результата (см пример работы).
        """
        try:
            russian = russian.lower()
            english = english.lower()
            if not re.search('[а-я]+', russian) or not re.search('[a-z]+', english):
                return "Please enter in format ('russian word', 'english word')"
            if russian not in self.__ru_en_words:
                self.__ru_en_words[russian] = english
                self._words = list(self.__ru_en_words)
                return "Successfully added word '{}'.".format(russian)
            else:
                return "'{}' already in dictionary.".format(russian)
        except (TypeError, AttributeError):
            return "Please enter in format ('russian word', 'english word')"

    def delete_word(self, russian: str) -> str:
        """
        Удаляет из словаря введенное русское слово
        и соответсвующее ему английское.
        Возвращает строку в зависимоти от результата (см пример работы).
        """
        if type(russian) != str or not re.search('[а-я]+', russian):
            return "Please enter russian word that in dictionary"
        deleting = self.__ru_en_words.pop(russian, None)
        if deleting is not None:
            self._words = list(self.__ru_en_words)
            return "Successfully deleted word '{}'.".format(russian)
        else:
            return "'{}' not in dictionary.".format(russian)
