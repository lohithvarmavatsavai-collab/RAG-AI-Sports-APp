import os
import pandas as pd
import re

def clean_text(text):
    # Remove excessive newlines and spaces
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    # Strip leading/trailing whitespace
    text = text.strip()
    return text

def main():
    raw_dir = 'data_raw'
    clean_dir = 'data_clean'
    os.makedirs(clean_dir, exist_ok=True)
    
    metadata = pd.read_csv('metadata.csv')
    
    print(f"Cleaning {len(metadata)} files...")
    for index, row in metadata.iterrows():
        filename = row['filename']
        raw_path = os.path.join(raw_dir, filename)
        clean_path = os.path.join(clean_dir, filename)
        
        if os.path.exists(raw_path):
            with open(raw_path, 'r', encoding='utf-8') as f:
                raw_text = f.read()
            
            cleaned_text = clean_text(raw_text)
            
            with open(clean_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_text)
        else:
            print(f"Warning: File {raw_path} not found.")
            
    print("Data cleaning complete. Cleaned files saved to data_clean/")

if __name__ == '__main__':
    main()
