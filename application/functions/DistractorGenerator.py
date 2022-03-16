from collections import OrderedDict
from sense2vec import Sense2Vec
import random
import string
import os

s2v = Sense2Vec().from_disk(os.path.abspath("../project/QuestionGenerator/s2v_old"))


def generate_misspellings(answer):
    """
    This method randomly picks a character and substitute it with a random letter
    :param answer: the answer of a question
    :return: the list with new 10 misspelling words
    """
    misspelt = []
    for _ in range(0, 10):
        ix = random.choice(range(len(answer)))
        new_word = ''.join([answer[w] if w != ix else random.choice(string.ascii_letters) for w in range(len(answer))])
        misspelt.append(new_word)

    return misspelt


def generate_choices(word, total_choices_required):
    """
    This method generate the options of the question.
    It takes the sense of the word and create most similar n(20) words,
    append them to the choices.If no sense, create misspelling words instead.
    :param word: the answer of the question
    :param total_choices_required: number of options to generate
    :return: function call get_random_choices , which returns a list of choices
    """
    answer = word
    global s2v
    choices = []
    word = word.lower().replace(" ", "_")

    sense = s2v.get_best_sense(word)
    if sense is None:
        misspellings = generate_misspellings(answer)
        return get_random_choices(misspellings, answer, total_choices_required)

    most_similar_word = s2v.most_similar(sense, n=20)

    for option in most_similar_word:
        distractor = option[0].split("|")[0].replace("_", " ").lower()
        if distractor.lower().strip() != word.lower().strip():
            choices.append(distractor.title().lower())

    try:
        return get_random_choices(list(OrderedDict.fromkeys(choices)), answer, total_choices_required)
    except ValueError:
        misspellings = generate_misspellings(answer)
        return get_random_choices(misspellings, answer, total_choices_required)


# Using random ensures multiple users will get different possible choices for mcq's
def get_random_choices(choices, answer, total_choices_required):
    """
    This method shuffle the distractors.
    :param choices: choices of question
    :param answer: answer of question
    :param total_choices_required: total choices required
    :return: list of the shuffled distractors
    """
    filtered_choices = []
    for choice in choices:
        if answer not in choice and choice not in answer:
            filtered_choices.append(choice)
    shuffled_distractors = random.sample(filtered_choices, total_choices_required - 1)
    shuffled_distractors.insert(random.randrange(len(shuffled_distractors) + 1), answer.lower())
    return shuffled_distractors
