# Identity-Dataset

## 1. Objective

The objective of this dataset is to support the development and evaluation of an AI-based system
for extracting structured information from Indian identity documents. The dataset is designed
to handle real-world challenges such as varied document layouts, image quality issues, and OCR
limitations.

The fields extracted include:
- First Name
- Last Name
- Date of Birth
- Gender
- Document Number
- Address (if present)
- Document Type

---

## 2. Documents Covered

The dataset includes the following identity documents:
- Aadhaar Card
- PAN Card
- Passport
- Driving License

Only the front side of documents is mandatory. Back-side images are included where available.

---

## 3. Dataset Composition

### Training Dataset
- Contains document images along with annotated ground-truth JSON files
- Used for training and learning extraction patterns

### Test Dataset
- Contains document images along with expected output JSON files
- Used for evaluation and validation

---

## 4. Data Sources Used

The dataset was created using publicly available and open-source resources, including:

- Kaggle open-source document and OCR datasets
- Public GitHub repositories related to document understanding and OCR
- Sample and template-based identity document images used strictly for academic purposes

Due to limited availability of open-source Indian Driving License datasets, some Driving License
samples were synthetically created or adapted from publicly available templates while maintaining
realistic document structure.

All sensitive personal information has been anonymized or masked to ensure privacy.

---

## 5. Annotation Rules

- One JSON file is created per document image
- Extracted values are stored without truncation
- Date of Birth is standardized where possible
- Multi-line addresses are merged into a single string
- If a field is unreadable or not present, the value is set to null
- Document type is explicitly mentioned in each JSON file

Annotations were generated using an OCR-assisted pipeline followed by manual verification.

---

## 6. Edge Cases Covered

The dataset includes challenging real-world scenarios such as:
- Low-resolution images
- Motion blur and skewed documents
- Partial occlusion of text
- Masked or partially hidden document numbers
- Multi-line address fields
- Mixed language text (English and regional languages)

---

## 7. Known Limitations

- OCR-based extraction may fail for low-quality or highly blurred images
- Some name and address fields could not be extracted due to document layout variations
- Driving License data is partially synthetic due to limited open-source availability
- OCR accuracy depends heavily on image quality and lighting conditions

These limitations reflect real-world document processing challenges.

---

## 8. Conclusion

This dataset provides a realistic and diverse collection of Indian identity documents suitable
for training and evaluating document information extraction models. Despite OCR limitations,
the dataset represents real-world variability and supports robust model evaluation.



## Author
* **Dhruv Sharma**