from transformers import AutoModelWithLMHead, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(
    "mrm8488/t5-base-finetuned-question-generation-ap")  # using a pretrained model available on hugging face after
# discussion with client
model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")


# https://huggingface.co/mrm8488/t5-base-finetuned-question-generation-ap

def apply_t5_model(context, answer, max_length=64):
    """
    todo
    :param context:
    :param answer:
    :param max_length:
    :return: Any
    """
    input_text = "answer: %s  context: %s </s>" % (answer, context)
    features = tokenizer([input_text], return_tensors='pt')

    output = model.generate(input_ids=features['input_ids'],
                            attention_mask=features['attention_mask'],
                            max_length=max_length)

    return tokenizer.decode(output[0], skip_special_tokens=True, clean_up_tokenization_spaces=True).split(' ', 1)[1]


if __name__ == "__main__":
    print(apply_t5_model("The cheetah is the fastest land animal.", "cheetah"))
