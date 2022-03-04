import re
import string
import nltk
import scipy
import spacy
from nltk import tokenize
from sentence_transformers import SentenceTransformer
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer

nltk.download('punkt')
nlp = spacy.load("en_core_web_sm")
# The model below an All-round model tuned for many use-cases. Trained on a large and diverse dataset of over 1 billion training pairs.
BERTModel = SentenceTransformer('sentence-transformers/distilbert-base-nli-stsb-mean-tokens')


def replaceLast(string, find, replace):
    reversed = string[::-1]
    replaced = reversed.replace(find[::-1], replace[::-1], 1)
    return replaced[::-1]


def correctSpaces(stringToCorrect):
    return re.sub(' +', ' ', stringToCorrect)


def actiavteTopKPSampling(model, inputIds, maximumLengthStatement):
    return model.generate(
        inputIds,
        do_sample=True,
        max_length=maximumLengthStatement,
        top_p=0.9,
        top_k=20,
        repetition_penalty=20.0,
        num_return_sequences=5
    )


def generateSentences(sampleOuputs, tokeniser):
    generatedSentences = []
    for i, sampleOutput in enumerate(sampleOuputs):
        decodedSentence = tokeniser.decode(sampleOutput, skip_special_tokens=True)
        finalSentence = tokenize.sent_tokenize(decodedSentence)[0]
        generatedSentences.append(finalSentence)
    return generatedSentences


def element1(x):
    return x[1]


def findFinalFalseStatement(docs, query):
    docEmbeddings = BERTModel.encode(docs)
    queryEmbeddings = BERTModel.encode([query])
    scores = \
        scipy.spatial.distance.cdist(queryEmbeddings, docEmbeddings, "cosine")[0]
    docScorePairs = zip(range(len(scores)), scores)
    docScorePairs = sorted(docScorePairs, key=element1)
    dissimilarStatements = []
    for index, distance in docScorePairs:
        dissimilarStatements.append(docs[index])
    try:
        return dissimilarStatements[len(dissimilarStatements) % 2]
    except IndexError:
        return None


def completeRightMostPStatement(incompleteRightMostPStatement, originalStatement):
    tokeniser = GPT2Tokenizer.from_pretrained("gpt2")
    model = TFGPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokeniser.eos_token_id)
    inputIds = tokeniser.encode(incompleteRightMostPStatement, return_tensors='tf')
    maximumLengthStatement = len(incompleteRightMostPStatement.split()) + 10 #
    try:
        sampleOuputs = actiavteTopKPSampling(model, inputIds, maximumLengthStatement)
        generatedStatements = generateSentences(sampleOuputs, tokeniser)
    except InvalidArgumentError:
        return incompleteRightMostPStatement
    return findFinalFalseStatement(generatedStatements, originalStatement)


def falsifyStatement(originalStatement):
    cleanedOriginalStatement = cleanUpStatement(originalStatement)
    statementLength = len(cleanedOriginalStatement.split(" "))
    incompleteStatement = ""
    for i in range(0, statementLength):
        if i < statementLength - 1:
            incompleteStatement += (cleanedOriginalStatement.split(" ")[i]) + " "
    return correctSpaces(completeRightMostPStatement(incompleteStatement.strip(), originalStatement))


def cleanUpStatement(originalStatement):
    return originalStatement.translate(str.maketrans('', '', string.punctuation))


if __name__ == "__main__":
    print(falsifyStatement("Tom walked to the park"))
# todo maybe measure level of readability for assessing difficulty of generated false statements - text stat, bleu score
