import unittest
from flash_cards.flash_cards import FlashCards


class FlashCardsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.fc = FlashCards('words.txt')

    def tearDown(self) -> None:
        del self.fc

    def test_delete_word_in_dict(self):
        self.assertEqual("Successfully deleted word 'яблоко'.", self.fc.delete_word('яблоко'))

    def test_delete_word_not_in_dict(self):
        self.assertEqual("'банан' not in dictionary.", self.fc.delete_word('банан'))

    def test_delete_word_wrong_lang(self):
        self.assertEqual("Please enter russian word that in dictionary", self.fc.delete_word('sorry'))

    def test_delete_word_wrong_type(self):
        self.assertEqual("Please enter russian word that in dictionary", self.fc.delete_word(135))

    def test_delete_word_empty_input(self):
        self.assertEqual("Please enter russian word that in dictionary", self.fc.delete_word(''))
