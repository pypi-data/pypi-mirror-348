import json
from typing import List

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import Field
from typing_extensions import TypedDict

from .utils import Utils


class TreeIndex:
    def __init__(self, api_key: str):
        self.client = ChatOpenAI(temperature=0, model="gpt-4o", api_key=api_key)
        self.utils = Utils(api_key=api_key)

    def _convert_to_string(self, chunk_metadata: dict) -> str:
        """
        Converts the chunk metadata to a formatted string.
        """
        summary_list = chunk_metadata["chunks"]
        summaries = "\n".join([chunk["summary"] for chunk in summary_list])
        return summaries

    def _generate_higher_summary(self, summaries: str):
        """
        Generates a higher-level summary from the input summaries.
        """
        prompt = PromptTemplate(
            template="""
            Based on the multiple summaries of the text chunks, please generate a higher-level summary and some keywords that captures the main points of the text.

            NOTE: 
            1. 請輸出繁體中文
            2. The summary should be concise and capture the main points of the text.
            3. The summary should be around 5-8 sentences long.

            Summaries:
            {summaries}
            """,
            input_variables=["summaries"],
        )

        class MetaData(TypedDict):
            higher_summary: str = Field(
                description="The higher-level summary of the summaries",
            )
            keywords: List[str] = Field(
                description="A list of keywords that represent the main points of the chunk.",
            )

        llm_with_tool = self.client.with_structured_output(MetaData)
        chain = prompt | llm_with_tool
        
        return chain.invoke({"summaries": summaries})
    
    def tree_index(self, file_name, chunk_metadata: dict, json_format=False) -> str:
        """
        Generates a higher-level summary from the input summaries.
        """
        summaries = self._convert_to_string(chunk_metadata)
        higher_summary = self._generate_higher_summary(summaries)
        embeddings = self.utils.get_embedding(higher_summary.get("higher_summary"))

        data = {
            "file_name": file_name,
            "summary": higher_summary.get("higher_summary"),
            "keywords": higher_summary.get("keywords"),
            "embeddings": embeddings,
            "chunks": chunk_metadata["chunks"]
        }

        if json_format:
            json_data = json.dumps(data, ensure_ascii=False)
            return json_data
        else:
            return data