#python3 phobos:models.py
from django.db import models
from django.contrib.auth.models import User
#from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
import random
from Dr_R.settings import BERT_TOKENIZER, BERT_MODEL
import torch

def attention_pooling(hidden_states, attention_mask):
    # Apply attention mask to hidden states
    attention_mask_expanded = attention_mask.unsqueeze(-1).expand(hidden_states.size())
    masked_hidden_states = hidden_states * attention_mask_expanded
    
    # Calculate attention scores and apply softmax
    attention_scores = torch.nn.functional.softmax(masked_hidden_states, dim=1)
    
    # Weighted sum using attention scores
    pooled_output = (masked_hidden_states * attention_scores).sum(dim=1)
    return pooled_output

class DifficultyChoices(models.TextChoices):
    EASY = 'EASY', 'Easy'
    MEDIUM = 'MEDIUM', 'Medium'
    DIFFICULT = 'DIFFICULT', 'Difficult'

class SubjectChoices(models.TextChoices):    

    COMPUTER_SCIENCE = 'COMPUTER_SCIENCE', 'Computer Science'
    MATHS = 'MATHS', 'Maths'
    PHYSICS = 'PHYSICS', 'Physics'
    # TODO: Add more subject choices as needed.

class QuestionChoices(models.TextChoices):
    STRUCTURAL_EXPRESSION = 'STRUCTURAL_EXPRESSION', 'Structural Expression'
    STRUCTURAL_FLOAT = 'STRUCTURAL_FLOAT', 'Structural Float'
    STRUCTURAL_VARIABLE_FLOAT = 'STRUCTURAL_VARIABLE_FLOAT', 'Variable Float'
    STRUCTURAL_TEXT = 'STRUCTURAL_TEXT', 'Structural Text'
    STRUCTURAL_LATEX = 'STRUCTURAL_LATEX', 'Structural Latex'
    SURVEY = 'SURVEY', 'Survey'
    # The following MCQ variations are useless because a `Question` 
    # may have different types of MCQ answers. So at the end of the
    # day, we just check if it's an MCQ and check all the types.
    MCQ_EXPRESSION = 'MCQ_EXPRESSION', 'MCQ Expression'
    MCQ_FLOAT = 'MCQ_FLOAT', 'MCQ Float'
    MCQ_VARIABLE_FLOAT = 'MCQ_VARIABLE_FLOAT', 'MCQ Variable Float'
    MCQ_LATEX = 'MCQ_LATEX', 'MCQ Latex'
    MCQ_TEXT = 'MCQ_TEXT', 'MCQ Text'
    MCQ_IMAGE = 'MCQ_IMAGE', 'MCQ Image'
    

class AssignmentChoices(models.TextChoices):
    QUIZ = 'QUIZ', 'Quiz'
    HOMEWORK = 'HOMEWORK', 'Homework'
    PRACTICE_TEST = 'PRACTICE_TEST', 'Practice Test'

class Course(models.Model):
    """
    Course class to store course on the platform.
    
    There are no standalone courses .i.e Each course
    has an instructor or multiple instructors.

    The name doesn't have to be unique, given that
    different instructors/instutions may give a course
    with the same title.

    # TODO: the subject should not be a text field in the html template,
            given that there are already known subjects like 
            Computer Science, Maths, Or Physics. So Subject 
            should be drop-down list.
            Same applies to difficulty level.
    
    """

    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=400, default="No description")
    subject = models.CharField(max_length=100,
                                choices=SubjectChoices.choices,
                                default=SubjectChoices.PHYSICS)
    number_of_students = models.IntegerField(blank=True, null=True)
    difficulty_level = models.CharField(
        max_length=10,
        choices=DifficultyChoices.choices,
        default=DifficultyChoices.MEDIUM,
    )
    professors = models.ManyToManyField('Professor', related_name='courses')
    topics = models.ManyToManyField('Topic', related_name='courses')
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='phobos/images/course_covers', blank=True, null=True)

    def __str__(self):
        return f" Course {self.name}, difficulty level - {self.difficulty_level}"
    def delete(self, *args, **kwargs):
        # Delete the image file from storage
        if self.image:
            self.image.delete(save=False)
        super(Course, self).delete(*args, **kwargs)

class Professor(User):
    """
    Class to store professors on the platform.
    """
    department = models.CharField(max_length=50)

class Topic(models.Model):

    """
    A course may cover various topics. For example Mechanics and Fields in Physics, but should likely cover at most 3. 
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class SubTopic(models.Model):
    """
    A topic may be comprised of various topics.
    For example, Faraday's law is a subtopic of electromagnetism.
    """
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE, related_name='sub_topics')
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Assignment(models.Model):
    """
    Assignments in the form of quizzes/homeworks/practice_test will be created by
    professors and may be comprised of one or multiple questions. 
    """
    name = models.CharField(max_length=30)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="assignments")
    timestamp = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(blank=True, null=True)
    assigned_date = models.DateTimeField(blank=True, null=True)
    difficulty_level = models.CharField(
        max_length=10,
        choices=DifficultyChoices.choices,
        default=DifficultyChoices.MEDIUM,
    )
    category = models.CharField(max_length=25, choices=AssignmentChoices.choices,
                                 default = AssignmentChoices.HOMEWORK)
    def __str__(self):
        return f"Assigment {self.name} ranked {self.difficulty_level} for '{self.course.name.title()}'"

class Question(models.Model):
    """
    A question may be standalone or attributed to a `Assigment`. 
    
    A question may be comprised of a sub question like a, b, c, or d.
    (Optional: the sub questions themselves may have i, ii, iii, iv, like Twitter threads).

    A question may be a multiple choice question (and single-answer or multiple-answers type)
    OR an expression question with answers that may be numeric or algebraic expressions.

    A question may have randomized variables associated to it. Such that different students
    will have different variables and hence different answers. 

    The weight attribute is used to compute a student's grade for an Assignment.
    So all the questions in an assignment may have the same weight (uniform distribution),
    or different weights based on the instructor's input or automated (based on difficulty)
    
    # TODO: !Important 
        Though the category input from the instructor at the time of creation of the question
        will be optional, we may use embeddings to determine the similarity with other questions 
        and assign the same category as the closest question.

        The vector or matrix representation of the question should be computed at the time of
        creation or later(automatically - it may also be updated as more questions come in).
        That will be used for category assignment described above, and most importantly for
        the search engine.

    # Define choices for the topic 

    """
    number = models.CharField(blank=False, null=False, max_length=5)
    text = models.TextField(max_length= 2000, null=False, blank=False)
    assignment = models.ForeignKey(Assignment, null=True, on_delete=models.CASCADE, \
                                   related_name="questions")
    category = models.CharField(max_length=50, null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    sub_topic = models.ForeignKey(SubTopic, on_delete=models.SET_NULL, null=True, blank=True)
    num_points = models.IntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(15)]) # Add lower and upper bound.
    parent_question = models.ForeignKey('self', on_delete=models.CASCADE, null=True, \
                                        blank=True, related_name='sub_questions')
    timestamp = models.DateTimeField(auto_now_add=True)
    difficulty_level = models.CharField(
        max_length=10,
        choices=DifficultyChoices.choices,
        default=DifficultyChoices.MEDIUM,
    )
    answer_type = models.CharField(
        max_length = 30,
        choices = QuestionChoices.choices,
        default = QuestionChoices.STRUCTURAL_TEXT
    )
    max_num_attempts = models.IntegerField(default=5)
    answer = models.CharField(max_length=1000, null=True, blank=True) # TODO: delete this attribute.
    deduct_per_attempt = models.FloatField(default=0.05, blank=True, null=True)
    margin_error = models.FloatField(default=0.03, blank=True, null=True)
    due_date = models.DateTimeField(null=True, blank=True)
    embedding = models.JSONField(null=True, blank=True)  # Field to store encoded representation for search
    

    def default_due_date(self):
        if self.assignment:
            return self.assignment.due_date
        return None

    def save(self, *args, **kwargs):
        if self.due_date is None:
            self.due_date = self.default_due_date()

        if not self.embedding:
            question_tokens = BERT_TOKENIZER.encode(self.text, add_special_tokens=True)
            with torch.no_grad():
                question_tensor = torch.tensor([question_tokens])
                question_attention_mask = (question_tensor != 0).float()  # Create attention mask
                question_encoded_output = BERT_MODEL(question_tensor, attention_mask=question_attention_mask)[0]

            # Apply attention-based pooling to question encoded output
            question_encoded_output_pooled = attention_pooling(question_encoded_output, question_attention_mask)

            # Save the encoded output to the question object
            self.embedding = question_encoded_output_pooled.tolist()

        super(Question, self).save(*args, **kwargs)


    def __str__(self):
        return f"Question {self.number} ranked {self.difficulty_level} for {self.assignment}"
    


class QuestionImage(models.Model):
    """
    Class for images associated with a particular question.
    For example, for more description or for a multiple choice question where the options
    are images.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='phobos/images/question_images/', blank=True, null=True)
    label = models.CharField(max_length=70, blank=True, null=True)

    def __str__(self):
        return f"{self.label} for {self.question}"
    
    def delete(self, *args, **kwargs):
        # Delete the image file from storage
        if self.image:
            self.image.delete(save=False)
        super(QuestionImage, self).delete(*args, **kwargs)

class Hint(models.Model):
    """
    Each question/subquestion may have hints in the form of text or urls to help.
    """
    question = models.ForeignKey(Question, related_name='hints', on_delete=models.CASCADE)
    text = models.TextField(blank=False, null=False) # Professor must include text(description)

    def __str__(self):
        return f"Hint {self.id} for {self.question}"
    
class AnswerBase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField(blank=False, null=False)
    answer_unit = models.CharField(max_length=50, blank=True, null=True) # Optional field for the units of the answer
    class Meta:
        abstract = True

    def __str__(self):
        return f"Answer for {self.question}: {self.content}"
        
class FloatAnswer(AnswerBase):
    """
    Answer to a `structural Question` may be an algebraic expression, a vector, or a float.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="float_answers")
    content = models.FloatField(blank=False, null=False)

    def __str__(self):
            
        return f"Float Answer for {self.question}: {self.content}"
    
class VariableFloatAnswer(AnswerBase):
    """
    Answer to a `structural Question` or `MCQ Question` may be a variable float. 
    E.g answer = F/m, where F and m are going to have multiple different values assigned
    to different users.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='variable_float_answers')
    content = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f"Variable Float answer for {self.question}: {self.content}"
        
            
class ExpressionAnswer(AnswerBase):
    """
    An expression for a `structural Question` may just be interpreted as text. The math.js library
    will parse the expression given by the teacher and the resulting text will be stored.
    When a user will input an answer, it will be compared to that text.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="expression_answers")
    content = models.CharField(max_length=200) 
    
    def __str__(self):
        
        return f"Expression Answer for {self.question}: {self.content}"

class LatexAnswer(AnswerBase):
    """
    An answer may a latex string that will later be rendered in the JavaScript.
    For now, this is only used for MCQ `Questions`.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='latex_answers')
    content = models.CharField(max_length=400)

    def __str__(self):

        return f"Latex Answer for {self.question}: {self.content}"
    
class TextAnswer(AnswerBase):
    """
    Probably less common, but a `Question` may have a text answer.
    Will implement semantic validation for text answers using a transformer later.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='text_answers')
    content = models.CharField(max_length=1000)

    def __str__(self):
        return f"Text Answer for {self.question}: {self.content}"
    
class MCQAnswerBase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField(blank=False, null=False)
    is_answer = models.BooleanField(default=False)
    class Meta:
        abstract = True

    def __str__(self):
        return f"MCQ Answer for {self.question}: {self.content}"

class MCQFloatAnswer(MCQAnswerBase):
    """
    Float Answer to a `MCQ Question`.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="mcq_float_answers")
    content = models.FloatField(blank=False, null=False)
    def __str__(self):
        if self.is_answer:
            return f"Correct MCQ Float Answer for {self.question}: {self.content}"
        else:
            return f"Incorrect MCQ Float Answer for {self.question}: {self.content}" 
        
class MCQVariableFloatAnswer(MCQAnswerBase):
    """
    Answer to a `structural Question` or `MCQ Question` may be a variable float. 
    E.g answer = F/m, where F and m are going to have multiple different values assigned
    to different users.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='mcq_variable_float_answers')
    content = models.CharField(max_length=100, null=False, blank=False)
    def __str__(self):
        if self.is_answer:
            return f"Correct MCQ Variable Float Answer for {self.question}: {self.content}"
        else:
            return f"Incorrect MCQ Variable Float Answer for {self.question}: {self.content}" 
        
            
class MCQExpressionAnswer(MCQAnswerBase):
    """
    Expression answer for a `MCQ Question`.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="mcq_expression_answers")
    content = models.CharField(max_length=200) 
    def __str__(self):
        if self.is_answer:
            return f"Correct MCQ Expression Answer for {self.question}: {self.content}"
        else:
            return f"Incorrect MCQ Expression Answer for {self.question}: {self.content}" 

class MCQLatexAnswer(MCQAnswerBase):
    """
    Latex answer for `MCQ Question`.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='mcq_latex_answers')
    content = models.CharField(max_length=400)

    def __str__(self):
        if self.is_answer:
            return f"Correct MCQ Latex Answer for {self.question}: {self.content}"
        else:
            return f"Incorrect MCQ Latex Answer for {self.question}: {self.content}" 
    
class MCQTextAnswer(MCQAnswerBase):
    """
    Text answer for `MCQ Question`.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='mcq_text_answers')
    content = models.CharField(max_length=400)

    def __str__(self):
        if self.is_answer:
            return f"Correct MCQ Text Answer for {self.question}: {self.content}"
        else:
            return f"Incorrect MCQ Text Answer for {self.question}: {self.content}"    
    
class MCQImageAnswer(MCQAnswerBase):
    """
    An answer to an `MCQ Question` may simply be an image.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='mcq_image_answers')
    image = models.ImageField(upload_to='phobos/images/question_images/', \
                              blank=True, null=True)  
    label = models.CharField(max_length=70, blank=True, null=True) 
    content = models.CharField(max_length=1, blank=True, null=True)

    def __str__(self):
        return f"Image answer for {self.question} with url {self.image.url}" 
    def delete(self, *args, **kwargs):
        # Delete the image file from storage
        if self.image:
            self.image.delete(save=False)
        super(MCQImageAnswer, self).delete(*args, **kwargs)
class Variable(models.Model):
    """
    A `Question` may have variables associated to it. 
    A variable will have symbol representing it. Will be one character most of the times
    but some may be subscripted. E.g epislon_zero may be represented like this 'e_0'

    For example, question with pk 12 may have 5 variables associated to it.
    Those variable will each have maybe 4 instances and each time a student
    opens a `Question` for the first time, one of the instances of each variable
    is going to assigned to `QuestionStudent` object which relates the `Question`
    and the `Student`.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='variables')
    symbol = models.CharField(max_length=3, blank=False, null=False)
    instances_created = models.BooleanField(default=False)
    is_integer = models.BooleanField(default=False)

    def __str__(self):
        return f"Variable `{self.symbol}` for question {self.question}"
    def create_instances(self, num = 5, is_int=False):
        """
        Creates num number of random variable instances.
        """
        intervals = self.intervals.all()
        if intervals:
            for _ in range(num):
                bounds = random.choice(intervals)
                lower_bound = bounds.lower_bound
                upper_bound = bounds.upper_bound
                random_float = random.uniform(lower_bound, upper_bound)
                if is_int:
                    random_float = float(int(random_float))
                vi = VariableInstance.objects.create(variable=self, value=random_float)
                vi.save()
            self.instances_created = True
        # TODO: Handle case when intervals are not created.
        else:
            raise Exception("Intervals were not created before create_instances() was called.")
    def get_instance(self):
        if not self.instances_created:
            self.create_instances()
        return random.choice(self.instances.all())
    
class VariableInstance(models.Model):
    """
    Instance of `Variable`
    """
    variable = models.ForeignKey(Variable, on_delete=models.CASCADE, related_name='instances')
    value = models.FloatField(null=False, blank=False)
class VariableInterval(models.Model):
    """
    A `Variable` may have multiple intervals in its domain.
    For example, variable x domain may be [1,5] U [9, 17]
    """
    variable = models.ForeignKey(Variable, on_delete=models.CASCADE,related_name='intervals')
    lower_bound = models.FloatField(default=-999,blank=False, null=False)
    upper_bound = models.FloatField(default=999, blank=False, null=False)

    def __str__(self):
        return f"Interval {self.lower_bound} - {self.upper_bound} for {self.variable}"

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='vector_answers')
    content = models.FloatField(blank=False, null=False)  # Store the vector as an array of floats

    def __str__(self):
        return f"Correct Vector Answer for {self.question}: {self.content}"

class EnrollmentCode(models.Model):

    course= models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollment_code")
    code = models.IntegerField(default=0000)
    creation_date = models.DateField(auto_now_add=True)
    expiring_date = models.DateField()
