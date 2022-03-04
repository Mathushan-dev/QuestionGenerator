from transformers import AutoModelWithLMHead, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("ramsrigouthamg/t5_boolean_questions")  # using a pretrained model available on hugging face after discussion with client
model = AutoModelWithLMHead.from_pretrained("ramsrigouthamg/t5_boolean_questions")


def applyT5Model(context, answer, max_length=64):
    input_text = "truefalse: %s  passage: %s </s>" % (answer, context)
    features = tokenizer([input_text], return_tensors='pt')

    output = model.generate(input_ids=features['input_ids'],
                            attention_mask=features['attention_mask'],
                            max_length=max_length)

    return tokenizer.decode(output[0], skip_special_tokens=True, clean_up_tokenization_spaces=True).split(' ', 1)[1]


if __name__ == "__main__":
    print(applyT5Model("Jack walked to the park", "yes"))
