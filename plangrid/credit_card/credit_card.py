from abc import abstractmethod
import unittest


class BaseCard:
    @staticmethod
    @abstractmethod
    def match(number):
        pass


class Visa(BaseCard):
    @staticmethod
    def match(number):
        if 40 <= int(number[0:2]) <= 42 and len(number) == 16:
            return True


class Master(BaseCard):
    @staticmethod
    def match(number):
        if 42 <= int(number[0:2]) <= 44 and len(number) >= 15:
            return True


def detect_card_type(number):
    cards = [
        Visa,
        Master,
    ]
    matches = []
    for card in cards:
        if card.match(number=number):
            matches.append(card.__name__)
    return matches


class TestCreditCard(unittest.TestCase):
    def test_none(self):
        self.assertEqual(detect_card_type("1234567890123456"), [])

    def test_visa(self):
        self.assertEqual(detect_card_type("4034567890123456"), ["Visa"])
        self.assertEqual(detect_card_type("42345678901234"), [])
        self.assertEqual(detect_card_type("3234567890123456"), [])

    def test_master(self):
        self.assertEqual(detect_card_type("4434567890123456"), ["Master"])
        self.assertCountEqual(detect_card_type("4234567890123456"), ["Master", "Visa"])


if __name__ == "__main__":
    unittest.main()
