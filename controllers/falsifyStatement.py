import spacy
import string
from allennlp.predictors.predictor import Predictor
from nltk import tokenize
from nltk.tree import Tree

nlp = spacy.load("en_core_web_sm")
predictor = Predictor.from_path(
    "https://s3-us-west-2.amazonaws.com/allennlp/models/elmo-constituency-parser-2018.03.14.tar.gz")


def generateTree(cleanedOriginalStatement):
    parserOutput = predictor.predict(sentence=cleanedOriginalStatement)
    return Tree.fromString(parserOutput["trees"])


def getRightMostNPVP(tree, rightMostNP = None, rightMostVP = None):
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
    cleanedTreePhrase = [" ".join(branch.leaves()) for branch in list(treePhrase)]
    print(cleanedTreePhrase)
    cleanedTreePhrase = [" ".join(cleanedTreePhrase)]
    print(cleanedTreePhrase)
    cleanedTreePhrase = cleanedTreePhrase[0]
    print(cleanedTreePhrase)
    return cleanedTreePhrase


def falsifyStatement(originalStatement):
    cleanedOriginalStatement = cleanUpStatement(originalStatement)
    tree = generateTree(cleanedOriginalStatement)
    rightMostNP, rightMostVP = getRightMostNPVP(tree)
    cleanedRightMostNP = removeTreeAttributes(rightMostNP)
    cleanedRightMostVP = removeTreeAttributes(rightMostVP)


def cleanUpStatement(originalStatement):
    return originalStatement.translate(str.maketrans('', '', string.punctuation))


# def test_cleanUpStatement():
print(falsifyStatement("Hey, how    are you? I am fine!"))  # == "Hey how    are you I am fine")
