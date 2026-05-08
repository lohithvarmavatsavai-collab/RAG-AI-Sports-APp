import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

import streamlit as st

@st.cache_resource
def _load_resources():
    # Load once at module level so app.py doesn't reload on every query
    model = SentenceTransformer('all-MiniLM-L6-v2')
    index = faiss.read_index('faiss_index/sports_rag.index')
    chunks_df = pd.read_csv('chunks.csv')
    return model, index, chunks_df

def retrieve(query, sport_filter=None, category_filter=None, top_k=5):
    """
    Retrieve the top_k most relevant chunks for a given query.
    Optional filters for sport and category.
    Returns a list of dicts with chunk text and metadata.
    """
    _model, _index, _chunks_df = _load_resources()

    # Embed the query
    query_vec = _model.encode([query]).astype('float32')

    # Search FAISS — get more candidates if filtering
    search_k = top_k * 10 if (sport_filter or category_filter) else top_k
    distances, indices = _index.search(query_vec, search_k)

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue
        row = _chunks_df.iloc[idx]

        # Apply optional filters
        if sport_filter and row['sport'].lower() != sport_filter.lower():
            continue
        if category_filter and row['category'].lower() != category_filter.lower():
            continue

        results.append({
            'chunk_id': row['chunk_id'],
            'source_id': row['source_id'],
            'sport': row['sport'],
            'category': row['category'],
            'title': row['title'],
            'organization': row['organization'],
            'text': row['text'],
            'score': float(dist)  # Lower L2 distance = more relevant
        })

        if len(results) >= top_k:
            break

    return results


if __name__ == '__main__':
    # Quick test
    test_query = "How much protein does a strength training athlete need?"
    results = retrieve(test_query, sport_filter='Strength Training', category_filter='Nutrition', top_k=3)
    print(f"\nQuery: {test_query}\n")
    for i, r in enumerate(results):
        print(f"--- Result {i+1} ---")
        print(f"Source: {r['title']} ({r['organization']})")
        print(f"Text: {r['text'][:200]}...")
        print(f"L2 Score: {r['score']:.4f}\n")
