from transformers import pipeline, AutoTokenizer
import pandas as pd
import re
import torch

# Load model and tokenizer
segmenter = pipeline(
        "token-classification",
        model="PleIAs/Segmentext",
        aggregation_strategy="simple",
        device=0 if torch.cuda.is_available() else -1
)
tokenizer = AutoTokenizer.from_pretrained("PleIAs/Segmentext")

def segment_glm_ocr_text(ocr_text, max_tokens=500):
    # Replace newlines with ¶ separator (Segmentext expects this)
    editorial_text = re.sub(r"\n", " ¶ ", ocr_text)

    # Tokenize the full text
    tokens = tokenizer.tokenize(editorial_text)

    # Split into token-based chunks
    token_chunks = [tokens[i:i+max_tokens] for i in range(0, len(tokens), max_tokens)]

    # Convert token chunks back to text
    text_chunks = [tokenizer.convert_tokens_to_string(chunk) for chunk in token_chunks]

    # Run segmentation
    results = []
    for chunk in segmenter(text_chunks):
        results.extend(chunk)

    # Filter & format
    df = pd.DataFrame(results)
    df = df[df['entity_group'] != 'separator']
    df['word'] = df['word'].str.replace('¶', '\n', regex=False).str.strip()
    df = df[df['word'].str.len() > 0]

    return df[['entity_group', 'word']].to_dict('records')