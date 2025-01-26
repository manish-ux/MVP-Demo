import pytesseract
from pytesseract import Output
from pdf2image import convert_from_path
import cv2
import os
import json

def pdf_to_images(pdf_path, output_folder="temp_images"):
    """Convert a PDF file into images, one per page."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    images = convert_from_path(pdf_path)
    image_paths = []
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f"page_{i + 1}.jpg")
        image.save(image_path, "JPEG")
        image_paths.append(image_path)
    return image_paths

def extract_text_from_image(image_path):
    """Extract text from an image using OCR."""
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    processed_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_string(processed_image, lang='eng')
    return text

def extract_structured_data(text):
    """Convert raw text into structured data."""
    # A simple implementation to parse key-value pairs. Customize as needed.
    lines = text.split("\n")
    structured_data = {}
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            structured_data[key.strip()] = value.strip()
    return structured_data

def process_pdf(pdf_path):
    """Process the PDF and return structured data."""
    image_paths = pdf_to_images(pdf_path)
    extracted_data = []
    for image_path in image_paths:
        text = extract_text_from_image(image_path)
        structured_data = extract_structured_data(text)
        extracted_data.append(structured_data)
    return extracted_data

def main():
    pdf_path = "sample.pdf"  # Replace with your PDF path
    output_json_path = "output.json"

    print("Processing PDF...")
    extracted_data = process_pdf(pdf_path)

    print("Saving structured data to JSON file...")
    with open(output_json_path, "w") as json_file:
        json.dump(extracted_data, json_file)

    print(f"Data saved to {output_json_path}")

if __name__ == "__main__":
    main()
