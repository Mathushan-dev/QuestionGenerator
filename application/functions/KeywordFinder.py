import nltk

nltk.download('averaged_perceptron_tagger')


def find_random_keyword(text):
    """
    This method finds a random noun word in the text
    :param text: text to generate question
    :return: Any
    """
    is_noun = lambda pos: pos[:2] == 'NN'
    tokenized = nltk.word_tokenize(text)
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]
    if nouns is None:
        return text[-1]
    if len(nouns) < 1:
        return text[-1]
    return nouns[-1]