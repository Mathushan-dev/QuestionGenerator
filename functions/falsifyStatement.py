import re
import string
import nltk
import scipy
import spacy
import readability
from allennlp.predictors.predictor import Predictor
from nltk import tokenize
from nltk.tree import Tree
from sentence_transformers import SentenceTransformer
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer
from T5QuestionGenerator import applyT5Model

nltk.download('punkt')
nlp = spacy.load("en_core_web_sm")
predictor = Predictor.from_path(
    "https://s3-us-west-2.amazonaws.com/allennlp/models/elmo-constituency-parser-2018.03.14.tar.gz")
# The model below an All-round model tuned for many use-cases. Trained on a large and diverse dataset of over 1 billion training pairs.
BERTModel = SentenceTransformer('sentence-transformers/all-distilroberta-v1')


def generateTree(cleanedOriginalStatement):
    parserOutput = predictor.predict(sentence=cleanedOriginalStatement)
    return Tree.fromstring(parserOutput["trees"])


def getRightMostNPVP(tree, rightMostNP=None, rightMostVP=None):
    if len(tree.leaves()) == 1:
        return rightMostNP, rightMostVP
    rightMostBranch = tree[-1]
    if rightMostBranch.label() == "NP":
        rightMostNP = rightMostBranch
    elif rightMostBranch.label() == "VP":
        rightMostVP = rightMostBranch

    return getRightMostNPVP(rightMostBranch, rightMostNP, rightMostVP)


def removeTreeAttributes(treePhrase):
    if treePhrase is None:
        return None
    return [" ".join([" ".join(branch.leaves()) for branch in list(treePhrase)])][0]


def replaceLast(string, find, replace):
    reversed = string[::-1]
    replaced = reversed.replace(find[::-1], replace[::-1], 1)
    return replaced[::-1]


def correctSpaces(stringToCorrect):
    return re.sub(' +', ' ', stringToCorrect)


def removeRightMostP(cleanedOriginalStatement, longestRightMostP):
    spaceCorrectedJoinedRightMostP = correctSpaces(longestRightMostP)
    spaceCorrectedJoinedOriginalStatement = correctSpaces(cleanedOriginalStatement)
    return replaceLast(spaceCorrectedJoinedOriginalStatement, spaceCorrectedJoinedRightMostP, "")


def actiavteTopKPSampling(model, inputIds, maximumLengthStatement):
    return model.generate(
        inputIds,
        do_sample=True,
        max_length=maximumLengthStatement,
        top_p=0.85,
        top_k=30,
        repetition_penalty=10.0,
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


def getReadabilityScore(text):
    results = readability.getmeasures(text, lang='en')
    return results['readability grades']['FleschReadingEase']


def slice_per(source, step):
    return [source[i::step] for i in range(step)]


def findFinalFalseStatement(generatedStatements):
    return slice_per(sorted(generatedStatements, key=getReadabilityScore), 4)[-1][0]


def completeRightMostPStatement(incompleteRightMostPStatement):
    tokeniser = GPT2Tokenizer.from_pretrained("gpt2")
    model = TFGPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokeniser.eos_token_id)
    inputIds = tokeniser.encode(incompleteRightMostPStatement, return_tensors='tf')
    maximumLengthStatement = len(incompleteRightMostPStatement.split()) + 40
    sampleOuputs = actiavteTopKPSampling(model, inputIds, maximumLengthStatement)
    generatedStatements = generateSentences(sampleOuputs, tokeniser)
    cleanedGeneratedStatements = []
    for statement in generatedStatements:
        cleanedGeneratedStatements.append(statement.replace(u'\xa0', u''))
    return findFinalFalseStatement(cleanedGeneratedStatements)


def falsifyStatement(originalStatement):
    cleanedOriginalStatement = cleanUpStatement(originalStatement)
    tree = generateTree(cleanedOriginalStatement)
    rightMostNP, rightMostVP = getRightMostNPVP(tree)
    cleanedRightMostNP = removeTreeAttributes(rightMostNP)
    cleanedRightMostVP = removeTreeAttributes(rightMostVP)
    longestRightMostP = max(cleanedRightMostNP, cleanedRightMostVP)
    incompleteRightMostPStatement = removeRightMostP(cleanedOriginalStatement, longestRightMostP)
    print(incompleteRightMostPStatement)
    return applyT5Model(incompleteRightMostPStatement, None, False)


def cleanUpStatement(originalStatement):
    return originalStatement.translate(str.maketrans('', '', string.punctuation))


if __name__ == "__main__":
    print(falsifyStatement("The student was very sad and he started crying."))
# todo maybe measure level of readability for assessing difficulty of generated false statements - text stat, bleu score
