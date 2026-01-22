import os
import json
import re
import cv2
import pytesseract

# -------- REGEX PATTERNS --------
DOB_PATTERN = r'(\d{2}[/-]\d{2}[/-]\d{4}|\d{4}[/-]\d{2}[/-]\d{2})'
GENDER_PATTERN = r'\b(Male|Female|M|F)\b'
PAN_PATTERN = r'\b[A-Z]{5}[0-9]{4}[A-Z]\b'
AADHAAR_PATTERN = r'\b\d{4}\s\d{4}\s\d{4}\b'
DRIVING_LICENSE_PATTERN = r'\b[A-Z]{2}[- ]?\d{13,15}\b'
PASSPORT_PATTERN = r'\b[A-Z][0-9]{7}\b'

DOC_MAP = {
    "aadhaar": "Aadhaar",
    "pan": "PAN",
    "passport": "Passport",
    "driving_license": "Driving License"
}

def extract(pattern, text):
    m = re.search(pattern, text)
    return m.group(0) if m else None

def build_json(ocr_text, document_type):
    return {
        "document_type": document_type,
        "first_name": "",
        "last_name": "",
        "date_of_birth": extract(DOB_PATTERN, ocr_text),
        "gender": extract(GENDER_PATTERN, ocr_text),
        "document_number": (
            extract(PAN_PATTERN, ocr_text) or
            extract(AADHAAR_PATTERN, ocr_text) or
            extract(DRIVING_LICENSE_PATTERN, ocr_text) or
            extract(PASSPORT_PATTERN, ocr_text)
        ),
        "address": None
    }

def process_folder(image_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(image_dir):
        if not file.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        image_path = os.path.join(image_dir, file)
        image = cv2.imread(image_path)
        if image is None:
            continue

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ocr_text = pytesseract.image_to_string(gray)

        doc_key = file.split("_")[0].lower()
        document_type = DOC_MAP.get(doc_key, "Unknown")

        json_data = build_json(ocr_text, document_type)

        json_filename = os.path.splitext(file)[0] + ".json"
        json_path = os.path.join(output_dir, json_filename)

        with open(json_path, "w") as f:
            json.dump(json_data, f, indent=2)

        print("✅ Saved:", json_filename)

# -------- RUN --------
if __name__ == "__main__":
    IMAGE_DIR = "test_images"          # or train_images
    OUTPUT_DIR = "test_expected_output"  # or train_annotations

    process_folder(IMAGE_DIR, OUTPUT_DIR)
