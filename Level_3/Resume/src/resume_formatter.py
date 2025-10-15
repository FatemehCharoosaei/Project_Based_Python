# resume_formatter.py
from datetime import date
def format_date(date_obj):
   """
   Safely format date objects to string.
   
   Args:
       date_obj: Can be date object, string, or any other type
       
   Returns:
       str: Formatted date string
   """
   if isinstance(date_obj, date):
       return date_obj.strftime("%B %Y")
   return str(date_obj) if date_obj else ""
def format_personal_info(info):
   """
   Format personal information section safely.
   
   Args:
       info: Dictionary containing personal info or other data type
       
   Returns:
       str: Formatted personal info in markdown
   """
   if not info:
       return ""
   
   # Handle case where info is a dictionary
   if isinstance(info, dict):
       markdown = f"### {info.get('full_name', 'Name Not Provided')}\n\n"
       
       contact_info = []
       if info.get('email'):
           contact_info.append(info['email'])
       if info.get('phone'):
           contact_info.append(info['phone'])
       if info.get('address'):
           address = info['address']
           if isinstance(address, dict):
               location = f"{address.get('city', '')}, {address.get('state', '')}, {address.get('country', '')}".strip(', ')
               if location:
                   contact_info.append(location)
       if info.get('linkedin'):
           contact_info.append(f"[LinkedIn]({info['linkedin']})")
       if info.get('github'):
           contact_info.append(f"[GitHub]({info['github']})")
       if info.get('website'):
           contact_info.append(f"[Website]({info['website']})")
       
       if contact_info:
           markdown += " | ".join(contact_info) + "\n\n"
       
       return markdown
   
   # Handle unexpected data types
   return f"### Personal Information\n\n{str(info)}\n\n"
def format_summary(summary):
   """
   Format summary section safely.
   
   Args:
       summary: String or other data type
       
   Returns:
       str: Formatted summary in markdown
   """
   if not summary:
       return ""
   return f"#### Summary\n\n{str(summary)}\n\n"
def format_work_experience(experience):
   """
   Format work experience section safely.
   
   Args:
       experience: List of dictionaries, list of strings, or other data type
       
   Returns:
       str: Formatted work experience in markdown
   """
   if not experience:
       return ""
   
   markdown = "#### Work Experience\n\n"
   
   # Handle list of dictionaries
   if isinstance(experience, list) and experience and isinstance(experience[0], dict):
       for job in experience:
           job_title = job.get('job_title', 'Position Not Specified')
           company = job.get('company', 'Company Not Specified')
           markdown += f"###### {job_title} | {company}\n"
           
           # Handle location
           location = ""
           job_location = job.get('location', {})
           if isinstance(job_location, dict):
               city = job_location.get('city', '')
               state = job_location.get('state', '')
               location = f"{city}, {state}".strip(', ')
           
           # Format dates
           start_date = format_date(job.get('start_date'))
           end_date = format_date(job.get('end_date'))
           dates = f"{start_date} - {end_date}".strip(' -')
           
           if location or dates:
               markdown += f"*{location + ' | ' if location else ''}{dates}*\n\n"
           
           # Handle description
           description = job.get('description', '')
           if description:
               markdown += f"{description}\n\n"
           
           # Handle achievements
           achievements = job.get('achievements', [])
           if achievements and isinstance(achievements, list):
               markdown += "**Key Achievements:**\n"
               for achievement in achievements:
                   markdown += f"- {achievement}\n"
               markdown += "\n"
       
       return markdown
   
   # Handle list of strings or other formats
   if isinstance(experience, list):
       for item in experience:
           markdown += f"- {str(item)}\n"
       return markdown + "\n"
   
   # Handle unexpected data types
   return f"#### Work Experience\n\n{str(experience)}\n\n"
def format_education(education):
   """
   Format education section safely.
   
   Args:
       education: List of dictionaries, list of strings, or other data type
       
   Returns:
       str: Formatted education in markdown
   """
   if not education:
       return ""
   
   markdown = "#### Education\n\n"
   
   # Handle list of dictionaries
   if isinstance(education, list) and education and isinstance(education[0], dict):
       for edu in education:
           degree = edu.get('degree', 'Degree Not Specified')
           field = edu.get('field_of_study', '')
           institution = edu.get('institution', 'Institution Not Specified')
           
           markdown += f"###### {degree} {('in ' + field) if field else ''} | {institution}\n"
           
           # Handle location
           location = ""
           edu_location = edu.get('location', {})
           if isinstance(edu_location, dict):
               city = edu_location.get('city', '')
               state = edu_location.get('state', '')
               location = f"{city}, {state}".strip(', ')
           
           # Format dates
           start_date = format_date(edu.get('start_date'))
           end_date = format_date(edu.get('end_date'))
           dates = f"{start_date} - {end_date}".strip(' -')
           
           if location or dates:
               markdown += f"*{location + ' | ' if location else ''}{dates}*\n\n"
           
           # Handle honors
           honors = edu.get('honors', [])
           if honors and isinstance(honors, list):
               markdown += "**Honors:**\n"
               for honor in honors:
                   markdown += f"- {honor}\n"
               markdown += "\n"
       
       return markdown
   
   # Handle list of strings or other formats
   if isinstance(education, list):
       for item in education:
           markdown += f"- {str(item)}\n"
       return markdown + "\n"
   
   # Handle unexpected data types
   return f"#### Education\n\n{str(education)}\n\n"
def format_skills(skills):
   """
   Format skills section safely.
   
   Args:
       skills: List of strings, string, or other data type
       
   Returns:
       str: Formatted skills in markdown
   """
   if not skills:
       return ""
   
   if isinstance(skills, list):
       skill_list = [str(skill) for skill in skills]
       return f"#### Skills\n\n{', '.join(skill_list)}\n\n"
   
   return f"#### Skills\n\n{str(skills)}\n\n"
def format_certifications(certifications):
   """
   Format certifications section safely handling both string and dictionary data types.
   
   Args:
       certifications: Can be a list of strings, list of dictionaries, or other formats
       
   Returns:
       str: Formatted certifications section in markdown
   """
   if not certifications:
       return ""
   
   # Handle case where certifications is a list of strings
   if isinstance(certifications, list) and certifications and isinstance(certifications[0], str):
       markdown = "#### Certifications\n\n"
       for cert in certifications:
           markdown += f"- {cert}\n"
       return markdown + "\n"
   
   # Handle case where certifications is a list of dictionaries
   if isinstance(certifications, list) and certifications and isinstance(certifications[0], dict):
       markdown = "#### Certifications\n\n"
       for cert in certifications:
           # Safely extract title using get() method for dictionaries
           title = cert.get('title', 'Certification Not Specified')
           issuer = cert.get('issuer', '')
           date_obtained = cert.get('date_obtained', '')
           
           markdown += f"- **{title}**"
           if issuer:
               markdown += f" - {issuer}"
           if date_obtained:
               formatted_date = format_date(date_obtained)
               markdown += f" (Obtained: {formatted_date})"
           markdown += "\n"
       return markdown + "\n"
   
   # Handle unexpected data types
   return f"#### Certifications\n\n{str(certifications)}\n\n"
def format_projects(projects):
   """
   Format projects section safely.
   
   Args:
       projects: List of dictionaries, list of strings, or other data type
       
   Returns:
       str: Formatted projects in markdown
   """
   if not projects:
       return ""
   
   markdown = "#### Projects\n\n"
   
   # Handle list of dictionaries
   if isinstance(projects, list) and projects and isinstance(projects[0], dict):
       for project in projects:
           title = project.get('title', 'Project Title Not Specified')
           markdown += f"###### {title}\n\n"
           
           description = project.get('description', '')
           if description:
               markdown += f"{description}\n\n"
           
           technologies = project.get('technologies', [])
           if technologies:
               if isinstance(technologies, list):
                   markdown += f"**Technologies used:** {', '.join(technologies)}\n"
               else:
                   markdown += f"**Technologies used:** {technologies}\n"
           
           url = project.get('url', '')
           if url:
               markdown += f"**URL:** [{url}]({url})\n"
           
           markdown += "\n"
       
       return markdown
   
   # Handle list of strings or other formats
   if isinstance(projects, list):
       for item in projects:
           markdown += f"- {str(item)}\n"
       return markdown + "\n"
   
   # Handle unexpected data types
   return f"#### Projects\n\n{str(projects)}\n\n"
def format_languages(languages):
   """
   Format languages section safely.
   
   Args:
       languages: List of dictionaries, list of strings, or other data type
       
   Returns:
       str: Formatted languages in markdown
   """
   if not languages:
       return ""
   
   markdown = "#### Languages\n\n"
   
   # Handle list of dictionaries
   if isinstance(languages, list) and languages and isinstance(languages[0], dict):
       for lang in languages:
           language = lang.get('language', 'Language Not Specified')
           proficiency = lang.get('proficiency', 'Proficiency Not Specified')
           markdown += f"- {language}: {proficiency}\n"
       return markdown + "\n"
   
   # Handle list of strings or other formats
   if isinstance(languages, list):
       for item in languages:
           markdown += f"- {str(item)}\n"
       return markdown + "\n"
   
   # Handle unexpected data types
   return f"#### Languages\n\n{str(languages)}\n\n"
def format_volunteer_experience(experience):
   """
   Format volunteer experience section safely.
   
   Args:
       experience: List of dictionaries, list of strings, or other data type
       
   Returns:
       str: Formatted volunteer experience in markdown
   """
   if not experience:
       return ""
   
   markdown = "#### Volunteer Experience\n\n"
   
   # Handle list of dictionaries
   if isinstance(experience, list) and experience and isinstance(experience[0], dict):
       for exp in experience:
           role = exp.get('role', 'Role Not Specified')
           organization = exp.get('organization', 'Organization Not Specified')
           markdown += f"###### {role} | {organization}\n"
           
           # Handle location
           location = ""
           exp_location = exp.get('location', {})
           if isinstance(exp_location, dict):
               city = exp_location.get('city', '')
               state = exp_location.get('state', '')
               location = f"{city}, {state}".strip(', ')
           
           # Format dates
           start_date = format_date(exp.get('start_date'))
           end_date = format_date(exp.get('end_date'))
           dates = f"{start_date} - {end_date}".strip(' -')
           
           if location or dates:
               markdown += f"*{location + ' | ' if location else ''}{dates}*\n\n"
           
           # Handle description
           description = exp.get('description', '')
           if description:
               markdown += f"{description}\n\n"
       
       return markdown
   
   # Handle list of strings or other formats
   if isinstance(experience, list):
       for item in experience:
           markdown += f"- {str(item)}\n"
       return markdown + "\n"
   
   # Handle unexpected data types
   return f"#### Volunteer Experience\n\n{str(experience)}\n\n"
def format_interests(interests):
   """
   Format interests section safely.
   
   Args:
       interests: List of strings, string, or other data type
       
   Returns:
       str: Formatted interests in markdown
   """
   if not interests:
       return ""
   
   if isinstance(interests, list):
       return f"#### Interests\n\n{', '.join(str(interest) for interest in interests)}\n\n"
   
   return f"#### Interests\n\n{str(interests)}\n\n"
def format_references(references):
   """
   Format references section safely.
   
   Args:
       references: List, string, or other data type
       
   Returns:
       str: Formatted references in markdown
   """
   if not references:
       return ""
   
   if isinstance(references, list) and references:
       return "#### References\n\nAvailable upon request\n"
   
   return f"#### References\n\n{str(references)}\n\n"
def format_resume(data):
   """
   Main function to format resume data into markdown.
   Handles unexpected data types safely.
   
   Args:
       data: Dictionary containing resume sections
       
   Returns:
       str: Complete formatted resume in markdown
   """
   if not data or not isinstance(data, dict):
       return "No resume data available."
   
   # Safely extract each section with fallback to empty string
   sections = [
       format_personal_info(data.get('personal_info')),
       format_summary(data.get('summary')),
       format_work_experience(data.get('work_experience')),
       format_education(data.get('education')),
       format_skills(data.get('skills')),
       format_certifications(data.get('certifications')),
       format_projects(data.get('projects')),
       format_languages(data.get('languages')),
       format_volunteer_experience(data.get('volunteer_experience')),
       format_interests(data.get('interests')),
       format_references(data.get('references'))
   ]
   
   # Filter out empty sections and join
   non_empty_sections = [section for section in sections if section.strip()]
   return "".join(non_empty_sections).strip()