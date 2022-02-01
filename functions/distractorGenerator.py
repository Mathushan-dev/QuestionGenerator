from collections import OrderedDict
from sense2vec import Sense2Vec
import random
import os
s2v = Sense2Vec().from_disk(os.path.abspath("../QuestionGenerator/s2v_old"))

def generateChoices(word, totalChoicesRequired):
    answer = word
    global s2v
    choices = []
    word = word.lower().replace(" ", "_")

    sense = s2v.get_best_sense(word)
    mostSimilarWord = s2v.most_similar(sense, n=20)

    for option in mostSimilarWord:
        distractor = option[0].split("|")[0].replace("_", " ").lower()
        if distractor.lower() != word.lower():
            choices.append(distractor.title())


    return getRandomChoices(list(OrderedDict.fromkeys(choices)), answer, totalChoicesRequired)

# Using random ensures multiple users will get different possible choices for mcq's
def getRandomChoices(choices, answer, totalChoicesRequired):
    shuffledDistractors = random.sample(choices, totalChoicesRequired - 1)
    shuffledDistractors.insert(random.randrange(len(shuffledDistractors) + 1), answer)
    return shuffledDistractors


if __name__ == "__main__":
    print(generateChoices("monkey", 4))
