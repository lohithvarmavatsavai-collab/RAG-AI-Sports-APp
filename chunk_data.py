import os
import pandas as pd

def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if len(chunk.split()) > 20: # Keep chunks with at least 20 words
            chunks.append(chunk)
    return chunks

def main():
    clean_dir = 'data_clean'
    metadata = pd.read_csv('metadata.csv')
    
    all_chunks = []
    chunk_id_counter = 1
    
    print("Chunking data...")
    for index, row in metadata.iterrows():
        filename = row['filename']
        clean_path = os.path.join(clean_dir, filename)
        
        if os.path.exists(clean_path):
            with open(clean_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            chunks = chunk_text(text, chunk_size=150, overlap=30)
            
            for chunk in chunks:
                all_chunks.append({
                    'chunk_id': f"C{chunk_id_counter:04d}",
                    'source_id': row['source_id'],
                    'sport': row['sport'],
                    'category': row['category'],
                    'title': row['title'],
                    'organization': row['organization'],
                    'text': chunk
                })
                chunk_id_counter += 1
                
    chunks_df = pd.DataFrame(all_chunks)
    chunks_df.to_csv('chunks.csv', index=False)
    print(f"Created {len(chunks_df)} chunks and saved to chunks.csv")

if __name__ == '__main__':
    main()
