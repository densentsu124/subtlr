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

    Input: I am very gwapo.
    Output: I am very handsome.
    Input: Despite sa kaguol, he picked himself up. Kaya ra lagi na, that's what he thought.
    Output: Despite the sorrow, he picked himself up. He thought he could do it, that's why.
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