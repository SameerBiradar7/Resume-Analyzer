import spacy
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    print("Downloading language model...")
    from spacy.cli import download
    download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')
import docx
from PyPDF2 import PdfReader

nlp = spacy.load('en_core_web_sm')


import docx
from PyPDF2 import PdfReader

def extract_text_from_file(file, file_extension):
    """
    Extract text from a file based on its extension.
    Supports 'pdf', 'docx'.
    """
    if file_extension == 'pdf':
        reader = PdfReader(file)
        text = ''
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    elif file_extension == 'docx':
        doc = docx.Document(file)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    else:
        raise ValueError("Unsupported file extension: {}".format(file_extension))


def extract_section(text, section_title):
    section = []
    in_section = False
    for line in text.split("\n"):
        if section_title.lower() in line.lower():
            in_section = True
        elif in_section and line.strip() == "":
            break
        elif in_section:
            section.append(line)
    return "\n".join(section)


def parse_resume(resume_text):
    doc = nlp(resume_text)
    skills = extract_section(resume_text, 'skills')
    experience = extract_section(resume_text, 'experience')
    education = extract_section(resume_text, 'education')

    return {
        'skills': skills.lower(),
        'experience': experience.lower(),
        'education': education.lower(),
        'entities': [ent.text for ent in doc.ents],
        'full_text': resume_text
    }
