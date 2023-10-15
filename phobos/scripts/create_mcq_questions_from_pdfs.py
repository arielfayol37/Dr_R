import re, os
import PyPDF2
from phobos.models import Question, MCQTextAnswer, QuestionChoices, Course, Assignment

def run():
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
        question_numbers = []
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
            question_numbers.append(match.group(1))
        return questions, question_numbers

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
    def extract_topics_from_pdf(pdf_path):
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()
        print(text)
        pattern = r"(\d+)\. ANS: [A-E] \nTOP: \d+[\+]? (\w+)"
        matches = re.findall(pattern, text)
        topics = {question: topic for question, topic in matches}
        return topics
    course, course_created = Course.objects.get_or_create(name='Question Bank')
    assignment, assignment_created = Assignment.objects.get_or_create(name='Question Bank 101', course=course)
    # In case you want to delete the questions in the question bank,
    # uncomment the following:
    # if not created:
        # assignment.questions.all().delete()
    for test_number in [1,2,3,4,5]:
        rpdf_path = f"PHYSICS QUESTION BANK/p101tb{test_number}q.pdf"
        pdf_path = os.path.abspath(rpdf_path)

        text = extract_text_from_pdf(pdf_path)
        parsed_questions, question_numbers  = parse_questions(text)

        rpdf_path = f"PHYSICS QUESTION BANK/p101tb{test_number}a.pdf"
        pdf_path = os.path.abspath(rpdf_path)
        answers_dict = extract_answers_from_pdf(pdf_path)
        # Adding the answer character to the parsed_questions dictionary
        for index, question_number in enumerate(question_numbers):
            parsed_questions[index]['answer_'+ str(question_number)] = answers_dict[str(question_number)]

        # Creating question objects
        for parsed_question in parsed_questions:
            for key, value in parsed_question.items():
                if key.startswith('question'):
                    q_number = key.split('_')[1]
                    new_question = Question(
                        number='--',
                        text = value,
                        #topic = topics_dict[q_number],  # Assigning the topic extracted from the answer key PDF
                        #sub_topic = sub_topic,
                        assignment = assignment
                    )
                    new_question.answer_type = QuestionChoices.MCQ_TEXT
                    new_question.save(save_settings=True)
                    new_question.mcq_settings.num_points = 5
                    new_question.mcq_settings.save()
                    answer_char = parsed_question[f'answer_{q_number}']
                    for option_char, option_value in parsed_question[f'options_{q_number}'].items():
                        new_answer = MCQTextAnswer.objects.create(question=new_question,content=option_value)
                        if option_char == answer_char:
                            new_answer.is_answer = True
                        new_answer.save()
                    

