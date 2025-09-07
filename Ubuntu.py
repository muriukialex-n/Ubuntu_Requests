import requests
import os
from urllib.parse import urlparse
import hashlib

def get_filename_from_url(url, response_content):
    """Extract filename from URL or generate one using hash for uniqueness"""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    
    if not filename:  # No filename in the URL
        # Use a hash of the content to generate a unique filename
        file_hash = hashlib.md5(response_content).hexdigest()
        filename = f"image_{file_hash}.jpg"
        
    return filename

def fetch_image(url, save_dir, existing_files):
    """Fetch an image from the URL and save it, avoiding duplicates."""
    try:
        # Request with headers to simulate respectful client behavior
        headers = {
            "User-Agent": "UbuntuImageFetcher/1.0",
            "Accept": "image/*"
        }
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()  # Ensure no HTTP errors
        
        # Check if content is actually an image
        if "image" not in response.headers.get("Content-Type", ""):
            print(f"✗ Skipped: {url} (Not an image)")
            return
        
        # Determine filename
        filename = get_filename_from_url(url, response.content)
        filepath = os.path.join(save_dir, filename)
        
        # Avoid duplicates
        if filename in existing_files:
            print(f"✗ Skipped duplicate: {filename}")
            return
        
        # Save the image
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        existing_files.add(filename)
        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error for {url}: {e}")
    except Exception as e:
        print(f"✗ An error occurred for {url}: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")
    
    # Get one or multiple URLs
    urls = input("Please enter one or more image URLs (separated by commas): ").split(",")
    urls = [u.strip() for u in urls if u.strip()]
    
    # Create directory if it doesn't exist
    save_dir = "Fetched_Images"
    os.makedirs(save_dir, exist_ok=True)
    
    # Track existing files for duplicate prevention
    existing_files = set(os.listdir(save_dir))
    
    # Fetch each image
    for url in urls:
        fetch_image(url, save_dir, existing_files)
    
    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
