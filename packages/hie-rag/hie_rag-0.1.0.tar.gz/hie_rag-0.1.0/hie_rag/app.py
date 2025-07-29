# import json
# import os

# from .generate import Generate
# from .process import Process
# from .split import Split
# from .tree_index import TreeIndex
# from .utils import Utils
# from .vectordb import Vectordb


# # Function to handle data
# def handle_data(data):
#     """
#     Processes incoming data and returns a response.
#     """
#     try:
#         # This is the logic that used to be in the /api/data route
#         return {"received": data}
#     except Exception as e:
#         return {"error": str(e)}

# # Function to handle file upload and processing
# def handle_file_upload(uploaded_file, access_token):
#     """
#     Processes the uploaded file and extracts its text.
#     """
#     try:
#         utils = Utils(api_key=access_token)
#         process = Process(api_key=access_token)
#         split = Split(api_key=access_token)
#         tree_index = TreeIndex(api_key=access_token)

#         if uploaded_file is None:
#             return {"error": "No file selected for uploading"}

#         filename = uploaded_file.filename
#         extracted_text = utils.extract_text(uploaded_file)
#         final_chunk_list = split.split(extracted_text)
#         processed_chunks = process.process_chunks(final_chunk_list)
#         data = tree_index.output_index(processed_chunks)

#         return {"filename": filename, "data": data}
#     except Exception as e:
#         return {"error": str(e)}

# # Function to handle generation logic
# def handle_generation(file, access_token):
#     """
#     Handles the file for generation and returns generated data.
#     """
#     try:
#         data = json.load(file)

#         if "chunks" not in data:
#             return {"error": "Missing 'chunks' in data"}

#         path = os.getenv("INDEX_PATH")
#         vectordb = Vectordb(path=path, api_key=access_token)
#         generate = Generate(api_key=access_token)

#         save_index_result = vectordb.save_index(data)
#         generated_full_data = []
        
#         for i in data["chunks"]:
#             original_chunk = i["original_chunk"]
#             query_result = vectordb.query_by_text(original_chunk, n_results=3)
#             possible_reference = query_result["metadatas"][0][1]["summary"] + "\n" + query_result["metadatas"][0][2]["summary"]

#             data_gen = generate.generate(original_chunk, possible_reference)
#             generated_full_data.extend(data_gen["dataset"])

#         return {"data": generated_full_data}
#     except json.JSONDecodeError:
#         return {"error": "Invalid JSON file format"}
#     except Exception as e:
#         return {"error": str(e)}