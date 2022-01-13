import nltk

nltk.download('wordnet')

from nltk.corpus import wordnet
import random


def generateChoices(word, totalChoicesRequired):
    syns = generateSynset(word)
    syn = selectValidSyn(syns, word)
    choices = generateDistractors(syn, word)
    requiredChoices = getRandomChoices(choices, totalChoicesRequired)
    requiredChoices.append(word)
    return requiredChoices


def generateSynset(word):
    word = word.lower()
    syns = wordnet.synsets(word)

    return syns


def selectValidSyn(syns, word):
    # todo using syns[0] because assumption of the word's definition is made (need to distinguish correct definition)
    syn = syns[0]
    return syn


def generateDistractors(syn, word):
    distractors = []
    word = word.lower()
    word = word.replace(" ", "_")

    hypernyms = syn.hypernyms()
    if len(hypernyms) == 0:
        return distractors

    # todo using hypernyms[0] because assumption of the word's hypernym is made (need to distinguish correct hypernym)
    for hyponym in hypernyms[0].hyponyms():
        distractor = hyponym.lemmas()[0].name()
        if distractor == word:
            continue
        if distractor is not None and distractor not in distractors:
            distractors.append(distractor)

    return distractors


# Using random ensures multiple users will get different possible choices for mcq's
def getRandomChoices(choices, totalChoicesRequired):
    return random.sample(choices, totalChoicesRequired - 1)


print(generateChoices("machine learning", 4))
# todo some words may not appear in wordnet: catch errors and provide alternative way of generating distractors - (wikileaks)
# todo talk about weaknesses of using wordnet and why alternative was chosen