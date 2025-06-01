import tkinter as tk
from tkinter import ttk
import docxtpl
from googletrans import Translator
import os
import json
from openai import OpenAI
from scripts.widget import options, load_from_txt
from scripts.widget import myopenai
from scripts.widget import remove_signs
from scripts.widget import process_job_description
from scripts.widget import savefile
from scripts.rag import generate_cv_summary
from datetime import datetime
import sys
config_path=r"textfiles\config.txt"
resume_summary_path = r'textfiles\resume.txt'
german_cover_letter=r"mydocs\Cover_letter_template_germanopenai.docx"
english_cover_letter=r"mydocs\Cover_letter_template.docx"
german_cv=r"mydocs\CV_German.docx"
english_cv=r"mydocs\CV_English.docx"
email_template=r"mydocs\emailtemplate.docx"
myOptions= options(r"textfiles\choices.txt")
config=json.loads(load_from_txt(config_path))
client = OpenAI(api_key=config["api_key"])

def get_output_folder():
    """Get the folder where the EXE or PY file is located."""
    if getattr(sys, 'frozen', False):
        # If running as a bundled exe
        return os.path.dirname(sys.executable)
    else:
        # If running as a normal .py script
        return os.path.dirname(os.path.abspath(__file__))

translator = Translator()
month_name = datetime.now().strftime("%B")
parent_folder = get_output_folder()


def parse_job_description():
    result = json.loads(process_job_description(client,job_description_entry))
    
    company_name = result.get("Company name")
    company_location = result.get("Company city")
    company_country =result.get("Company country")
    job_role = result.get("Job role")
    recruiter_name = result.get("Recruiter name")
    qualifications = result.get("Qualifications for the job")
    job_language = result.get("Job post language")

    # Display extracted info in the entry fields
    company_name_entry.delete(0, tk.END)
    company_name_entry.insert(0, company_name)
    company_location_entry.delete(0, tk.END)
    company_location_entry.insert(0, company_location)
    country_entry.delete(0, tk.END)
    country_entry.insert(0, company_country)
    job_role_entry.delete("1.0", tk.END)
    job_role_entry.insert("1.0", job_role)
    job_first_para_entry.delete("1.0", tk.END)
    job_first_para_entry.insert("1.0", job_role)
    recruiter_name_entry.delete(0, tk.END)
    recruiter_name_entry.insert(0, recruiter_name)
    job_qualifications_entry.delete("1.0", tk.END)
    job_qualifications_entry.insert("1.0", qualifications)
    job_language_entry.delete(0, tk.END)
    job_language_entry.insert(0, job_language)


def generate_letter():
    company_language= job_language_entry.get()
    company_name= company_name_entry.get()
    company_location= company_location_entry.get()
    country= country_entry.get()
    application_type= application_type_entry.get()
    job_role= job_role_entry.get("1.0", tk.END)
    recruiter_name= recruiter_name_entry.get()
    today_date= datetime.today().strftime("%d %B %Y")
    first_point=first_point_entry.get()
    job_first_para=job_first_para_entry.get("1.0", tk.END)
    company_name_short=company_name_entry.get()
    #abt_cmpny=abt_cmpny_entry.get()
    job_disc_cv = job_qualifications_entry.get("1.0", tk.END)
    job_language=job_language_entry.get()
    job_role_filtered = remove_signs(job_role)
    first_para=("write a 3 sentence starting paragraph for my cover letter showing enthusiasm in the role"+ job_role+
                "at "+ company_name+ ". write in" + company_language + "language. Add things related to company to show"
                " more enthusiasm. Don't add salutation. Write in exactly 7 words. I am adding some information about"
                                                                       " the specific department in the company: ")
    first_para_sentence = myopenai(client,first_para)
    summary_sentence = generate_cv_summary(client,resume_summary_path, job_first_para, job_disc_cv, job_language)
    
    if company_language=='German':
        cover_letter_doc = docxtpl.DocxTemplate(german_cover_letter) if config["coverletter"] else None
        cv_doc = docxtpl.DocxTemplate(german_cv) if config["resume"] else None
    elif company_language=='English':
        cover_letter_doc = docxtpl.DocxTemplate(english_cover_letter) if config["coverletter"] else None
        cv_doc = docxtpl.DocxTemplate(english_cv) if config["resume"] else None
        
    email_doc = docxtpl.DocxTemplate(email_template) if config["email"] else None
    
    if application_type== 'Initiative application':
        para=myOptions['Initiative application'][0]
        
        folder_path = fr"{parent_folder}\{month_name}\Initiative\{company_name}\{job_role_filtered}"

    else:
        para=myOptions['Application'][0]
        folder_path = fr"{parent_folder}\{month_name}\{company_name}\{job_role_filtered}"
    if 'Embedded' in first_point and company_language=='German':
        embedded_devices=myOptions['embedded_devices_german'][0]
    elif 'Embedded' in first_point and company_language=='English':
        embedded_devices=myOptions['embedded_devices_english'][0]
    else:
        embedded_devices=''

    if company_language=='German':
        first_point = translator.translate(first_point, dest='de')  # 'de' stands for German
    
    

    if cover_letter_doc:
        print("cover_letter created")
        cover_letter_doc.render({ 'company_name' : company_name,
                'company_location':company_location,
                'country':country,
                'date':today_date,
                'application_type': application_type,
                'job_role':job_role.replace('\n', ''),
                'recruiter_name':recruiter_name,
                'first_point' :first_point,
                'embedded_devices' : embedded_devices,
                'first_para_sentence' : first_para_sentence,
                'job_first_para' : job_first_para,
                'company_name_short': company_name_short})
    if email_doc:
        print("email created")
        email_doc.render({ 'company_name' : company_name,
                    'date':today_date,
                    'application_type': application_type,
                    'job_role':job_role.replace('\n', ''),
                    #'application_medium': application_medium,
                    'recruiter_name':recruiter_name,
                    'para': para
                    })
    if cv_doc:
        print("resume created")
        cv_doc.render({'summary_sentence_english': summary_sentence,
                    'summary_sentence_german': summary_sentence})
    
    savefile(cover_letter_doc, folder_path, "/Cover_letter.docx") if config["coverletter"] else None
    savefile(cv_doc, folder_path, "/CV.docx" ) if config["resume"] else None
    savefile(email_doc, parent_folder,"/email.docx")if config["email"] else None


    
# Create tkinter window
window = tk.Tk()
window.title("Jobpilot")

# Create and place widgets
frame = tk.Frame(window, padx=20, pady=20)
frame.pack()



job_description_label = tk.Label(frame, text="Job Description:")
job_description_label.grid(row=0, column=0, sticky="w", pady=5)
job_description_entry = tk.Text(frame, height=5, width=50)
job_description_entry.grid(row=0, column=1, padx=10, pady=5, columnspan=2)

company_name_label = tk.Label(frame, text="Company Name:")
company_name_label.grid(row=1, column=0, sticky="w", pady=5)
company_name_entry = tk.Entry(frame)
company_name_entry.grid(row=1, column=1, padx=10, pady=5)

company_location_label = tk.Label(frame, text="Company Location:")
company_location_label.grid(row=2, column=0, sticky="w", pady=5)
company_location_entry = tk.Entry(frame)
company_location_entry.grid(row=2, column=1, padx=10, pady=5)

country = tk.Label(frame,text="Country")
country.grid(row=3,column=0)
country_entry = tk.Entry(frame)
country_entry.grid(row=3, column=1, pady=10)

application_type = tk.Label(frame,text="Application type")
application_type.grid(row=4,column=0)
choices= myOptions['application_type']
application_type_entry=ttk.Combobox(frame, values=choices)
application_type_entry.grid(row=4, column=1, pady=10)
application_type_entry.set("Application")

job_qualifications = tk.Label(frame,text="Job qualifications")
job_qualifications.grid(row=5,column=0)
job_qualifications_entry= tk.Text(frame, height=5, width=50)
job_qualifications_entry.grid(row=5, column=1,  padx=10, pady=5, columnspan=2)


job_role_label = tk.Label(frame, text="Job Role")
job_role_label.grid(row=6, column=0, sticky="w", pady=5)
job_role_entry = tk.Text(frame, height=1, width=30)#tk.Entry(frame)
job_role_entry.grid(row=6, column=1, padx=10, pady=5)

job_first_para = tk.Label(frame,text="Job role first para")
job_first_para.grid(row=7,column=0)
job_first_para_entry= tk.Text(frame, height=1, width=30)
job_first_para_entry.grid(row=7, column=1, padx=10, pady=5)


recruiter_name_label = tk.Label(frame, text="Recruiter Name:")
recruiter_name_label.grid(row=8, column=0, sticky="w", pady=5)
recruiter_name= myOptions['Recruiter']
recruiter_name_entry = ttk.Combobox(frame, values=recruiter_name)
recruiter_name_entry.grid(row=8, column=1, padx=10, pady=5)


first_point = tk.Label(frame,text="First Point")
first_point.grid(row=9,column=0)
first_point_choices= myOptions['first_point']
first_point_entry=ttk.Combobox(frame, values=first_point_choices)
first_point_entry.grid(row=9, column=1)

job_language_label = tk.Label(frame, text="Job Post Language:")
job_language_label.grid(row=10, column=0, sticky="w", pady=5)
language_choices= myOptions['company_language']
job_language_entry = ttk.Combobox(frame, values=language_choices)
job_language_entry.grid(row=10, column=1, padx=10, pady=5)

parse_button = tk.Button(frame, text="Parse", command=parse_job_description)
parse_button.grid(row=11, column=0, pady=10)

generate_button = tk.Button(frame, text="Generate Word", command=generate_letter)
generate_button.grid(row=11, column=1, pady=10)

status_label = tk.Label(frame, text="")
status_label.grid(row=13, columnspan=2, pady=10)

# Things to create label and buttons
things_to_create_label = tk.Label(frame, text="Things to create:")
things_to_create_label.grid(row=12, column=0, sticky="w", pady=5)

# Functions to sync changes back to config
def update_config_from_ui():
    config['resume'] = cover_letter_var.get()
    config['coverletter'] = cv_var.get()
    config['email'] = email_var.get()
    print("Updated config:", config)

# Variables for checkbuttons (initialized from config)
cover_letter_var = tk.BooleanVar(value=config['coverletter'])
cv_var = tk.BooleanVar(value=config['resume'])
email_var = tk.BooleanVar(value=config['email'])

# Checkbuttons in a row
cover_letter_cb = tk.Checkbutton(frame, text="Cover Letter", variable=cover_letter_var,command=update_config_from_ui)
cover_letter_cb.grid(row=12, column=0, sticky="w", padx=5, pady=5)

cv_cb = tk.Checkbutton(frame, text="CV", variable=cv_var,command=update_config_from_ui)
cv_cb.grid(row=12, column=1, sticky="w", padx=5, pady=5)

email_cb = tk.Checkbutton(frame, text="Email", variable=email_var,command=update_config_from_ui)
email_cb.grid(row=12, column=2, sticky="w", padx=5, pady=5)
window.mainloop()
