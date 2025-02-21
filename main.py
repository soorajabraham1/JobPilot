import tkinter as tk
from tkinter import ttk
from openai import OpenAI
from docx import Document
import docxtpl
from datetime import datetime
from googletrans import Translator
import os
from pathlib import Path
from code.widget import options 
from code.widget import myopenai
from code.widget import remove_signs
from code.widget import process_job_description
from code.widget import savefile
from code.rag import generate
from datetime import datetime

translator = Translator()
month_name = datetime.now().strftime("%B")

myOptions= options(r"textfiles\choices.txt")

def parse_job_description():
    lines= process_job_description(job_description_entry)
    
    company_name = ""
    company_location = ""
    company_country = ""
    job_role = ""
    recruiter_name = ""
    qualifications = ""
    job_language = ""

    for line in lines:
        if "Company name:" in line:
            company_name = line.split(":")[1].strip()
        elif "Company city:" in line:
            company_location = line.split(":")[1].strip()
        elif "Company country:" in line:
            company_country = line.split(":")[1].strip()
        elif "Job role:" in line:
            job_role = line.split(":")[1].strip()
        elif "Recruiter name:" in line:
            recruiter_name = line.split(":")[1].strip()
        elif "Requirements for the job:" in line:
            qualifications = line.split(":")[1].strip()
        elif "The job post language:" in line:
            job_language = line.split(":")[1].strip()
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
    first_para="write a 3 sentence starting parahgraph for my coverletter showing enthusiasm in the role"+ job_role+ "at "+ company_name+ ". write in" + company_language + "language. Add things related to company to show more enthusiasm. Don't add salutation. Write in exactly 7 words. I am adding some information about the specific department in the company: "
    first_para_sentence = myopenai(first_para)

    #summary_sentence = myopenai(summary_eng)
    summary_sentence = generate("path", job_first_para, job_disc_cv, job_language)
    
    if company_language=='German':
        doc = docxtpl.DocxTemplate(r"mydocs\Cover_letter_template_germanopenai.docx")
        cv_doc = docxtpl.DocxTemplate(r"mydocs\CV_German.docx")
    elif company_language=='English':
        doc = docxtpl.DocxTemplate(r"mydocs\Cover_letter_templateopenai.docx")
        cv_doc = docxtpl.DocxTemplate(r"mydocs\CV_English.docx")
        
    doc1 = docxtpl.DocxTemplate(r"mydocs\emailtemplate.docx")
    
    if application_type== 'Initiative application':
        para=myOptions['Initiative application'][0]
        
        folder_path = fr"E:\{month_name}\Initiative\{company_name}\{job_role_filtered}"

    else:
        para=myOptions['Application'][0]
        folder_path = fr"E:\{month_name}\{company_name}\{job_role_filtered}"
    if 'Embedded' in first_point and company_language=='German':
        embedded_devices=myOptions['embedded_devices_german'][0]
    elif 'Embedded' in first_point and company_language=='English':
        embedded_devices=myOptions['embedded_devices_english'][0]
    else:
        embedded_devices=''

    if company_language=='German':
        first_point = translator.translate(first_point, dest='de')  # 'de' stands for German
    
    

    doc.render({ 'company_name' : company_name,
                'company_location':company_location,
                'country':country,
                'date':today_date,
                'application_type': application_type,
                'job_role':job_role,
                'recruiter_name':recruiter_name,
                'first_point' :first_point,
                'embedded_devices' : embedded_devices,
                'first_para_sentence' : first_para_sentence,
                'job_first_para' : job_first_para,
                'company_name_short': company_name_short})
    
    doc1.render({ 'company_name' : company_name,
                'date':today_date,
                'application_type': application_type,
                'job_role':job_role,
                #'application_medium': application_medium,
                'recruiter_name':recruiter_name,
                'para': para
                })
    cv_doc.render({'summary_sentence_english': summary_sentence,
                   'summary_sentence_german': summary_sentence})
    
    savefile(doc, folder_path, "/Cover_letter.docx")
    
    savefile(cv_doc, folder_path, "/CV.docx" )
    folder_path = Path(folder_path)  # Convert to Path object
    parent_folder = folder_path.parent.parent
    savefile(doc1, fr"{parent_folder}","\emailtemplate.docx")
    
# Create tkinter window
window = tk.Tk()
window.title("Job Description Parser and Word Generator")

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
job_language_entry = ttk.Combobox(frame, values=choices)
job_language_entry.grid(row=10, column=1, padx=10, pady=5)

parse_button = tk.Button(frame, text="Parse", command=parse_job_description)
parse_button.grid(row=11, column=0, pady=10)

generate_button = tk.Button(frame, text="Generate Word", command=generate_letter)
generate_button.grid(row=11, column=1, pady=10)

status_label = tk.Label(frame, text="")
status_label.grid(row=12, columnspan=2, pady=10)

# Start the tkinter main loop
window.mainloop()
