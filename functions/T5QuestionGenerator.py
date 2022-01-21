import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

t5Model = T5ForConditionalGeneration.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")
t5Tokeniser = T5Tokenizer.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")
device = torch.device("cpu")
deviceT5Model = t5Model.to(device)


def generateBeamOutputs(statement, answer):
    modelInput = "context: " + statement + " " + "answer: " + answer + " </s>"
    encoding = t5Tokeniser.encode_plus(modelInput, max_length=512, padding=True, return_tensors="pt")
    inputIds, attentionMask = encoding["input_ids"].to(device), encoding["attention_mask"].to(device)
    deviceT5Model.eval()
    return deviceT5Model.generate(
        input_ids=inputIds, attention_mask=attentionMask,
        max_length=72,
        early_stopping=True,
        num_beams=5,
        num_return_sequences=3
    )


def applyT5Model(statement, answer):
    beamOutputs = generateBeamOutputs(statement, answer)
    return generateQuestionsFromBeamOutputs(beamOutputs)


def generateQuestionsFromBeamOutputs(beamOutputs):
    questions = []
    for output in beamOutputs:
        questions.append(t5Tokeniser.decode(output, skip_special_tokens=True, clean_up_tokenization_spaces=True))

    return questions


if __name__ == "__main__":
    print(applyT5Model("The cheetah is the fastest land animal.", "cheetah"))
