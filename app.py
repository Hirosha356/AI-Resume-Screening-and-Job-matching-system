from flask import Flask, render_template, request
import os
from resume_parser import extract_text
from similarity import calculate_similarity

UPLOAD_FOLDER = "uploads/resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# store resume data
resume_data = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():

    global resume_data
    resume_data = {}

    job_description = request.form['job_description']
    files = request.files.getlist("resumes")

    results = []
    seen_resumes = set()

    skills_list = [
        "python","java","javascript","sql","html","css",
        "react","django","flask","tensorflow","pytorch",
        "pandas","numpy","scikit-learn","docker",
        "git","jupyter","powerbi","tableau"
    ]

    job_desc = job_description.lower()
    recruiter_skills = [skill for skill in skills_list if skill in job_desc]

    for file in files:

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        resume_text = extract_text(filepath)

        if not resume_text:
            resume_text = "No content extracted from resume."

        resume_text_lower = resume_text.lower()

        # duplicate detection
        if resume_text_lower in seen_resumes:
            results.append({
                "name": file.filename,
                "score": "Duplicate",
                "matched": "-",
                "missing": "-"
            })
            continue

        seen_resumes.add(resume_text_lower)

        matched = []
        missing = []

        for skill in recruiter_skills:
            if skill in resume_text_lower:
                matched.append(skill)
            else:
                missing.append(skill)

        score = calculate_similarity(job_description, resume_text)

        if len(matched) == 0:
            score = 0

        # store resume data
        resume_data[file.filename] = {
            "text": resume_text,
            "matched": matched,
            "missing": missing
        }

        results.append({
            "name": file.filename,
            "score": round(score * 100, 2),
            "matched": ", ".join(matched),
            "missing": ", ".join(missing)
        })

    # sort results
    results = sorted(
        results,
        key=lambda x: 0 if x["score"] == "Duplicate" else x["score"],
        reverse=True
    )

    # ⭐ Recommended candidate (top non-duplicate)
    best_candidate = None
    for r in results:
        if r["score"] != "Duplicate":
            best_candidate = r["name"]
            break

    # 📋 Shortlisted candidates (≥ 20%)
    shortlisted = [
        r for r in results
        if isinstance(r["score"], float) and r["score"] >= 20
    ]

    return render_template(
        "result.html",
        results=results,
        best=best_candidate,
        shortlisted=shortlisted
    )


@app.route('/resume/<name>')
def resume_detail(name):

    data = resume_data.get(name)

    if not data:
        return "Resume not found"

    text = data["text"]

    sections = {
        "role": "",
        "languages": "",
        "frameworks": "",
        "tools": "",
        "projects": ""
    }

    lower_text = text.lower()

    try:
        if "role:" in lower_text:
            sections["role"] = text.split("Role:")[1].split("Languages:")[0].strip()

        if "languages:" in lower_text:
            sections["languages"] = text.split("Languages:")[1].split("Libraries/Frameworks:")[0].strip()

        if "libraries/frameworks:" in lower_text:
            sections["frameworks"] = text.split("Libraries/Frameworks:")[1].split("Tools:")[0].strip()

        if "tools:" in lower_text:
            sections["tools"] = text.split("Tools:")[1].split("Projects:")[0].strip()

        if "projects:" in lower_text:
            sections["projects"] = text.split("Projects:")[1].strip()

    except:
        pass

    return render_template(
        "detail.html",
        name=name,
        matched=", ".join(data["matched"]),
        missing=", ".join(data["missing"]),
        sections=sections
    )


if __name__ == '__main__':
    app.run(debug=True)