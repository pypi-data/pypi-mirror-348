import contextlib
import io
import os
import tempfile

import numpy as np
import tiktoken
from markitdown import MarkItDown
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity


class Utils:
    def __init__(self, api_key=None):
        self.client = OpenAI(api_key=api_key)

    def extract_text(self, uploaded_file: bytes):
        """Extract text from an uploaded file using MarkItDown."""
        md = MarkItDown(llm_client=self.client, llm_model="gpt-4o")

        # Accept both raw bytes and file-like objects with `.read()`
        if isinstance(uploaded_file, bytes):
            file_bytes = uploaded_file
        elif hasattr(uploaded_file, "read"):
            file_bytes = uploaded_file.read()
        else:
            raise TypeError("Unsupported file type: must be bytes or file-like object")

        # Write to temp file for MarkItDown to process
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(file_bytes)

        try:
            # Redirect stderr to suppress native print warnings like "CropBox missing"
            with contextlib.redirect_stderr(io.StringIO()):
                extracted_text = md.convert(temp_file_path)
        finally:
            # Clean up the temporary file
            os.remove(temp_file_path)

        return extracted_text.text_content

    def count_tokens(self, text: str, encoding="cl100k_base") -> int:
        """Count tokens in text using tiktoken"""
        tokenizer = tiktoken.get_encoding(encoding)
        return len(tokenizer.encode(text))

    def list_embeddings(self, chunks: list, model="text-embedding-3-small") -> list:
        """Get embeddings for a list of text chunks"""
        embeddings = []
        for chunk in chunks:
            response = self.client.embeddings.create(input=chunk, model=model)
            embeddings.append(response.data[0].embedding)
        return embeddings

    def get_embedding(self, text: str, model="text-embedding-3-small") -> list:
        """Get embedding for a text"""
        response = self.client.embeddings.create(input=text, model=model)
        return response.data[0].embedding

    def get_consecutive_least_similar(self, embeddings: list) -> int:
        """Find the index where consecutive similarity is lowest"""
        cs = cosine_similarity(embeddings)
        
        # Get similarities between consecutive sentences only
        consecutive_similarities = []
        for i in range(len(cs) - 1):
            consecutive_similarities.append(cs[i][i + 1])
        
        # Find the index where consecutive similarity is lowest
        split_index = np.argmin(consecutive_similarities)
        
        return split_index