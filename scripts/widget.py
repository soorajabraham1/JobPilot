import tkinter as tk
import os

def savefile(doc, folder_path, filename ):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    folder_path_letter = folder_path + filename
    doc.save(folder_path_letter)

def myopenai(client,query):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo-16k",
    messages=[{"role": "user", "content": query}]
    )
    return completion.choices[0].message.content

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

def load_from_txt(file_path):
    with open(file_path, "r") as file:
        return file.read()

def process_job_description(client,job_description_entry):
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

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[{"role": "user", "content": prompt + input_text}]
    )

    # Extract the generated content from the response
    extracted_info = response.choices[0].message.content
    
    return extracted_info

