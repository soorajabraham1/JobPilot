import tkinter as tk
from tkinter import ttk
from code.chatgpt import get_response_for_prompt
import os


def savefile(doc, folder_path, filename ):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    folder_path_letter = folder_path + filename
    doc.save(folder_path_letter)



def remove_signs(text):
    
        allowed_characters = set("abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ")
        return "".join([char for char in text if char in allowed_characters])


def options(file_location):
    myOptions={}
    subOptions = None
    with open(file_location, "r") as file:#
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            if not line:
                continue  # Skip empty lines
            if line.endswith(":"):
                subOptions = line[:-1]  # Extract brand name (remove colon)
                myOptions[subOptions] = []  # Create an empty list for colors
            else:
                myOptions[subOptions].append(line.strip("- "))  # Add color
    return myOptions


def process_job_description(job_description_entry):
    # Extract job description from the entry field
    job_description = job_description_entry.get("1.0", tk.END).strip()

    # Example prompt to extract information from a webpage or text
    prompt = """
    Extract the following details from the webpage/document as a dictionary. The keys should not change:
    - "Company name"
    - "Company city"
    - "Company country"
    - "Job role"
    - "Recruiter name" (if not mentioned, set it as "Recruiter"):
    - "Qualifications for the job"
    - "Job post language"
    """

    input_text = job_description  # Use the job description pasted by the user
    
    return get_response_for_prompt(prompt + input_text)

def myWindow():


    myOptions={}
    subOptions = None
    with open(r"textfiles\choices.txt", "r") as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            if not line:
                continue  # Skip empty lines
            if line.endswith(":"):
                subOptions = line[:-1]  # Extract brand name (remove colon)
                myOptions[subOptions] = []  # Create an empty list for colors
            else:
                myOptions[subOptions].append(line.strip("- "))  # Add color

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
    application_type_entry.set(data["name"])

    job_qualifications = tk.Label(frame,text="Job qualifications")
    job_qualifications.grid(row=5,column=0)
    job_qualifications_entry= tk.Text(frame, height=5, width=50)
    job_qualifications_entry.grid(row=5, column=1,  padx=10, pady=5, columnspan=2)


    job_role_label = tk.Label(frame, text="Job Role:")
    job_role_label.grid(row=6, column=0, sticky="w", pady=5)
    job_role_entry = tk.Entry(frame)
    job_role_entry.grid(row=6, column=1, padx=10, pady=5)

    job_first_para = tk.Label(frame,text="Job role first para")
    job_first_para.grid(row=7,column=0)
    job_first_para_entry= tk.Entry(frame)
    job_first_para_entry.grid(row=7, column=1, pady=10)


    recruiter_name_label = tk.Label(frame, text="Recruiter Name:")
    recruiter_name_label.grid(row=8, column=0, sticky="w", pady=5)
    recruiter_name_entry = tk.Entry(frame)
    recruiter_name_entry.grid(row=8, column=1, padx=10, pady=5)

    first_point = tk.Label(frame,text="First Point")
    first_point.grid(row=9,column=0)
    first_point_choices= myOptions['first_point']
    first_point_entry=ttk.Combobox(frame, values=first_point_choices)
    first_point_entry.grid(row=9, column=1)

    job_language_label = tk.Label(frame, text="Job Post Language:")
    job_language_label.grid(row=10, column=0, sticky="w", pady=5)
    job_language_entry = tk.Entry(frame)
    job_language_entry.grid(row=10, column=1, padx=10, pady=5)

    parse_button = tk.Button(frame, text="Parse", command=parse_job_description)
    parse_button.grid(row=11, column=0, pady=10)

    generate_button = tk.Button(frame, text="Generate Word", command=generate_letter)
    generate_button.grid(row=11, column=1, pady=10)

    status_label = tk.Label(frame, text="")
    status_label.grid(row=12, columnspan=2, pady=10)

    # Start the tkinter main loop
    window.mainloop()
