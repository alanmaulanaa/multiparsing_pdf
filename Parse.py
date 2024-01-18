import os
import fitz
from glob import glob
import csv
import re

def cleanup_text(raw_text):
    # Remove extra whitespaces and newline characters
    cleaned_text = re.sub(r'\s+', ' ', raw_text).strip()
    return cleaned_text

script_directory = os.path.dirname(os.path.abspath(__file__))
pdf_folder = os.path.join(script_directory, 'PDF_Folder')
output_csv = os.path.join(script_directory, 'output.csv')

# Get a list of all PDF files in the folder
pdf_files = glob(os.path.join(pdf_folder, '*.pdf'))

data = []

for pdf_path in pdf_files:
    print(f"Processing file: {pdf_path}")

    # Open the PDF file
    doc = fitz.open(pdf_path)
    text = ""

    # Extract text from each page
    for page in doc:
        text += page.get_text()

    # Cleanup the text
    cleaned_text = cleanup_text(text)

    # Append the data to the list
    data.append({'File': os.path.basename(pdf_path), 'Text': cleaned_text})

    doc.close()
    print("-------------------------------")

# Save the data to a CSV file
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['File', 'Text']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Write the data
    writer.writerows(data)

print(f"CSV file saved at: {output_csv}")
