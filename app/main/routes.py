from flask import render_template, flash, redirect, url_for, request
from . import main
from .forms import ResumeForm
from models.resume_parser import parse_resume, extract_text_from_file
from models.job_description_parser import parse_job_description
from models.resume_scorer import score_resume, generate_feedback
from werkzeug.utils import secure_filename
import os
from PyPDF2 import PdfReader

ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ''
    for page_num in range(reader.numPages):
        page = reader.getPage(page_num)
        text += page.extract_text()
    return text

@main.route('/', methods=['GET', 'POST'])
def index():
    print("Route accessed")  # Debug print
    form = ResumeForm()
    if form.validate_on_submit():
        print("Form submitted")  # Debug print
        try:
            resume_file = form.resume.data
            if resume_file and allowed_file(resume_file.filename):
                print(f"Processing file: {resume_file.filename}")  # Debug print
                resume_file.seek(0)
                filename = secure_filename(resume_file.filename)
                file_extension = filename.rsplit('.', 1)[1].lower()
                
                resume_text = extract_text_from_file(resume_file, file_extension)
                print(f"Extracted text length: {len(resume_text)}")  # Debug print
                
                resume_data = parse_resume(resume_text)
                print(f"Parsed resume data: {resume_data}")  # Debug print
                
                job_description_data = parse_job_description(
                    form.job_description.data,
                    form.job_responsibilities.data if hasattr(form, 'job_responsibilities') else "",
                    form.job_experience.data if hasattr(form, 'job_experience') else "",
                    form.job_skills.data,
                    form.job_education.data if hasattr(form, 'job_education') else ""
                )
                
                scores = score_resume(resume_data, job_description_data)
                feedback = generate_feedback(resume_data, job_description_data)
                
                print(f"Scores: {scores}")  # Debug print
                print(f"Feedback: {feedback}")  # Debug print
                
                return render_template('results.html', 
                                    scores=scores, 
                                    feedback=feedback)
            else:
                print("Invalid file type",form.errors)  # Debug print
                flash('Please upload a valid PDF or DOCX file.', 'error')
        except Exception as e:
            print(f"Error occurred: {str(e)}")  # Debug print
            flash(f'Error processing resume: {str(e)}', 'error')
    
    return render_template('index.html', form=form)
