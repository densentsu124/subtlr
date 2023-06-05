import openai
openai.api_key = "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"

def translate(text):
    response = openai.Completion.create(
                model="text-davinci-003",
                prompt=generate_prompt(text),
                temperature=0.6,
            )
    return response.choices[0].text

def generate_prompt(text):
    return """Translate the mix of English and Bisaya words into English based on the context of the English text. The output should be English.
    In cases where one of the words in the bisaya text does not make sense given the sentence structure, find the most suitable bisaya word and replace it and then translate to english.
    In cases where the text is purely bisaya, translte it into english with proper grammar.
    In cases where the text is purely english, just use the input as the output.
    In cases where the text doesnt make sense, reply with (incomprehensible).
    In cases where you require more context, reply with (incomprehensible).

    Input: I am very gwapo.
    Output: I am very handsome.
    Input: Despite sa kaguol, he picked himself up. Kaya ra lagi na, that's what he thought.
    Output: Despite the sorrow, he picked himself up. He thought he could do it, that's why.
    Input: Dance usa then more three lighht.
    Output: ...
    Input: Naa nami danri.
    Output: We're already here.
    Input: {}
    Output:""".format(
            text.capitalize()
        )
    return "1"


# def main():
#     text_input = "I brought mani to class. I have very many mani."
#     print("Translated output: {}".format(translate(text_input)))

# if __name__ == "__main__":
#     main()