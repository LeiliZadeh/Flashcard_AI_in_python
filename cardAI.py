# -*- coding: utf-8 -*-

import time
import google.generativeai as palm
import PyPDF2
import os
from pypdf import PdfReader

# Configure the PaLM API key
palm.configure(api_key='AIzaSyCXpiohNJcnIh8D4pv6w-3uVy8Bxo0n048')

# Use the palm.list_models function to find available models:
models = [m for m in palm.list_models(
) if 'generateText' in m.supported_generation_methods]
model = models[0].name
print(model)

# Simplest Chatbot
'''prompt1 = """
You are an expert at solving word problems.

Solve the following problem:

I have three houses, each with three cats.
each cat owns 4 mittens, and a hat. Each mitten was
knit from 7m of yarn, each hat from 4m.
How much yarn was needed to make all the items?

Think about it step by step, and show your work.
"""

completion1 = palm.generate_text(
    model=model,
    prompt=prompt1,
    temperature=0,
    max_output_tokens=800,
)

print(completion1.result)

# Set your input text
prompt2 = "What is Quantum Computing? Explain like I'm 5."

completion2 = palm.generate_text(
    model=model,
    prompt=prompt2,
    temperature=0,
    max_output_tokens=200,
)

print(completion2.result)
'''
# Custom Chatbot - Text Summarizer
directory = '/Users/leili/Desktop/Flashcard_AI_in_python'
filename = '/Lec2-CloudComputing.pdf'

# Create a pdf file object
pdfFileObject = open(directory + filename, 'rb')
# Create a pdf reader object
pdfReader = PdfReader(pdfFileObject)
text = []
summary = ''

# Storing the pages in a list
for i in range(0, len(pdfReader.pages)):
    # Creating a page object
    pageObj = pdfReader.pages[i].extract_text()
    pageObj = pageObj.replace('\t\r', '')
    pageObj = pageObj.replace('\xa0', '')
    # Extracting text from page
    text.append(pageObj)

# Merge multiple pages to reduce API Calls


def join_elements(lst, chars_per_element):
    new_lst = []
    for i in range(0, len(lst), chars_per_element):
        new_lst.append(''.join(lst[i:i+chars_per_element]))
    return new_lst


# Option to keep x elements per list element
new_text = join_elements(text, 3)

print(f"Original Pages = ", len(text))
print(f"Compressed Pages = ", len(new_text))


def get_completion(prompt):
    completion = palm.generate_text(model=model,
                                    prompt=prompt,
                                    temperature=0,
                                    max_output_tokens=200,
                                    )
    return completion.result


summary = ""
for i in range(len(new_text)):
    prompt = f"""
  You are a flashcard maker AI, and your task is to find words and their definitions in text. Here's how you should work:
    Input Text: You will receive a text input from the user that contains sentences with words and their corresponding definitions. The text will be in the format: "Word: Definition."
    Flashcard Creation: Your primary job is to create flashcards for each word-definition pair you find in the input text.
    Example Flashcard: For each word-definition pair you find, create a flashcard that looks like this:
        Word: [Word]
        Definition: [Definition]
    Output: Print out the created flashcards for the user to review. Make sure to format them clearly, with each flashcard clearly indicating the word and its definition.
Remember to be accurate and clear in your flashcard creation, and provide a user-friendly experience for those who want to study and review the content.
  ```{text[i]}```
  """
    try:
        response = get_completion(prompt)
    except:
        response = get_completion(prompt)
    print(response)
    summary = f"{summary} {response}\n\n"
    # You can query the model only 3 times in a minute for free, so we need to put some delay
    time.sleep(19)

with open(directory + '/palm_api_summary.txt',
          'w') as out:
    out.write(summary)
