import os

from dotenv import load_dotenv
from hie_rag import SplitAndProcess

load_dotenv()

split_and_process = SplitAndProcess(api_key=os.getenv("OPENAI_API_KEY"))

with open("test.pdf", "rb") as uploaded_file:
    result_process = split_and_process.split_and_process(uploaded_file)

with open("test-split-and-process-result", "w", encoding="utf-8") as file:
    file.write("Split and Processed Text:\n")
    file.write(str(result_process) + "\n")

print("Results written to a txt file.")
