import unittest
from flash_cards.flash_cards import FlashCards
from unittest import mock


class FlashCardsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.fc = FlashCards('words.txt')

    def tearDown(self) -> None:
        del self.fc

    def test_check_word_in_dict(self):
        self.fc.add_word('тыква', 'pumpkin')
        self.assertIn('тыква', self.fc._FlashCards__ru_en_words)

    def test_play_empty_dict(self):
        self.fc.delete_word('яблоко')
        self.fc.delete_word('помидор')
        self.assertEqual("Dictionary is empty!", self.fc.play())

    @mock.patch('flash_cards.flash_cards.input')
    def test_play_not_empty_dict(self, mocked_input):
        self.fc.delete_word('яблоко')
        mocked_input.side_effect = 'tomato'
        self.assertNotEqual("Dictionary is empty!", self.fc.play())

    @mock.patch('flash_cards.flash_cards.input')
    @mock.patch('flash_cards.flash_cards.random.shuffle')
    def test_fc_success_play(self, shuffle_mock, mocked_input):
        mocked_input.side_effect = ['apple', 'tomato']

        def shuffle_mock_imp(lst):
            lst[:] = ['яблоко', 'помидор']

        shuffle_mock.side_effect = shuffle_mock_imp
        result = self.fc.play()
        self.assertEqual("Done! 2 of 2 words correct.", result)

    @mock.patch('flash_cards.flash_cards.input')
    @mock.patch('flash_cards.flash_cards.random.shuffle')
    def test_fc_play_zero_correct_answers(self, shuffle_mock, mocked_input):
        mocked_input.side_effect = ['eple', 'tomoto']

        def shuffle_mock_imp(lst):
            lst[:] = ['яблоко', 'помидор']

        shuffle_mock.side_effect = shuffle_mock_imp
        result = self.fc.play()
        self.assertEqual("Done! 0 of 2 words correct.", result)

    @mock.patch('flash_cards.flash_cards.input')
    @mock.patch('flash_cards.flash_cards.random.shuffle')
    def test_fc_play_one_correct_answer(self, shuffle_mock, mocked_input):
        mocked_input.side_effect = ['tomato', 'apel']

        def shuffle_mock_imp(lst):
            lst[:] = ['помидор', 'яблоко']

        shuffle_mock.side_effect = shuffle_mock_imp
        result = self.fc.play()
        self.assertEqual("Done! 1 of 2 words correct.", result)