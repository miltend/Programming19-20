import unittest
from flash_cards.flash_cards import FlashCards


class FlashCardsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.fc = FlashCards('words.txt')

    def tearDown(self) -> None:
        del self.fc

    def test_add_word_new_word(self):
        self.assertEqual("Successfully added word 'тыква'.", self.fc.add_word('тыква', 'pumpkin'))

    def test_add_word_already_in_dictionary(self):
        self.assertEqual("'яблоко' already in dictionary.", self.fc.add_word('яблоко', 'apple'))

    def test_add_word_first_lang(self):
        self.assertEqual("Please enter in format ('russian word', 'english word')",
                         self.fc.add_word('yabloko', 'apple'))

    def test_add_word_second_lang(self):
        self.assertEqual("Please enter in format ('russian word', 'english word')",
                         self.fc.add_word('яблоко', 'эпл'))

    def test_add_word_wrong_type(self):
        self.assertEqual("Please enter in format ('russian word', 'english word')",
                         self.fc.add_word(315, 'food'))

    def test_add_word_empty_input(self):
        self.assertEqual("Please enter in format ('russian word', 'english word')",
                         self.fc.add_word('', ''))