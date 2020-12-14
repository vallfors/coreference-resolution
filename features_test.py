import unittest
from preprocessing.featureUtils import *
from preprocessing.mention import *
from preprocessing.features import *

class TestFeatures(unittest.TestCase):
    feature_utils = FeatureUtils()
    feature_utils.init_stanza()

    def simple_mention_from_string(self, s):
        s_list = s.split()
        m = Mention(0, s_list[0], 0)
        for i in range (1, len(s_list)):
            m.append_word(s_list[i])
        m.calculate_headword(self.feature_utils)
        return m

    def test_animacy(self):
        m_book = self.simple_mention_from_string("the book")
        m_wife = self.simple_mention_from_string("my wife")
        m_lawyer = self.simple_mention_from_string("a successful lawyer")

        # The wife is animate, the book is not
        self.assertEqual(animacy(m_book, m_wife), INCOMPATIBLE)
        # Both the lawyer and the wife are animate
        self.assertEqual(animacy(m_lawyer, m_wife), COMPATIBLE)

    def test_pronoun_1(self):
        m_you = self.simple_mention_from_string("you")
        m_concert = self.simple_mention_from_string("my favorite concert")

        self.assertEqual(pronoun_1(m_you, m_concert), YES)
        self.assertEqual(pronoun_1(m_concert, m_you), NO)

    def test_pronoun_2(self):
        m_he = self.simple_mention_from_string("he")
        m_dress = self.simple_mention_from_string("your blue dress")

        self.assertEqual(pronoun_2(m_he, m_dress), NO)
        self.assertEqual(pronoun_2(m_dress, m_he), YES)        


    def test_definite_2(self):
        m_the_dog = self.simple_mention_from_string("the cute dog")
        m_ribbon = self.simple_mention_from_string("a ribbon on the dress")

        self.assertEqual(definite_2(m_the_dog, m_ribbon), NO)
        self.assertEqual(definite_2(m_ribbon, m_the_dog), YES)

    def test_demonstrative_2(self):
        m_this_dog = self.simple_mention_from_string("this dog")
        m_those_houses = self.simple_mention_from_string("those houses")
        m_kittens = self.simple_mention_from_string("cute kittens")

        self.assertEqual(demonstrative_2(m_this_dog, m_those_houses), YES)
        self.assertEqual(demonstrative_2(m_this_dog, m_kittens), NO)
        self.assertEqual(demonstrative_2(m_kittens, m_this_dog), YES)

    def test_number(self):
        m_students = self.simple_mention_from_string("university students")
        m_kitten = self.simple_mention_from_string("a tiny kitten")
        m_cake = self.simple_mention_from_string("a slice of chocolate cake")

        self.assertEqual(number(m_students, m_kitten), INCOMPATIBLE)
        self.assertEqual(number(m_kitten, m_cake), COMPATIBLE)
    
    def test_gender(self):
        m_woman = self.simple_mention_from_string("a woman")
        m_he = self.simple_mention_from_string("he")
        m_she = self.simple_mention_from_string("she")

        self.assertEqual(gender(m_woman, m_he), INCOMPATIBLE)
        self.assertEqual(gender(m_woman, m_she), COMPATIBLE)

    def test_both_proper_nouns(self):
        m_alice = self.simple_mention_from_string("Alice")
        m_portugal = self.simple_mention_from_string("Portugal")
        m_puppy = self.simple_mention_from_string("a puppy")
        m_cat = self.simple_mention_from_string("a cat")

        self.assertEqual(both_proper_nouns(m_alice, m_portugal), COMPATIBLE)
        self.assertEqual(both_proper_nouns(m_portugal, m_puppy), NOT_APPLICABLE)
        self.assertEqual(both_proper_nouns(m_cat, m_puppy), INCOMPATIBLE)


if __name__ == '__main__':
    unittest.main()