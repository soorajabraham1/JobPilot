import tkinter as tk
from tkinter import ttk
import docxtpl
from googletrans import Translator
import os
import json
from code.widget import options 
from code.chatgpt import myopenai
from code.widget import remove_signs
from code.widget import process_job_description
from code.widget import savefile
from code.rag import generate
from datetime import datetime

translator = Translator()
month_name = datetime.now().strftime("%B")
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
myOptions= options(r"textfiles\choices.txt")

def parse_job_description():
    result = json.loads(process_job_description(job_description_entry))
    print(result)
    
    company_name = result.get("Company name")
    company_location = result.get("Company city")
    company_country =result.get("Company country")
    job_role = result.get("Job role")
    recruiter_name = result.get("Recruiter name")
    qualifications = result.get("Qualifications for the job")
    job_language = result.get("Job post language")
    print(qualifications)
    
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
    job_disc_cv = job_qualifications_entry.get("1.0", tk.END)
    job_language=job_language_entry.get()
    job_role_filtered = remove_signs(job_role)
    first_para="write a 3 sentence starting parahgraph for my coverletter showing enthusiasm in the role"+ job_role+ "at "+ company_name+ ". write in" + company_language + "language. Add things related to company to show more enthusiasm. Don't add salutation. Write in exactly 7 words. I am adding some information about the specific department in the company: "
    first_para_sentence = myopenai(first_para)

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
    savefile(cv_doc, folder_path, "/CV.docx" ) # Convert to Path object
    savefile(doc1, parent_folder,"/emailtemplate.docx")


def open_settings():
    global settings_window
    settings_window = tk.Toplevel(window)  # Create a new top-level window
    settings_window.title("Settings")
    settings_window.geometry("300x200")

    def save_api_key():
        api_key = api_key_entry.get().strip()
        name = name_entry.get().strip()

        try:
            with open("textfiles/config.txt", "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        if api_key:
            data["api_kuttan"] = api_key
        if name:
            data["name"] = name

        with open("textfiles/config.txt", "w") as file:
            json.dump(data, file)

    api_key_label = tk.Label(settings_window, text="Enter API Key:")
    api_key_label.pack(pady=5)

    api_key_entry = tk.Entry(settings_window, width=30)
    api_key_entry.pack(pady=5)

    name_label = tk.Label(settings_window, text="Enter Name:")
    name_label.pack(pady=5)

    name_entry = tk.Entry(settings_window, width=30)
    name_entry.pack(pady=5)

    save_button = tk.Button(settings_window, text="Save", command=save_api_key)
    save_button.pack(pady=5)

    back_button = tk.Button(settings_window, text="Back", command=settings_window.destroy)
    back_button.pack(pady=20)

# Create tkinter window
window = tk.Tk()
window.title("JobPilot")

# Create and place widgets
frame = tk.Frame(window, padx=20, pady=20)
frame.pack()
settings_button = tk.Button(frame, text="Settings", command=open_settings)
settings_button.grid(row=13, columnspan=2, pady=10)

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
