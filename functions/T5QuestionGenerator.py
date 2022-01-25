import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
from transformers import AutoModelWithLMHead, AutoTokenizer

isQuestionGeneration = None
textCompletionModel = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-common_gen")
textCompletionTokeniser = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-common_gen")
questionGenerationModel = T5ForConditionalGeneration.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")
questionGenerationTokeniser = T5Tokenizer.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")
t5Model = None
t5Tokeniser = None
device = torch.device("cpu")
deviceT5Model = None


def generateBeamOutputs(statement, answer):
    modelInput = "context: " + statement + " " + "answer: " + answer
    encoding = t5Tokeniser.encode_plus(modelInput, padding=True, return_tensors="pt")
    inputIds, attentionMask = encoding["input_ids"].to(device), encoding["attention_mask"].to(device)
    deviceT5Model.eval()
    return deviceT5Model.generate(
        input_ids=inputIds, attention_mask=attentionMask,
        max_length=72,
        early_stopping=True,
        num_beams=5,
        num_return_sequences=3
    )


def applyT5Model(statement, answer, questionGeneration):
    global t5Model, t5Tokeniser, isQuestionGeneration, questionGenerationModel, questionGenerationTokeniser, textCompletionModel, textCompletionTokeniser, device
    isQuestionGeneration = questionGeneration
    if questionGeneration:
        t5Model = questionGenerationModel
        t5Tokeniser = questionGenerationTokeniser
        t5Model.to(device)
        beamOutputs = generateBeamOutputs(statement, answer)
        return generateQuestionsFromBeamOutputs(beamOutputs)
    else:
        t5Model = textCompletionModel
        t5Tokeniser = textCompletionTokeniser
        t5Model.to(device)
        return gen_sentence(statement)


def gen_sentence(words, max_length=32):
  input_text = words
  features = t5Tokeniser([input_text], return_tensors='pt')

  output = t5Model.generate(input_ids=features['input_ids'],
               attention_mask=features['attention_mask'],
               max_length=max_length)

  return t5Tokeniser.decode(output[0], skip_special_tokens=True)


def generateQuestionsFromBeamOutputs(beamOutputs):
    questions = []
    for output in beamOutputs:
        questions.append(t5Tokeniser.decode(output, skip_special_tokens=True, clean_up_tokenization_spaces=True).split(' ', 1)[1])

    return questions


if __name__ == "__main__":
    print(applyT5Model("The cheetah is the fastest land animal.", "cheetah"))
