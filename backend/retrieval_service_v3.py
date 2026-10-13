import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = Path(__file__).resolve().parent.parent

KNOWLEDGE_FILE = (
    BASE_DIR
    / "knowledge"
    / "processed"
    / "knowledge_chunks.json"
)


PROGRAM_FILES = {
    "FCCM": ["FCCM.pdf"],
    "AFCCM": ["AFCCM.pdf"],
    "FEM": ["FEM.pdf"],
    "AFEM": ["AFEM.pdf"],
    "FIM": ["FIM.pdf"],
    "FDM": ["FDM.pdf"],
    "FFM": ["FFM.pdf"],
    "FGO": ["FGO.pdf"]
}


class DoctynRetriever:

    def __init__(self):
        self.documents = []
        self.vectorizer = None
        self.matrix = None
        self.load()

    def load(self):
        if not KNOWLEDGE_FILE.exists():
            print(
                "Knowledge index not found. "
                "Run ingest_service_v3.py first."
            )
            return

        with open(
            KNOWLEDGE_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            self.documents = json.load(file)

        texts = [
            document["content"]
            for document in self.documents
        ]

        if not texts:
            return

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=50000
        )

        self.matrix = self.vectorizer.fit_transform(texts)

        print(
            f"Doctyn Retriever loaded "
            f"{len(self.documents)} knowledge chunks."
        )

    def search(
        self,
        query,
        top_k=5,
        program_code=None
    ):

        if (
            not self.documents
            or self.vectorizer is None
            or self.matrix is None
        ):
            return []

        query_vector = self.vectorizer.transform([query])

        scores = cosine_similarity(
            query_vector,
            self.matrix
        )[0]

        ranked_indexes = scores.argsort()[::-1]

        allowed_files = None

        if program_code:
            allowed_files = PROGRAM_FILES.get(
                program_code.upper()
            )

        results = []

        for index in ranked_indexes:

            document = self.documents[index]

            if (
                allowed_files
                and document["source_name"] not in allowed_files
            ):
                continue

            score = float(scores[index])

            if score <= 0:
                continue

            results.append({
                "score": round(score, 4),
                "source_type": document["source_type"],
                "source_name": document["source_name"],
                "page": document.get("page"),
                "content": document["content"]
            })

            if len(results) >= top_k:
                break

        return results


retriever = DoctynRetriever()


def search_doctyn_knowledge(
    query,
    top_k=5,
    program_code=None
):
    return retriever.search(
        query,
        top_k=top_k,
        program_code=program_code
    )
