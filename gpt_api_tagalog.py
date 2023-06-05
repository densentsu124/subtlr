#needs installation of openai package

import openai
openai.api_key = "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" #this is the paid one
# openai.api_key = "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" # free ones
# openai.api_key = "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"

def translate(text):
    response = openai.Completion.create(
                model="text-davinci-003",
                prompt=generate_prompt(text),
                temperature=0.6,
            )
    return response.choices[0].text

def generate_prompt(text):
    return """Translate the mix of English and Tagalog words into English based on the context of the English text. 
    The output should be English. In cases where the text is purely tagalog, translate it into english with proper grammar. 
    In cases where the text is purely english, just use the input as the output.
    In cases where the input doesnt make sense, reply with ellipses.
    In cases where you require more context, reply with ellipses.
    
    Input: I am very gwapo.
    Output: I am very handsome.
    Input: Kahit pagod na pagod na siya, he picked himself up. Kaya ko ito, that's what he thought.
    Output: Even if he's extremly tired, he picked himself up. He thought he could do it, that's why.
    Input: Meron akong tatlong talong.
    Output: I have three eggplants.
    Input: {}
    Output:""".format(
            text.capitalize()
        )
    return "1"