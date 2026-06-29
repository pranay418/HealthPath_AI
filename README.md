# HealthPath_AI

## Abstract

HealthPath_AI is an AI-powered healthcare assistant that analyzes medical reports (PDF, image, or manual input) using OCR and rule-based analysis. It identifies possible health conditions and generates personalized daily schedules, diet recommendations, lifestyle tips, and wellness scores to help patients improve their health.

---

## Keywords

**Artificial Intelligence (AI), Optical Character Recognition (OCR), Healthcare, Medical Report Analysis, Personalized Healthcare, Wellness Score, Streamlit, Python**

---

## 1. Introduction

HealthPath_AI helps patients understand medical reports by converting them into personalized health recommendations. It simplifies report analysis and promotes preventive healthcare through AI-assisted suggestions.

---

## 2. Problem Statement

Patients often find medical reports difficult to understand and lack personalized guidance for improving their health.

---

## 3. Objectives

* Analyze medical reports.
* Extract data using OCR.
* Detect health conditions.
* Generate personalized schedules.
* Recommend diet and lifestyle improvements.
* Calculate wellness scores.

---

## 4. Methodology

1. Upload report.
2. Extract text using OCR.
3. Process medical data.
4. Analyze health conditions.
5. Generate recommendations and wellness score.

---

## 5. Literature Review

Most healthcare systems focus on storing medical records. HealthPath_AI goes further by analyzing reports and providing personalized health recommendations.

---

## 6. System Architecture

```text
User Input
     │
     ▼
 OCR Extraction
     │
     ▼
Health Analysis
     │
     ▼
Recommendations
     │
     ▼
Dashboard
```

---

## 7. Features

* PDF/Image report upload
* OCR-based text extraction
* Manual report entry
* Health condition detection
* Diet recommendations
* Daily schedule generation
* Wellness score
* User-friendly dashboard

---

## 8. Implementation

The project is built with Python and Streamlit. OCR extracts report data, which is analyzed using rule-based logic to generate personalized health recommendations.

---

## 9. Tech Stack

* Python
* Streamlit
* Tesseract OCR
* Pandas
* SQLite
* Pillow

---

## 10. Project Modules

* Report Upload
* OCR Processing
* Health Analysis
* Recommendation Engine
* Wellness Score
* Dashboard

---

## 11. Project Structure

```text
HealthPath_AI/
│── app.py
│── requirements.txt
│── packages.txt
│── database.db
│── utils/
│── uploads/
│── assets/
└── README.md
```

---

## 12. Installation

```bash
git clone <repository-link>
cd HealthPath_AI
pip install -r requirements.txt
streamlit run app.py
```

---

## 13. Results

The system successfully analyzes medical reports, identifies health conditions, and generates personalized schedules, diet suggestions, and wellness scores.

---

## 14. Conclusion

HealthPath_AI simplifies medical report interpretation and helps users improve their health through personalized AI-assisted recommendations.

---

## 15. Future Scope

* Machine Learning integration
* Wearable device support
* Medicine reminders
* Multi-language support
* Mobile application

---

## 16. References

1. World Health Organization (WHO)
2. Tesseract OCR Documentation
3. Streamlit Documentation
4. Python Documentation
5. SQLite Documentation
