import re
import string
import nltk
import scipy
import spacy
from nltk import tokenize
from sentence_transformers import SentenceTransformer
from tensorboard.errors import InvalidArgumentError
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer

# The model below an All-round model tuned for many use-cases. Trained on a large and diverse dataset of over 1
# billion training pairs.
BERTModel = SentenceTransformer('sentence-transformers/distilbert-base-nli-stsb-mean-tokens')


def replace_last(string_to_replace, find, replace):
    """
    This method finds the last word of the string and replace it
    For example,calling replace_last("one one two three four one one", "one","haha") would get
    one one two three four one haha
    :param string_to_replace: the original string
    :param find: the target string to be replaced
    :param replace: the string to replace in
    :return: return the replaced string
    """
    reversed_string = string_to_replace[::-1]
    replaced = reversed_string.replace(find[::-1], replace[::-1], 1)
    return replaced[::-1]


def correct_spaces(string_to_correct):
    """
    This method format the space in a string ,only allowing one space between words
    :param string_to_correct: original string
    :return: space formatted string
    """
    return re.sub(' +', ' ', string_to_correct)


def activate_top_k_p_sampling(model, input_ids, maximum_length_statement):
    """
    This method generate 5 independent sequences using sampling
    :param model: the pretrained model
    :param input_ids: The sequence used as a prompt for the generation.
    :param maximum_length_statement: The maximum length of the sequence to be generated.
    :return: generated samples
    """
    return model.generate(
        input_ids,
        do_sample=True,
        max_length=maximum_length_statement,
        top_p=0.9,
        top_k=20,
        repetition_penalty=20.0,
        num_return_sequences=5
    )


def generate_sentences(sample_ouputs, tokeniser):
    """
    This method first transform the tokens to string and put into a list
    :param sample_ouputs: sample tokens
    :param tokeniser: tokeniser from pretrained model to decode the tokens
    :return:  list of  generated sentences
    """
    generated_sentences = []
    for i, sampleOutput in enumerate(sample_ouputs):
        decoded_sentence = tokeniser.decode(sampleOutput, skip_special_tokens=True)
        final_sentence = tokenize.sent_tokenize(decoded_sentence)[0]
        generated_sentences.append(final_sentence)
    return generated_sentences


def element1(x):
    """
    :param x: list
    :return: element index at 1
    """
    return x[1]


def find_final_false_statement(docs, query):
    """
    This method finds the false statement by using scipy to calculate
    the distance of vectors of the statements.
    :param docs: the generated statements, call docs
    :param query: the orginal statment, call query
    :return: return the list of dissimilar statements.
    """
    doc_embeddings = BERTModel.encode(docs)
    query_embeddings = BERTModel.encode([query])
    scores = \
        scipy.spatial.distance.cdist(query_embeddings, doc_embeddings, "cosine")[0]
    doc_score_pairs = zip(range(len(scores)), scores)
    doc_score_pairs = sorted(doc_score_pairs, key=element1)
    dissimilar_statements = []
    for index, distance in doc_score_pairs:
        dissimilar_statements.append(docs[index])
    try:
        return dissimilar_statements[len(dissimilar_statements) % 2]
    except IndexError:
        return None


def complete_right_most_p_statement(incomplete_right_most_p_statement, original_statement):
    """
    This method generate the statements of incomplete right most statements,
    by first finding top_k sampling tokens and transform in sentences.Finally call
    the find_final_false_statement function.
    :param incomplete_right_most_p_statement: a list of the incomplete statements
    :param original_statement: original statement
    :return: return function call of find_final_false_statement
    """
    tokeniser = GPT2Tokenizer.from_pretrained("gpt2")
    model = TFGPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokeniser.eos_token_id)
    input_ids = tokeniser.encode(incomplete_right_most_p_statement, return_tensors='tf')
    maximum_length_statement = len(incomplete_right_most_p_statement.split()) + 10  #
    try:
        sample_outputs = activate_top_k_p_sampling(model, input_ids, maximum_length_statement)
        generated_statements = generate_sentences(sample_outputs, tokeniser)
    except InvalidArgumentError:
        return incomplete_right_most_p_statement
    return find_final_false_statement(generated_statements, original_statement)


def falsify_statement(original_statement):
    """
    This method breaks the original statement into cleaned incomplete statement and return
    the falsified statement by calling other functions
    :param original_statement: original statement
    :return: falsified statement
    """
    cleaned_original_statement = clean_up_statement(original_statement)
    statement_length = len(cleaned_original_statement.split(" "))
    incomplete_statement = ""
    for i in range(0, statement_length):
        if i < statement_length - 1:
            incomplete_statement += (cleaned_original_statement.split(" ")[i]) + " "
    return correct_spaces(complete_right_most_p_statement(incomplete_statement.strip(), original_statement))


def clean_up_statement(original_statement):
    """
    This method cleans up the punctuation
    :param original_statement: original sentences
    :return: cleaned statement
    """
    return original_statement.translate(str.maketrans('', '', string.punctuation))
