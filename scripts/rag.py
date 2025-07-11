import numpy as np
import faiss

def generate_cv_summary(client,resume_summary_path, job_role, query,job_language):

    # Open the file in read mode
    with open(resume_summary_path, 'r') as file:
        # Read the contents of the file
        file_contents = file.read()
    text = file_contents
    

    # Split document into chunks
    chunk_size = 100
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    # Create embeddings for each text chunk
    def get_text_embedding(input):
        response = client.embeddings.create(
        input= input,
        model="text-embedding-3-small"
        )
        return response.data[0].embedding


    text_embeddings = np.array([get_text_embedding(chunk) for chunk in chunks])

    # Load into a vector database
    d = text_embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(text_embeddings)

    # Create embeddings for a question
    question = query
    question_embeddings = np.array([get_text_embedding(question)])

    # Retrieve similar chunks from the vector database
    D, I = index.search(question_embeddings, k=10)
    retrieved_chunk = [chunks[i] for i in I[0]]

    # Combine context and question in a prompt and generate response

    prompt = f"""
    Given the following CV and job description, generate a personalized and cohesive summary in {job_language} 
    that retains the same idea as the CV and incorporates relevant keywords from the job description. 
    Ensure the summary is specific, avoids generic statements, starts with 
    "Enthusiastic {job_role} with so andd so degree in ...,, and x years of experience in (if experience is there)  ...", and is strictly between 45-50 words.
    CV:
    {retrieved_chunk}

    Job Description:
    {question}

    Personalized Summary  (45-50 words):
    """

    response = client.chat.completions.create(
    model="gpt-3.5-turbo-16k",
    messages=[ {"role": "user", "content": prompt}])

    return response.choices[0].message.content

