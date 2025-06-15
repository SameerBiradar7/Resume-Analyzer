from flask_wtf import FlaskForm
from wtforms import FileField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileAllowed  # ✅ REQUIRED IMPORT

class ResumeForm(FlaskForm):
    resume = FileField(
        'Upload Resume', 
        validators=[
            FileRequired(),
            FileAllowed(['pdf', 'docx'], 'PDF or DOCX only!')
        ]
    )
    job_title = StringField('Job Title', validators=[DataRequired()])
    job_description = TextAreaField('Job Description', validators=[DataRequired()])
    job_responsibilities = TextAreaField('Job Responsibilities', validators=[DataRequired()])
    job_experience = TextAreaField('Required Experience', validators=[DataRequired()])
    job_skills = TextAreaField('Required Skills', validators=[DataRequired()])
    job_education = TextAreaField('Required Education', validators=[DataRequired()])
    submit = SubmitField('Submit')
