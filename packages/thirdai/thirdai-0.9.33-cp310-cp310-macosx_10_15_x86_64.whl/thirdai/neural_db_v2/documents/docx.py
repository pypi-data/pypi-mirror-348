import logging
from typing import Any, Dict, Iterable, Optional

import thirdai.neural_db.parsing_utils.doc_parse as doc_parse

from ..core.documents import Document
from ..core.types import NewChunkBatch
from .utils import join_metadata, series_from_value


class DOCX(Document):
    def __init__(
        self,
        path: str,
        doc_metadata: Optional[Dict[str, Any]] = None,
        doc_id: Optional[str] = None,
        display_path: Optional[str] = None,
    ):
        super().__init__(doc_id=doc_id, doc_metadata=doc_metadata)

        self.path = path
        self.display_path = display_path

    def chunks(self) -> Iterable[NewChunkBatch]:
        elements, success = doc_parse.get_elements(self.path)

        if not success:
            raise ValueError(f"Unable to parse docx file: '{self.path}'.")

        parsed_chunks = doc_parse.create_train_df(elements)

        text = parsed_chunks["para"]

        if len(text) == 0:
            logging.warning(f"Unable to parse content from docx {self.path}.")
            return []

        metadata = join_metadata(
            n_rows=len(text), chunk_metadata=None, doc_metadata=self.doc_metadata
        )

        return [
            NewChunkBatch(
                text=text,
                keywords=series_from_value("", len(text)),
                metadata=metadata,
                document=series_from_value(self.display_path or self.path, len(text)),
            )
        ]
