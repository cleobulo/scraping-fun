import argparse
import re

def get_url_from_arg():
    """
    Parses command line arguments to get the URL for scraping.
    """
    # Create argument parser
    # and add the URL argument
    parser = argparse.ArgumentParser(description="URL base for scraping.")
    parser.add_argument("url", help="Initial URL to scraping.")
    args = parser.parse_args()
    url = args.url

    # Validate the URL format using regex
    if not re.match(r'^https?://', url):
        raise ValueError("Invalid URL format. Please provide a valid URL.")

    print(f"Scraping started at: {url}")

    # Return the URL if valid
    return url
