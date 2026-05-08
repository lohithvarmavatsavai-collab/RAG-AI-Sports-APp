import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

def main():
    print("Loading chunks...")
    chunks_df = pd.read_csv('chunks.csv')
    texts = chunks_df['text'].tolist()
    
    print("Loading embedding model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print(f"Generating embeddings for {len(texts)} chunks...")
    embeddings = model.encode(texts, show_progress_bar=True)
    embeddings = np.array(embeddings).astype('float32')
    
    print("Building FAISS index...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    
    os.makedirs('faiss_index', exist_ok=True)
    faiss.write_index(index, 'faiss_index/sports_rag.index')
    
    print("Index saved successfully to faiss_index/sports_rag.index")

if __name__ == '__main__':
    main()
