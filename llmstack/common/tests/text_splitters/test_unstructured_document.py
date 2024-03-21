import unittest

from llmstack.common.utils.splitter import UnstructuredDocumentSplitter

SAMPLE_FILE_NAME = f"{'/'.join((__file__.split('/')[:-1]))}/2001_A_SPACE_ODYSSEY.pdf"


class TestUnstructuredTextSplitter(unittest.TestCase):
    def test_unstructured_document_splitter(self):
        chunks = UnstructuredDocumentSplitter(
            file_name=SAMPLE_FILE_NAME,
            chunk_size=4000,
        )._split_text()

        print("=== TestUnstructuredTextSplitter.test_unstructured_document_splitter ===")

        for _chunk in chunks:
            print("-" * 80)
            print(_chunk.text.replace(r"\n\s*\n", " "))
            print("\n")

        assert len(chunks) > 1


if __name__ == "__main__":
    unittest.main()
