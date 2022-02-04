import re
import string
import nltk
import scipy
import spacy
from allennlp.predictors.predictor import Predictor
from nltk import tokenize
from nltk.tree import Tree
from sentence_transformers import SentenceTransformer
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer

nltk.download('punkt')
nlp = spacy.load("en_core_web_sm")
predictor = Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/elmo-constituency-parser-2018.03.14.tar.gz")
# The model below an All-round model tuned for many use-cases. Trained on a large and diverse dataset of over 1 billion training pairs.
BERTModel = SentenceTransformer('sentence-transformers/distilbert-base-nli-stsb-mean-tokens')


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
        num_return_sequences=10
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
    maximumLengthStatement = len(incompleteRightMostPStatement.split()) + 40 #
    sampleOuputs = actiavteTopKPSampling(model, inputIds, maximumLengthStatement)
    generatedStatements = generateSentences(sampleOuputs, tokeniser)
    return findFinalFalseStatement(generatedStatements, originalStatement)


def falsifyStatement(originalStatement):
    cleanedOriginalStatement = cleanUpStatement(originalStatement)
    tree = generateTree(cleanedOriginalStatement)
    rightMostNP, rightMostVP = getRightMostNPVP(tree)
    cleanedRightMostNP = removeTreeAttributes(rightMostNP)
    cleanedRightMostVP = removeTreeAttributes(rightMostVP)
    if cleanedRightMostNP is None and cleanedRightMostVP is None:
        return "A false statement could not be generated for\"" + originalStatement + "\"."
    if cleanedRightMostNP is None:
        longestRightMostP = cleanedRightMostVP
    if cleanedRightMostVP is None:
        longestRightMostP = cleanedRightMostNP
    if cleanedRightMostVP is not None and cleanedRightMostNP is not None:
        longestRightMostP = max(cleanedRightMostNP, cleanedRightMostVP)
    incompleteRightMostPStatement = removeRightMostP(cleanedOriginalStatement, longestRightMostP)
    return correctSpaces(completeRightMostPStatement(incompleteRightMostPStatement, originalStatement))


def cleanUpStatement(originalStatement):
    return originalStatement.translate(str.maketrans('', '', string.punctuation))


if __name__ == "__main__":
    print(falsifyStatement("The old woman was sitting down and sipping tea."))
# todo maybe measure level of readability for assessing difficulty of generated false statements - text stat, bleu score
