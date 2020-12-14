import numpy

# Return value constants
INCOMPATIBLE = 0.0
COMPATIBLE = 1.0
NOT_APPLICABLE = -1.0
YES = 1.0
NO = 0.0


"""--------------------Lexical--------------------"""
def string_matching_headword(m_i, m_j):
    if m_i.headword == m_j.headword:
        return YES 
    else: 
        return NO

def pronouns_and_string_match(m_i, m_j):
    personal_pronoun = "PRP"
    possessive_pronoun = "PRP$"
    if ((m_i.headword_pos_tag == personal_pronoun or m_i.headword_pos_tag == possessive_pronoun) and 
        (m_j.headword_pos_tag == personal_pronoun or m_j.headword_pos_tag == possessive_pronoun) and 
        len(m_i.words) == len(m_j.words)):
        for i in range(len(m_i.words)):
            if m_i.words[i] != m_j.words[i]:
                return NO
        return YES
    return NO

def edit_distance_headword(m_i, m_j):
    x = m_i.headword
    y = m_j.headword
    D = numpy.zeros((len(x)+1, len(y)+1), dtype=int)
    D[0, 1:] = range(1, len(y)+1)
    D[1:, 0] = range(1, len(x)+1)
    for i in range(1, len(x)+1):
        for j in range(1, len(y)+1):
            delt = 1 if x[i-1] != y[j-1] else 0
            D[i, j] = min(D[i-1, j-1]+delt, D[i-1, j]+1, D[i, j-1]+1)
    return D[len(x), len(y)] # / max(len(x), len(y)) #normalized

def proper_names_and_string_match(m_i, m_j):
    proper_name_singular = "NNP"
    proper_name_plural = "NNPs"
    if ((m_i.headword_pos_tag == proper_name_singular or m_i.headword_pos_tag == proper_name_plural) and 
        (m_j.headword_pos_tag == proper_name_singular or m_j.headword_pos_tag == proper_name_plural) and 
        len(m_i.words) == len(m_j.words)):
        for i in range(len(m_i.words)):
            if m_i.words[i] != m_j.words[i]:
                return NO
        return YES
    return NO

"""-------------------Syntactic-------------------"""
def both_proper_names_or_pronouns(m_i, m_j):
    personal_pronoun = "PRP"
    possessive_pronoun = "PRP$"
    proper_name_singular = "NNP"
    proper_name_plural = "NNPs"
    if ((m_i.headword_pos_tag == proper_name_singular or m_i.headword_pos_tag == proper_name_plural) and 
        (m_j.headword_pos_tag == proper_name_singular or m_j.headword_pos_tag == proper_name_plural)):
        return YES
    if ((m_i.headword_pos_tag == personal_pronoun or m_i.headword_pos_tag == possessive_pronoun) and 
        (m_j.headword_pos_tag == personal_pronoun or m_j.headword_pos_tag == possessive_pronoun)):
        return YES
    return NO

def compatible_pronouns(m_i, m_j):
    personal_pronoun = "PRP"
    possessive_pronoun = "PRP$"
    if ((m_i.headword_pos_tag == personal_pronoun or m_i.headword_pos_tag == possessive_pronoun) and 
        (m_j.headword_pos_tag == personal_pronoun or m_j.headword_pos_tag == possessive_pronoun) and 
        m_i.headword_gender == m_j.headword_gender and 
        m_i.headword_gender != 'UNKNOWN' and
        m_i.headword_number == m_j.headword_number and 
        m_i.headword_number != 'UNKNOWN' and
        m_i.headword_person == m_j.headword_person and
        m_i.headword_person != 'UNKNOWN'):
        return YES
    return NO

"""--------------------Semantic-------------------"""
def same_named_entity(m_i, m_j):
    if (m_i.headword_named_entity == m_j.headword_named_entity and
        m_i.headword_named_entity != 'UNKNOWN'):
        return YES
    return NO

"""-------------Distance and Position-------------"""

def distance_sentences(m_i, m_j):
    return abs(m_i.sentence - m_j.sentence)

def distance_mentions(m_i, m_j):
    """ the number of mentions between m_i and m_j """
    return abs(m_i.id - m_j.id)


"""----------------From Ng and Cardie-------------------"""

"""--------------Soon original features-----------------"""

#TODO: All these features are based on the description in Ng and Cardie,
# and can probably be improved by reading the original descriptions in Soon

#TODO: Soon string feature

# Whether the first mention is a pronoun
def pronoun_1(m_i, m_j):
    personal_pronoun = "PRP"
    possessive_pronoun = "PRP$" # Probably should be skipped?
    if (m_i.headword_pos_tag == personal_pronoun or m_i.headword_pos_tag == possessive_pronoun):
        return YES
    else:
        return NO

# Whether the second mention is a pronoun
def pronoun_2(m_i, m_j):
    personal_pronoun = "PRP"
    possessive_pronoun = "PRP$" # Probably should be skipped?
    if (m_j.headword_pos_tag == personal_pronoun or m_j.headword_pos_tag == possessive_pronoun):
        return YES
    else:
        return NO

# The second mention is definite
def definite_2(m_i, m_j):
    if m_j.words[0] == "the":
        return YES
    else:
        return NO

def number(m_i, m_j):
    if m_i.headword_number == m_j.headword_number:
        return COMPATIBLE
    else:
        return INCOMPATIBLE

def gender(m_i, m_j):
    if m_i.headword_gender == m_j.headword_gender:
        return COMPATIBLE
    else:
        return INCOMPATIBLE

# The second mention is demonstrative
def demonstrative_2(m_i, m_j):
    demonstrative_pronouns = ["this", "that", "these","those"]
    if m_j.words[0] in demonstrative_pronouns:
        return YES
    else:
        return NO

def both_proper_nouns(m_i, m_j):
    proper_name_singular = "NNP"
    proper_name_plural = "NNPs"
    m_i_proper_name = False
    m_j_proper_name = False
    if m_i.headword_pos_tag == proper_name_singular or m_i.headword_pos_tag == proper_name_plural:
        m_i_proper_name = True
    if m_j.headword_pos_tag == proper_name_singular or m_j.headword_pos_tag == proper_name_plural:
        m_j_proper_name = True
    
    if m_i_proper_name and m_j_proper_name:
        return COMPATIBLE
    elif not m_i_proper_name and not m_j_proper_name:
        return INCOMPATIBLE # Why are Incompatible and not applicable not reversed?
    else:
        return NOT_APPLICABLE

    #TODO: Appositive. Is it worth implementing?
    # Wordnet class. Probably just skip this one.
    #TODO: Alias. Can be added at the same time as the alias sieve.
    # Sentnum: Already implemented as distance_sentences above

"""--------------Grammatical---------------------"""
def animacy(m_i, m_j):
    if m_i.headword_animacy == m_j.headword_animacy:
        return COMPATIBLE
    else:
        return INCOMPATIBLE


basic_features = [string_matching_headword, pronouns_and_string_match, proper_names_and_string_match,
    both_proper_names_or_pronouns, compatible_pronouns, same_named_entity,
    pronoun_1, pronoun_2, definite_2, number, gender, demonstrative_2, both_proper_nouns, animacy,
    edit_distance_headword, distance_mentions, distance_sentences]