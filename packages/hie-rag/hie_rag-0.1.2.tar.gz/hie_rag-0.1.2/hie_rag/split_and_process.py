from hie_rag.process import Process
from hie_rag.split import Split
from hie_rag.utils import Utils


class SplitAndProcess:
    def __init__(self, api_key=None):
        self.split = Split(api_key=api_key)
        self.utils = Utils(api_key=api_key)
        self.process = Process(api_key=api_key)

    def split_and_process(self, uploaded_file):
        extracted_text = self.utils.extract_text(uploaded_file)
        result_split = self.split.split(extracted_text)
        result_process = self.process.process_chunks(result_split)

        return result_process