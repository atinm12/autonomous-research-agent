import chromadb

from sentence_transformers import (
    SentenceTransformer
)


# -----------------------------------
# INITIALIZE VECTOR DATABASE
# -----------------------------------

client = chromadb.Client()

collection = client.get_or_create_collection(
    name="research_memory"
)


# -----------------------------------
# EMBEDDING MODEL
# -----------------------------------

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# -----------------------------------
# CHUNKING CONFIGURATION
# -----------------------------------

chunk_size = 250

overlap = 40


# -----------------------------------
# TEXT CHUNKING
# -----------------------------------

def chunk_text(text):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(
            words[start:end]
        )

        chunks.append(chunk)

        start += (
            chunk_size - overlap
        )

    return chunks


# -----------------------------------
# STORE MEMORY
# -----------------------------------

def store_memory(document, metadata=None):

    chunks = chunk_text(document)

    stored_ids = []

    for index, chunk in enumerate(chunks):

        embedding = (
            embedding_model.encode(chunk)
            .tolist()
        )

        doc_id = (
            f"{hash(chunk)}_{index}"
        )

        collection.add(

            ids=[doc_id],

            documents=[chunk],

            embeddings=[embedding],

            metadatas=[
                metadata or {}
            ]
        )

        stored_ids.append(doc_id)

    return (
        f"Stored {len(stored_ids)} "
        f"chunks in memory"
    )


# -----------------------------------
# SEARCH MEMORY
# -----------------------------------

def search_memory(
    query,
    n_results=3
):

    query_embedding = (
        embedding_model.encode(query)
        .tolist()
    )

    results = collection.query(

        query_embeddings=[
            query_embedding
        ],

        n_results=n_results
    )

    return results