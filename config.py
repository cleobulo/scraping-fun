from dotenv import load_dotenv

import os
import re

# Load environment variables from .env file
load_dotenv()

def get_settings():
    """    Obtém a URL inicial a partir de variáveis de ambiente.
    Valida o formato da URL e retorna a URL se for válida.
    """
    url = os.getenv("SEED_URL")

    # Validate the URL format using regex
    if not re.match(r'^https?://', url):
        raise ValueError("Invalid URL format. Please provide a valid URL.")

    print(f"Scraping started at: {url}")

    # Return the URL if valid
    return url
