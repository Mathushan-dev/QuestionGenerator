from collections import OrderedDict
from sense2vec import Sense2Vec
import random
import string
import os

s2v = Sense2Vec().from_disk(os.path.abspath("../QuestionGenerator/s2v_old"))


def generateMisspellings(answer):
    misspelt = []
    for x in range(0, 10):
        ix = random.choice(range(len(answer)))
        new_word = ''.join([answer[w] if w != ix else random.choice(string.ascii_letters) for w in range(len(answer))])
        misspelt.append(new_word)

    return misspelt


def generateChoices(word, totalChoicesRequired):
    answer = word
    global s2v
    choices = []
    word = word.lower().replace(" ", "_")

    sense = s2v.get_best_sense(word)
    if sense is None:
        misspellings = generateMisspellings(answer)
        return getRandomChoices(misspellings, answer, totalChoicesRequired)

    mostSimilarWord = s2v.most_similar(sense, n=20)

    for option in mostSimilarWord:
        distractor = option[0].split("|")[0].replace("_", " ").lower()
        if distractor.lower().strip() != word.lower().strip():
            choices.append(distractor.title().lower())

    return getRandomChoices(list(OrderedDict.fromkeys(choices)), answer, totalChoicesRequired)


# Using random ensures multiple users will get different possible choices for mcq's
def getRandomChoices(choices, answer, totalChoicesRequired):
    shuffledDistractors = random.sample(choices, totalChoicesRequired - 1)
    shuffledDistractors.insert(random.randrange(len(shuffledDistractors) + 1), answer.lower())
    return shuffledDistractors


if __name__ == "__main__":
    print(generateChoices("monkey", 4))
