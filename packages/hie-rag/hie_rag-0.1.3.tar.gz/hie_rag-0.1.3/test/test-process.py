import os

from dotenv import load_dotenv
from hie_rag.app import Split
from hie_rag.process import Process
from hie_rag.utils import Utils

load_dotenv()

split = Split(api_key=os.getenv("OPENAI_API_KEY"), min_chunk_size=200, max_chunk_size=500)
utils = Utils(api_key=os.getenv("OPENAI_API_KEY"))
process = Process(api_key=os.getenv("OPENAI_API_KEY"))

with open("test.pdf", "rb") as uploaded_file:
    extracted_text = utils.extract_text(uploaded_file)

# Prepare the chunks to process
extracted_text = extracted_text[:1000]
result_split = split.split(extracted_text)
result_process = process.process_chunks(result_split)

# Write results to the text file
with open("test-process-result", "w", encoding="utf-8") as file:
    file.write("Processed Chunks:\n")
    file.write(str(result_process) + "\n")



print("Results written to a txt file.")
