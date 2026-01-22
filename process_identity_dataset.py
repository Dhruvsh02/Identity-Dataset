import os
import json
import re
import cv2
import pytesseract
from tqdm import tqdm

BASE_DIR = os.getcwd()


print("BASE_DIR:", BASE_DIR)
print("EXISTS:", os.path.exists(BASE_DIR))
print("CONTENT:", os.listdir(BASE_DIR))


SETS = {
    "train": {
        "img_out": "train_images",
        "json_out": "train_annotations"
    },
    "test": {
        "img_out": "test_images",
        "json_out": "test_expected_output"
    }
}

DOC_MAP = {
    "aadhaar": "Aadhaar",
    "pan": "PAN",
    "passport": "Passport",
    "driving_license": "Driving License"
}

# ---------- REGEX ----------
DOB = r'(\d{2}[/-]\d{2}[/-]\d{4}|\d{4}[/-]\d{2}[/-]\d{2})'
GENDER = r'\b(Male|Female|M|F)\b'
PAN = r'\b[A-Z]{5}[0-9]{4}[A-Z]\b'
AADHAAR = r'\b\d{4}\s\d{4}\s\d{4}\b'
DRIVING_LICENSE = r'\b[A-Z]{2}[- ]?\d{13,15}\b'
PASSPORT = r'\b[A-Z][0-9]{7}\b'

def extract(text, pattern):
    m = re.search(pattern, text)
    return m.group(0) if m else None

# ---------- PROCESS ----------
for split in SETS:
    img_out = os.path.join(BASE_DIR, SETS[split]["img_out"])
    json_out = os.path.join(BASE_DIR, SETS[split]["json_out"])

    os.makedirs(img_out, exist_ok=True)
    os.makedirs(json_out, exist_ok=True)

    counter = 1

    for folder in DOC_MAP:
        input_dir = os.path.join(BASE_DIR, split, folder)
        if not os.path.exists(input_dir):
            continue

        for file in tqdm(os.listdir(input_dir), desc=f"{split}-{folder}"):
            if not file.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue

            new_name = f"{folder}_{split}_{counter:03d}.jpg"
            counter += 1

            src = os.path.join(input_dir, file)
            dst = os.path.join(img_out, new_name)

            image = cv2.imread(src)
            cv2.imwrite(dst, image)

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray)

            doc_number = (
                extract(text, PAN) or
                extract(text, AADHAAR) or
                extract(text, DRIVING_LICENSE) or
                extract(text, PASSPORT)
            )

            data = {
                "document_type": DOC_MAP[folder],
                "first_name": "",
                "last_name": "",
                "date_of_birth": extract(text, DOB),
                "gender": extract(text, GENDER),
                "document_number": doc_number,
                "address": None
            }

            json_name = new_name.replace(".jpg", ".json")
            with open(os.path.join(json_out, json_name), "w") as f:
                json.dump(data, f, indent=2)

print("✅ Train & Test processing completed successfully.")
