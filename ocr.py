import ollama
from pathlib import Path

def ocr_with_ollama(image_path, model_name="glm-ocr"):
    if not Path(image_path).exists():
        print(f"Error: File {image_path} not found.")
        return None

    try:
        response = ollama.chat(
                model=model_name,
                messages=[{
                        'role': 'user',
                        'content': 'Text Recognition:',
                        'images': [image_path]
                }]
        )

        text_content = response['message']['content']
        return text_content

    except Exception as e:
        return f"An error occurred: {e}"

