import requests
from pathlib import Path
# ID of the book to download (example: a Python book)
book_id = "1503212300"  # You can find this ID from dBooks search results
# Set output path to current working directory
output_path = Path.cwd()
# Fetch book details from dBooks API
details_url = f"https://www.dbooks.org/api/book/{book_id}"
response = requests.get(details_url)
book = response.json()
# Display book information
print(f"📖 Title: {book['title']}")
print(f"✍️ Author: {book['authors']}")
print(f"📥 Download Link: {book['download']}")
# Download the PDF file
download_url = book['download']
file_response = requests.get(download_url)
# Save the file in the current working directory
file_name = f"{book['title'].replace(' ', '_')}.pdf"
file_path = output_path / file_name
with open(file_path, "wb") as f:
   f.write(file_response.content)
print(f"✅ Book saved to: {file_path}")