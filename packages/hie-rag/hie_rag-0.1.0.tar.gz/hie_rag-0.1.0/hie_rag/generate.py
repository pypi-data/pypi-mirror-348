from typing import Dict, List

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import Field
from typing_extensions import TypedDict


class Generate:
    def __init__(self, api_key: str):   
        self.client = ChatOpenAI(temperature=0, model="gpt-4o", api_key=api_key)

    def generate(self, content: str, possible_reference: str) -> Dict:
        """Generate data for finetuning"""
        prompt = PromptTemplate(
            template="""
            你是一個資料生成器，負責生成用於微調模型的資料集。
            你的工作是閱讀以下內容，並生成一系列人類可能給出的指令（instruction）以及對應的詳細回應（response）。
            instruction 可能會是一個問題、請求整理或者整理內容等指令。

            注意事項：
            1. 請輸出繁體中文。
            2. 請務必只生成與內容相關的指令與回應。
            3. 如果不確定內容在講什麼，可以參考「可能參考資料（Possible Reference）」來幫助理解。
            4.「可能參考資料」只是可能幫助你理解的參考來源。
            5. 不要捏造答案，如果真的不知道，就不要亂寫。

            Content:
            {content}

            Possible Reference:
            {possible_reference}

            """,
            input_variables=["content", "possible_reference"],
        )
        class InstructionResponse(TypedDict):
            instruction: str = Field(
                description="An instruction that a human might provide based on the content.",
            )
            response: str = Field(
                description="The corresponding response to the instruction.",
            )
            used_reference: bool = Field(
                description="Indicates whether the possible reference was used to generate this pair. True if the Possible Reference is relavent and useful, False otherwise.",
            )
            reference_usage: str = Field(
                description="Explanation of how the reference was used, if it was used.",
            )

        class Dataset(TypedDict):
            dataset: List[InstructionResponse]
            content_analysis: str = Field(
                description="Brief analysis of whether and how the reference helped with understanding the content.",
            )

        model = self.client
        llm_with_tool = model.with_structured_output(Dataset)
        chain = prompt | llm_with_tool
        
        return chain.invoke({"content": content, "possible_reference": possible_reference})