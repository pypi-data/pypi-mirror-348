import os

from dotenv import load_dotenv
from hie_rag.app import Split
from hie_rag.utils import Utils

load_dotenv()

split = Split(api_key=os.getenv("OPENAI_API_KEY"), min_chunk_size=200, max_chunk_size=500)
utils = Utils(api_key=os.getenv("OPENAI_API_KEY"))

with open("test.pdf", "rb") as uploaded_file:
    extracted_text = utils.extract_text(uploaded_file)

# Simplify the extracted text for testing
extracted_text = extracted_text[:1000]

# Split the extracted text
result_split = split.split(extracted_text)

# Write results to the text file
with open("test-split-result", "w", encoding="utf-8") as file:
    file.write("Splitted Text:\n")
    file.write(str(result_split) + "\n")
    file.write("Length of the Splitted Text:\n")
    file.write(str(len(result_split)) + "\n")

print("Results written to a txt file.")
