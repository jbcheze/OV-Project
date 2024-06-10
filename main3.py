# import PyPDF2
# from openai import OpenAI

# pdf_file = open("./pdf_doc/texte1.pdf", "rb")
# pdf_reader = PyPDF2.PdfReader(pdf_file)

# client = OpenAI(api_key="")

# for page_num in range(len(pdf_reader.pages)):
#     page_text = pdf_reader.pages[page_num].extract_text()
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a helpful reserach assistant."},
#             {"role": "user", "content": f"Summarize this : {page_text}"},
#         ],
#     )

#     page_summary = response.choices[0].message.content

# print(page_summary)

import PyPDF2
import cohere
from dotenv import load_dotenv

# Open the PDF file
pdf_file = open("./pdf_doc/texte1.pdf", "rb")
pdf_reader = PyPDF2.PdfReader(pdf_file)

# Initialize the Cohere client
load_dotenv()

cohere_client = cohere.Client(api_key="aNQr5ZTkCl5cV76YlLCktgp3xWpTsvMeLgGOCYsN")

for page_num in range(len(pdf_reader.pages)):
    page_text = pdf_reader.pages[page_num].extract_text()
    response = cohere_client.generate(
        model="command-xlarge-nightly",
        prompt=f"Summarize this: {page_text}",
        max_tokens=100,  # You can adjust this based on how detailed you want the summary to be
        temperature=0.5,  # You can adjust the temperature to control the randomness of the output
    )

    page_summary = response.generations[0].text.strip()
    print(page_summary)

# Close the PDF file
# pdf_file.close()


# import PyPDF2
# import cohere
# from dotenv import load_dotenv
# import os

# # Load environment variables from the .env file
# load_dotenv()

# # Get the Cohere API key from environment variables
# cohere_api_key = os.getenv("API_KEY_COHERE")

# if not cohere_api_key:
#     raise ValueError("API_KEY_COHERE not found in environment variables")

# # Open the PDF file
# pdf_file = open("./pdf_doc/texte1.pdf", "rb")
# pdf_reader = PyPDF2.PdfReader(pdf_file)

# # Initialize the Cohere client
# cohere_client = cohere.Client(api_key=cohere_api_key)

# for page_num in range(len(pdf_reader.pages)):
#     page_text = pdf_reader.pages[page_num].extract_text()
#     response = cohere_client.generate(
#         model="command-xlarge-nightly",
#         prompt=f"Summarize this: {page_text}",
#         max_tokens=100,  # You can adjust this based on how detailed you want the summary to be
#         temperature=0.5,  # You can adjust the temperature to control the randomness of the output
#     )

#     page_summary = response.generations[0].text.strip()
#     print(page_summary)

# # Close the PDF file
# pdf_file.close()
