import random
import nltk

nltk.download('averaged_perceptron_tagger')


def findRandomKeyword(text):
    is_noun = lambda pos: pos[:2] == 'NN'
    tokenized = nltk.word_tokenize(text)
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]
    if nouns[-1] is None:
        return text[-1]
    return nouns[-1]


if __name__ == "__main__":
    print(findRandomKeyword("The cheetah is the fastest land animal on earth."))
