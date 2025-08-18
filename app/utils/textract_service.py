from collections import defaultdict
from typing import List


class TextractKVExtractor:
    def __init__(self, textract_client):
        """
        textract_client: boto3 Textract client (already configured)
        """
        self.client = textract_client

    def _get_kv_map(self, file_bytes):
        response = self.client.analyze_document(
            Document={"Bytes": file_bytes}, FeatureTypes=["FORMS"]
        )
        blocks = response["Blocks"]
        key_map, value_map, block_map = {}, {}, {}

        for block in blocks:
            block_map[block["Id"]] = block
            if block["BlockType"] == "KEY_VALUE_SET":
                if "KEY" in block["EntityTypes"]:
                    key_map[block["Id"]] = block
                else:
                    value_map[block["Id"]] = block
        return key_map, value_map, block_map

    def _find_value_block(self, key_block, value_map):
        for rel in key_block.get("Relationships", []):
            if rel["Type"] == "VALUE":
                for value_id in rel["Ids"]:
                    return value_map.get(value_id)
        return None

    def _get_text(self, block, block_map):
        if not block:
            return ""
        text = ""
        for rel in block.get("Relationships", []):
            if rel["Type"] == "CHILD":
                for child_id in rel["Ids"]:
                    child = block_map.get(child_id, {})
                    if child.get("BlockType") == "WORD":
                        text += child.get("Text", "") + " "
                    if (
                        child.get("BlockType") == "SELECTION_ELEMENT"
                        and child.get("SelectionStatus") == "SELECTED"
                    ):
                        text += "X "
        return text.strip()

    def _get_kv_relationship(self, key_map, value_map, block_map):
        kvs = defaultdict(list)
        for key_id, key_block in key_map.items():
            value_block = self._find_value_block(key_block, value_map)
            key_text = self._get_text(key_block, block_map)
            value_text = self._get_text(value_block, block_map)
            kvs[key_text].append(value_text)
        return kvs

    def _extract_all_text(self, file_bytes: bytes) -> str:
        """
        Extracts all text from the document, including text not associated with keys.
        """
        response = self.client.detect_document_text(Document={"Bytes": file_bytes})
        text_blocks = [
            block["Text"]
            for block in response["Blocks"]
            if block["BlockType"] == "LINE"
        ]
        return "\n".join(text_blocks)

    def run(self, file_path=None, file_bytes=None, extract_full_text=False):
        """
        Run the extraction.
        Provide either `file_path` or `file_bytes`.
        If extract_full_text=True, returns all text (not just key-value pairs).
        """
        if file_path:
            with open(file_path, "rb") as f:
                file_bytes = f.read()
        if not file_bytes:
            raise ValueError("You must provide file_path or file_bytes.")

        if extract_full_text:
            return self._extract_all_text(file_bytes)

        key_map, value_map, block_map = self._get_kv_map(file_bytes)
        kvs = self._get_kv_relationship(key_map, value_map, block_map)
        return str(kvs)


def extract_text_single_id(
    images_bytes_list: List[bytes],
    textract_instance: TextractKVExtractor,
    extract_full_text: bool = False,
) -> str:
    """
    Extract text from a list of PNG image bytes using TextractKVExtractor.
    if extract full text is true, it will not only return key values pairs.
    Args:
        id_and_images: Tuple containing (id, list of PNG image bytes)
        textract_instance: TextractKVExtractor instance

    Returns:
        concatenated extracted text from all images
    """

    full_text = ""
    for img_bytes in images_bytes_list:
        text = textract_instance.run(
            file_bytes=img_bytes, extract_full_text=extract_full_text
        )
        full_text += text
    return full_text
