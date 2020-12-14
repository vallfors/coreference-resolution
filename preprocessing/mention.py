from .featureUtils import *

class Mention():
    def __init__(self, id, word, sentence, start_position):
        self.id = id
        self.sentence = int(sentence)
        # Start and end positions within sentence. 1-indexed.
        self.start_position = int(start_position)
        self.end_position = int(start_position) # To be updated
        self.words = [word]
        self.headword = ''
        # Universal POS-tag (upos in Stanza)
        self.headword_pos_tag = ''
        # Position in the mention
        self.headword_position = -1
        self.headword_gender = ''
        self.headword_number = ''
        self.headword_animacy = ''
        self.headword_person = ''
        self.headword_named_entity = ''
    
    def append_word(self, word):
        self.words.append(word)

    def set_headword(self, headword):
        self.headword = headword

    def update_id(self, id):
        self.id = id

    def set_end_position(self, end_position):
        self.end_position = end_position

    def calculate_headword(self, f):
        s = " ".join(self.words)
        word = f.headword_from_string(s)
        self.headword = word['headword']
        self.headword_pos_tag = word['pos_tag']
        self.headword_position = word['position'] if word['position'] != '' else -1
        self.headword_gender = word['gender']
        self.headword_number = word['number']
        self.headword_animacy = word['animacy']
        self.headword_person = word['person']
        self.headword_named_entity = word['named_entity']

        
    def __str__(self):
        s = "Mention with id " + str(self.id) + " in sentence " + str(self.sentence) + " is " + " ".join(self.words) + ". Headword: " + self.headword
        return s