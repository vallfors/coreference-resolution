import stanza
from stanza.server import CoreNLPClient
import os

class FeatureUtils:
    stanza_initialized = False

    def init_stanza(self):
        if self.stanza_initialized:
            return

        corenlp_dir = './corenlp'
        if not os.path.isdir(corenlp_dir):
            stanza.install_corenlp(dir=corenlp_dir)
        
        try:
            with CoreNLPClient(
                annotators=['tokenize', 'ssplit', 'pos', 'lemma', 'ner', 'parse', 'depparse', 'coref'],
                timeout=30000,
                memory='16G',
                be_quiet=True) as client:
                self.client = client
                self.stanza_initialized = True
        except AssertionError as e:
            print("Du har förmodligen inte ställt in $CORENLP_HOME. Kör detta:")
            print("export CORENLP_HOME={}".format(os.path.abspath(corenlp_dir)))
            raise e


    # Returns head word object from text string.
    def headword_from_string(self, s):
        word = {
                'headword': '', 
                'pos_tag': '', 
                'position': '', 
                'gender': '', 
                'number': '',
                'animacy': '',
                'person': '',
                'named_entity': ''
        }
        ann = self.client.annotate(s)
        sent = ann.sentence[0]
        if len(sent.mentionsForCoref) > 0:
            coref = sent.mentionsForCoref[0]
            word['headword'] = coref.headString
            word['position'] = coref.headIndex
            word['gender'] = coref.gender
            word['number'] = coref.number
            word['animacy'] = coref.animacy
            word['person'] = coref.person
            word['named_entity'] = coref.nerString
            for token in sent.token:
                if token.beginIndex == coref.headIndex:
                    word['pos_tag'] = token.pos
        return word

