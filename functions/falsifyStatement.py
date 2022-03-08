import re
import string
import nltk
import scipy
import spacy
from nltk import tokenize
from sentence_transformers import SentenceTransformer
from tensorboard.errors import InvalidArgumentError
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer

nltk.download('punkt')
nlp = spacy.load("en_core_web_sm")
# The model below an All-round model tuned for many use-cases. Trained on a large and diverse dataset of over 1
# billion training pairs.
BERTModel = SentenceTransformer('sentence-transformers/distilbert-base-nli-stsb-mean-tokens')


def replace_last(string_to_replace, find, replace):
    """
    todo
    :param string_to_replace:
    :param find:
    :param replace:
    :return: Any
    """
    reversed_string = string_to_replace[::-1]
    replaced = reversed_string.replace(find[::-1], replace[::-1], 1)
    return replaced[::-1]


def correct_spaces(string_to_correct):
    """
    todo
    :param string_to_correct:
    :return: str
    """
    return re.sub(' +', ' ', string_to_correct)


def activate_top_k_p_sampling(model, input_ids, maximum_length_statement):
    """

    :param model:
    :param input_ids:
    :param maximum_length_statement:
    :return: Any
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
    todo
    :param sample_ouputs:
    :param tokeniser:
    :return: list
    """
    generated_sentences = []
    for i, sampleOutput in enumerate(sample_ouputs):
        decoded_sentence = tokeniser.decode(sampleOutput, skip_special_tokens=True)
        final_sentence = tokenize.sent_tokenize(decoded_sentence)[0]
        generated_sentences.append(final_sentence)
    return generated_sentences


def element1(x):
    """
    todo
    :param x:
    :return: Any
    """
    return x[1]


def find_final_false_statement(docs, query):
    """
    todo
    :param docs:
    :param query:
    :return: Optional[Any]
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
    todo
    :param incomplete_right_most_p_statement:
    :param original_statement:
    :return: Optional[{split}]
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
    todo
    :param original_statement:
    :return: str
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
    todo
    :param original_statement:
    :return: Any
    """
    return original_statement.translate(str.maketrans('', '', string.punctuation))


if __name__ == "__main__":
    print(falsify_statement("Tom walked to the park"))
