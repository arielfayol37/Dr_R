import re, os
import PyPDF2
os.chdir(r'C:\Users\Noella\Downloads')

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    return text
def parse_questions(text):
    # Regex pattern to capture questions and options
    pattern = r"____(\d+)\. (.*?)(?=____\d+\.|$)"
    questions = []
    for match in re.finditer(pattern, text):
        question_text = match.group(2)
        # Split the question text by options
        parts = re.split(r"([A-E]\.)", question_text)
        question = parts[0].strip()
        options = {parts[i][0]: parts[i+1].strip() for i in range(1, len(parts)-1, 2)}

        questions.append({
            f"question_{match.group(1)}": question,
            f"options_{match.group(1)}": options
        })
    return questions
def extract_answers_from_pdf(pdf_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        # Initialize PDF reader
        reader = PyPDF2.PdfReader(file)
        
        # Extract text from the PDF
        text = ""
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()

    return extract_answers(text)

def extract_answers(text):
    # Regex pattern to capture question number and its answer
    pattern = r"(\d+)\. ANS: ([A-E])"
    
    # Find all matches using the regex pattern
    matches = re.findall(pattern, text)
    
    # Convert the matches into a dictionary
    answers = {question: answer for question, answer in matches}
    
    return answers

#pdf_path = r"C:\Users\Noella\Downloads\PHYSICS QUESTION BANK\p101tb1q.pdf"  #Replace with your PDF file path
pdf_path = r"C:\Users\User\AppData\Local\Programs\Python\Python310\Scripts\env_site\Scripts\Dr_R2\PHYSICS QUESTION BANK\p101tb1q.pdf"
text = extract_text_from_pdf(pdf_path)
parsed_questions = parse_questions(text)
print(parsed_questions[0:10])




#pdf_path = r"C:\Users\Noella\Downloads\PHYSICS QUESTION BANK\p101tb1a.pdf" 
pdf_path = r"C:\Users\User\AppData\Local\Programs\Python\Python310\Scripts\env_site\Scripts\Dr_R2\PHYSICS QUESTION BANK\p101tb1a.pdf"
answers_dict = extract_answers_from_pdf(pdf_path)
print(answers_dict)
