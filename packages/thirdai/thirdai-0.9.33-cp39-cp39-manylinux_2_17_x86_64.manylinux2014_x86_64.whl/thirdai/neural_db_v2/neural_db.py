import json
import os
from typing import Iterable, List, Optional, Tuple, Union

from .chunk_stores import PandasChunkStore, SQLiteChunkStore
from .core.chunk_store import ChunkStore
from .core.documents import Document
from .core.reranker import Reranker
from .core.retriever import Retriever
from .core.supervised import SupervisedDataset
from .core.types import Chunk, ChunkId, InsertedDocMetadata, NewChunkBatch, Score
from .documents import PrebatchedDoc, document_by_name
from .rerankers.pretrained_reranker import PretrainedReranker
from .retrievers import FinetunableRetriever, Mach, MachEnsemble


class NeuralDB:
    def __init__(
        self,
        chunk_store: Optional[ChunkStore] = None,
        retriever: Optional[Retriever] = None,
        save_path: Optional[str] = None,
        **kwargs,
    ):
        self.reranker: Optional[Reranker] = None

        if save_path is None:
            self.chunk_store = chunk_store or SQLiteChunkStore(**kwargs)
            self.retriever = retriever or FinetunableRetriever(**kwargs)
            return

        if chunk_store or retriever:
            raise ValueError(
                "When using 'save_path', cannot use custom 'retriever' or 'chunk_store'"
            )

        os.makedirs(save_path)

        self.chunk_store = SQLiteChunkStore(
            save_path=self.chunk_store_path(save_path), **kwargs
        )
        self.retriever = FinetunableRetriever(
            save_path=self.retriever_path(save_path), **kwargs
        )
        self.save_metadata(save_path)

    def insert_chunks(self, chunks: Iterable[NewChunkBatch], **kwargs):
        return self.insert([PrebatchedDoc(chunks)], **kwargs)

    def insert(
        self, docs: List[Union[str, Document]], **kwargs
    ) -> List[InsertedDocMetadata]:
        docs = [
            doc if isinstance(doc, Document) else document_by_name(doc) for doc in docs
        ]

        chunks, doc_metadata = self.chunk_store.insert(docs=docs, **kwargs)
        self.retriever.insert(chunks=chunks, **kwargs)

        return doc_metadata

    def search(
        self,
        query: str,
        top_k: int = 5,
        constraints: dict = None,
        rerank: bool = False,
        **kwargs,
    ) -> List[Tuple[Chunk, Score]]:
        return self.search_batch([query], top_k, constraints, rerank, **kwargs)[0]

    def search_batch(
        self,
        queries: List[str],
        top_k: int,
        constraints: dict = None,
        rerank: bool = False,
        **kwargs,
    ) -> List[List[Tuple[Chunk, Score]]]:
        if not constraints:
            results = self.retriever.search(queries, top_k, **kwargs)
        else:
            choices = self.chunk_store.filter_chunk_ids(constraints, **kwargs)
            # TODO is there a better way that duplicating the constraints here
            results = self.retriever.rank(
                queries, [choices for _ in queries], top_k, **kwargs
            )

        chunk_results = []
        for i, query_results in enumerate(results):
            if not query_results:
                chunk_results.append([])
            else:
                chunk_ids, scores = [list(tup)[:top_k] for tup in zip(*query_results)]
                chunks = self.chunk_store.get_chunks(chunk_ids)
                query_results = list(zip(chunks, scores))
                if rerank:
                    query_results = self.rerank(queries[i], query_results)
                chunk_results.append(query_results)

        return chunk_results

    def rerank(
        self, query: str, results: List[Tuple[Chunk, Score]]
    ) -> List[Tuple[Chunk, Score]]:
        if self.reranker is None:
            self.reranker = PretrainedReranker()
        return self.reranker.rerank(query, results)

    def delete(self, chunk_ids: List[ChunkId]):
        self.chunk_store.delete(chunk_ids)
        self.retriever.delete(chunk_ids)

    def delete_doc(
        self,
        doc_id: str,
        keep_latest_version: bool = False,
        return_deleted_chunks: bool = False,
    ):
        before_version = (
            self.chunk_store.max_version_for_doc(doc_id)
            if keep_latest_version
            else float("inf")
        )
        chunk_ids = self.chunk_store.get_doc_chunks(
            doc_id=doc_id, before_version=before_version
        )

        if return_deleted_chunks:
            chunks_to_delete = self.chunk_store.get_chunks(chunk_ids)

        self.retriever.delete(chunk_ids)
        self.chunk_store.delete(chunk_ids)

        if return_deleted_chunks:
            return chunks_to_delete

    def upvote(self, queries: List[str], chunk_ids: List[ChunkId], **kwargs):
        self.retriever.upvote(queries, chunk_ids, **kwargs)

    def associate(self, sources: List[str], targets: List[str], **kwargs):
        self.retriever.associate(sources, targets, **kwargs)

    def supervised_train(
        self,
        supervised: SupervisedDataset,
        validation: Optional[SupervisedDataset] = None,
        **kwargs,
    ):
        self.retriever.supervised_train(
            samples=supervised.samples(),
            validation=validation.samples() if validation else None,
            **kwargs,
        )

    def documents(self) -> List[dict]:
        return self.chunk_store.documents()

    def context(self, chunk: Chunk, radius: int) -> List[Chunk]:
        return self.chunk_store.context(chunk=chunk, radius=radius)

    @staticmethod
    def chunk_store_path(directory: str) -> str:
        return os.path.join(directory, "chunk_store")

    @staticmethod
    def retriever_path(directory: str) -> str:
        return os.path.join(directory, "retriever")

    @staticmethod
    def metadata_path(directory: str) -> str:
        return os.path.join(directory, "metadata.json")

    @staticmethod
    def load_chunk_store(path: str, chunk_store_name: str, **kwargs):
        chunk_store_name_map = {
            PandasChunkStore.__name__: PandasChunkStore,
            SQLiteChunkStore.__name__: SQLiteChunkStore,
        }

        if chunk_store_name not in chunk_store_name_map:
            raise ValueError(f"Class name {chunk_store_name} not found in registry.")

        return chunk_store_name_map[chunk_store_name].load(path, **kwargs)

    @staticmethod
    def load_retriever(path: str, retriever_name: str, **kwargs):
        retriever_name_map = {
            FinetunableRetriever.__name__: FinetunableRetriever,
            Mach.__name__: Mach,
            MachEnsemble.__name__: MachEnsemble,
        }

        if retriever_name not in retriever_name_map:
            raise ValueError(f"Class name {retriever_name} not found in registry.")

        return retriever_name_map[retriever_name].load(path, **kwargs)

    def save_metadata(self, path: str):
        metadata = {
            "chunk_store_name": self.chunk_store.__class__.__name__,
            "retriever_name": self.retriever.__class__.__name__,
        }

        with open(self.metadata_path(path), "w") as f:
            json.dump(metadata, f)

    def save(self, path: str):
        if os.path.exists(path):
            if not os.path.isdir(path):
                raise ValueError(
                    f"Cannot save NeuralDB to {path} since it is not a directory"
                )
        else:
            os.makedirs(path)

        self.chunk_store.save(self.chunk_store_path(path))
        self.retriever.save(self.retriever_path(path))

        self.save_metadata(path)

    @staticmethod
    def load(path: str, **kwargs):
        with open(NeuralDB.metadata_path(path), "r") as f:
            metadata = json.load(f)

        chunk_store = NeuralDB.load_chunk_store(
            NeuralDB.chunk_store_path(path),
            chunk_store_name=metadata["chunk_store_name"],
            **kwargs,
        )

        retriever = NeuralDB.load_retriever(
            NeuralDB.retriever_path(path),
            retriever_name=metadata["retriever_name"],
            **kwargs,
        )

        return NeuralDB(chunk_store=chunk_store, retriever=retriever)
