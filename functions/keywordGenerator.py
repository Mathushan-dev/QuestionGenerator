import textrazor

textrazor.api_key = "30fe67fd47af0a4748a1f6646973773bb0286768e9272425170ee562"

client = textrazor.TextRazor(extractors=["entities", "topics"])  # todo change extractors


def analyseText(text):
    output = []
    try:
        response = client.analyze(text)
        for entity in response.entities():
            print(entity.userId, entity.relevance_score, entity.confidence_score, entity.freebase_types)
            output.append(entity.userId)
    except textrazor.TextRazorAnalysisException as ex:
        print(ex)

    return output


# todo return a list of all the keywords from the user inputted text
def findQuestionKeywords(text):
    return analyseText(text)


# todo handle no keywords error


def findRandomKeyword(text):
    return "cheetah"


def fake(text):
    keywords = findQuestionKeywords(text)
    if len(keywords) > 1:
        return random.choice(keywords)
    return keywords

# maybe use text rank, also consider wikifier
