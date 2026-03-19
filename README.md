# 🚀 AI Resume Screening and Job Matching System

An AI-powered resume screening system that analyzes resumes using Natural Language Processing (NLP) and ranks candidates based on job description similarity.

---

## 🧠 Description
This project helps automate the hiring process by screening resumes and identifying the best candidates efficiently. It extracts text from resumes and compares it with a given job description using similarity algorithms.

---

## 🚀 Features
- 📄 Upload resumes (PDF/DOCX)
- 🧠 Extract text using NLP
- 📊 Calculate similarity score
- 🏆 Rank candidates based on relevance
- 🔍 Identify matched and missing skills
- ⚡ Fast and automated screening process

---

## 🛠️ Tech Stack
- Python
- Flask
- Scikit-learn (TF-IDF, Cosine Similarity)
- NLTK / SpaCy
- HTML, CSS, JavaScript

---

## 📊 How It Works
1. Upload resume
2. Extract text from resume
3. Input job description
4. Apply TF-IDF vectorization
5. Compute cosine similarity
6. Display score and ranking

---

## ▶️ How to Run
```bash
pip install -r requirements.txt
python app.py
