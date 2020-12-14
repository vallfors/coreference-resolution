def sieve_one(m_i, m_j):
    """ the number of mentions between m_i and m_j is not greater than a given parameter """
    parameter = 8
    if abs(m_i.id - m_j.id) <= parameter:
        return True
    return False

def sieve_two(m_i, m_j):
    """ m_j is an alias of m_i """
    return False

def sieve_three(m_i, m_j):
    """ there is a match of both mentions strings up to their head words """
    for i in range(len(m_i.words)):
        if len(m_j.words) > i:
            if m_i.words[i].lower() == m_i.headword and m_j.words[i].lower() == m_j.headword:
                return True
            elif m_i.words[i].lower() == m_i.headword or m_j.words[i].lower() == m_j.headword:
                return False
            elif m_i.words[i].lower() != m_j.words[i].lower():
                return False
        else:
            return False
    return False

def sieve_four(m_i, m_j):
    """ the head word of m_i matches the head word of m_j """
    if m_i.headword == m_j.headword:
        return True 
    return False

def sieve_five(m_i, m_j):
    """ test shallow discourse attributes match for both mentions """
    return False

def sieve_six(m_i, m_j):
    """ m_j is a pronoun and m_i has the same gender, number, (speaker (add later maybe)) and animacy of m_j """
    personal_pronoun = "PRP"
    possessive_pronoun = "PRP$"
    if ((m_j.headword_pos_tag == personal_pronoun or m_j.headword_pos_tag == possessive_pronoun) and 
        m_i.headword_gender == m_j.headword_gender and 
        m_i.headword_gender != 'UNKNOWN' and
        m_i.headword_number == m_j.headword_number and 
        m_i.headword_number != 'UNKNOWN' and
        m_i.headword_animacy == m_j.headword_animacy and
        m_i.headword_animacy != 'UNKNOWN'):
        return True
    return False