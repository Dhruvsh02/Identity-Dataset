import os
import cv2
import pytesseract
import json
import re
from tqdm import tqdm

# =========================
# CONFIG
# =========================
BASE_DIR = os.getcwd()   # identity_dataset folder
IMAGE_DIR = "test_images"        # change to train_images if needed
OUTPUT_DIR = "test_expected_output"  # change to train_annotations if needed

os.makedirs(OUTPUT_DIR, exist_ok=True)

DOC_MAP = {
    "aadhaar": "Aadhaar",
    "pan": "PAN",
    "passport": "Passport",
    "driving_license": "Driving License"
}

# =========================
# REGEX PATTERNS
# =========================
DOB_PATTERN = r'(\d{2}[/-]\d{2}[/-]\d{4}|\d{4}[/-]\d{2}[/-]\d{2})'
GENDER_PATTERN = r'\b(Male|Female|M|F)\b'
PAN_PATTERN = r'\b[A-Z]{5}[0-9]{4}[A-Z]\b'
AADHAAR_PATTERN = r'\b\d{4}\s\d{4}\s\d{4}\b'
DRIVING_LICENSE_PATTERN = r'\b[A-Z]{2}[- ]?\d{13,15}\b'
PASSPORT_PATTERN = r'\b[A-Z][0-9]{7}\b'

# =========================
# HELPERS
# =========================
def extract(pattern, text):
    m = re.search(pattern, text)
    return m.group(0) if m else None

def extract_name(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    for line in lines:
        if "name" in line.lower():
            parts = line.split(":")
            if len(parts) > 1:
                name = parts[1].strip()
                words = name.split()
                if len(words) >= 2:
                    return words[0], " ".join(words[1:])
                elif len(words) == 1:
                    return words[0], ""
    return "", ""

# =========================
# MAIN PROCESS
# =========================
def process_images():
    for file in tqdm(os.listdir(IMAGE_DIR)):
        if not file.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        image_path = os.path.join(IMAGE_DIR, file)
        image = cv2.imread(image_path)
        if image is None:
            continue

        # ---- OCR PREPROCESSING ----
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 0, 255,
                              cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        config = r'--oem 3 --psm 6'
        ocr_text = pytesseract.image_to_string(gray, config=config)

        # ---- DOCUMENT TYPE FROM FILENAME ----
        doc_key = file.split("_")[0].lower()
        document_type = DOC_MAP.get(doc_key, "Unknown")

        # ---- FIELD EXTRACTION ----
        first_name, last_name = extract_name(ocr_text)

        document_number = (
            extract(PAN_PATTERN, ocr_text) or
            extract(AADHAAR_PATTERN, ocr_text) or
            extract(DRIVING_LICENSE_PATTERN, ocr_text) or
            extract(PASSPORT_PATTERN, ocr_text)
        )

        data = {
            "document_type": document_type,
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": extract(DOB_PATTERN, ocr_text),
            "gender": extract(GENDER_PATTERN, ocr_text),
            "document_number": document_number,
            "address": None
        }

        json_name = os.path.splitext(file)[0] + ".json"
        json_path = os.path.join(OUTPUT_DIR, json_name)

        with open(json_path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"✅ Saved: {json_name}")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    print("Processing images from:", IMAGE_DIR)
    process_images()
    print("🎉 All JSON files generated successfully.")
