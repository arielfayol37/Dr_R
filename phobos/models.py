#python3 phobos:models.py
from django.db import models
from django.contrib.auth.models import User
#from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
import random
from .utils import *
class DifficultyChoices(models.TextChoices):
    EASY = 'EASY', 'Easy'
    MEDIUM = 'MEDIUM', 'Medium'
    DIFFICULT = 'DIFFICULT', 'Difficult'

class SubjectChoices(models.TextChoices):    
    # COMPUTER_SCIENCE = 'COMPUTER_SCIENCE', 'Computer Science'
    # MATHS = 'MATHS', 'Maths'
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
    
    MATCHING_PAIRS = 'MATCHING_PAIRS', 'Matching Pairs'

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
        return f"{self.name}"
    def delete(self, *args, **kwargs):
        # Delete the image file from storage
        if self.image:
            self.image.delete(save=False)
        super(Course, self).delete(*args, **kwargs)

class CourseInfo(models.Model):
    """
    Class to store extra information about a course. 
    these info is provided by professor and viewed by students.
    """
    course= models.OneToOneField(Course, on_delete=models.CASCADE, related_name='course_info')
    course_skills= models.CharField(max_length=2000, default="")
    about_course= models.CharField(max_length=2000, default="")
    course_plan=models.CharField(max_length=2000, default="")
    course_instructors = models.CharField(max_length=2000, default="")
    instructors_image= models.ImageField(upload_to='phobos/images/professors', blank=True, null=True)
    notice = models.CharField(max_length=2000, default="")
    
    def __str__(self):
        return f'Course Info for {self.course}'
class Professor(User):
    """
    Class to store professors on the platform.
    """
    department = models.CharField(max_length=50)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Subject(models.Model):
    """
    Subject
    """
    name = models.CharField(max_length=50, blank=False, null=False, default='PHYSICS')
    def __str__(self):
        return self.name
class Topic(models.Model):

    """
    A course may cover various topics. For example Mechanics and Fields in Physics, but should likely cover at most 3. 
    """
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
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
    
class Unit(models.Model):
    """
    A subtopic may have many units under it. For example, the subtopic Collision, under the topic 
    Mechanics, has units 1D collision, 2D collision, conservation of linear momentum, etc. 
    """
    subtopic = models.ForeignKey(SubTopic, on_delete=models.CASCADE, related_name='units')
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
    is_assigned = models.BooleanField(default=False)
    grading_scheme = models.ForeignKey('GradingScheme', on_delete=models.SET_NULL, related_name='assignments', null=True, blank=True)
    
    def __str__(self):
        return f"Assigment {self.name} ranked {self.difficulty_level} for '{self.course.name.title()}'"
    
    def save(self, *args, **kwargs):
        if not self.grading_scheme:
            self.grading_scheme, created = GradingScheme.objects.get_or_create(name="Default", course=self.course)
            self.grading_scheme.save()
        super(Assignment, self).save(*args, **kwargs)


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
    """
    # parent question must have an integer as number because that's what is used for ordering.
    number = models.CharField(blank=False, null=False, max_length=5)
    text = models.TextField(max_length= 2000, null=False, blank=False)
    assignment = models.ForeignKey(Assignment, null=True, on_delete=models.CASCADE, \
                                   related_name="questions")
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    sub_topic = models.ForeignKey(SubTopic, on_delete=models.SET_NULL, null=True, blank=True)
    parent_question = models.ForeignKey('self', on_delete=models.CASCADE, null=True, \
                                        blank=True, related_name='sub_questions')
    answer_type = models.CharField(
        max_length = 30,
        choices = QuestionChoices.choices,
        default = QuestionChoices.STRUCTURAL_TEXT
    )
    embedding = models.JSONField(null=True, blank=True)  # Field to store encoded representation for search

    def default_due_date(self):
        if self.assignment:
            return self.assignment.due_date
        return None

    def save(self, *args, **kwargs):
        save_settings = kwargs.pop('save_settings', False)
        """"
        # TODO: Make the following work. It is supposed to check that the number saved is in the correct format
        for non-Question-Bank questions.
        number = kwargs.get('number', None)
        if kwargs.get('parent_question', None) == None:
            if not number.isdigit(): # we want number to be a digit because that's what is used for ordering
                raise ValueError(f'Expected the attribute "number" of a parent_question to be an integer, but got {self.number}')
        
        else: # if a sub_question
            if not number[:-1].isdigit() or not number[-1].isalpha():
                raise ValueError(f'Expected the format of "number" for a subquestion to be digits followed \
                                 by a letter, but got {self.number}')
            
        """

        super(Question, self).save(*args, **kwargs)
        if save_settings:
            if self.answer_type.startswith('MCQ') or self.answer_type.startswith('MATCHING'):
                settings, created = MCQQuestionSettings.objects.get_or_create(question=self)
            else:
                settings, created = StructuralQuestionSettings.objects.get_or_create(question=self)
            settings.due_date = self.default_due_date()
            settings.save()
            if not self.embedding:
                # Encode the question text, ensuring the sequence is within the max length limit
                max_length = 512  # BERT's maximum sequence length
                question_tokens = BERT_TOKENIZER.encode(self.text, add_special_tokens=True, max_length=max_length, truncation=True, padding='max_length')

                with torch.no_grad():
                    question_tensor = torch.tensor([question_tokens])
                    question_attention_mask = (question_tensor != 0).float()  # Create attention mask
                    question_encoded_output = BERT_MODEL(question_tensor, attention_mask=question_attention_mask)[0]

                # Apply attention-based pooling to question encoded output
                question_encoded_output_pooled = attention_pooling(question_encoded_output, question_attention_mask)

                # Save the encoded output to the question object
                self.embedding = question_encoded_output_pooled.tolist()

            super(Question, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not self.parent_question:
            self.sub_questions.all().delete()
        super(Question, self).delete(*args, **kwargs)

    def get_num_points(self):
        if self.answer_type.startswith('MCQ') or self.answer_type.startswith('MATCHING'):
            return self.mcq_settings.num_points
        else:
            return self.struct_settings.num_points
        
    def get_mcq_pk_ac_list(self): # ac == answer_code
        output = []
        # List of all answer types
        mcq_related_names = ['mcq_expression_answers', 'mcq_text_answers','mcq_float_answers',
                                'mcq_variable_float_answers','mcq_image_answers','mcq_latex_answers']
        for mrn in mcq_related_names:
            for mcq in getattr(self, mrn).all():
                output.append(mcq.get_pk_ac())
        return output
    
    def get_mcq_answers(self):
        output = []
        mcq_related_names = ['mcq_expression_answers', 'mcq_text_answers','mcq_float_answers',
                                'mcq_variable_float_answers','mcq_image_answers','mcq_latex_answers']
        for mrn in mcq_related_names:
            output.extend(getattr(self, mrn).all())
        return output        

    def __str__(self):
        return f"Question {self.number} for {self.assignment}"
    
class QuestionCategory(models.Model):
    """
    Information about the topic, subtopic, and unit of a question
    """
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='category')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    subtopic = models.ForeignKey(SubTopic, on_delete=models.SET_NULL, null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)
    
class BaseQuestionSettings(models.Model):
    """
    Base settings for a `Question`.
    Fields common to both Structural and MCQ questions will be defined here.
    """
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    num_points = models.IntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(15)])
    due_date = models.DateTimeField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    difficulty_level = models.CharField(
        max_length=10,
        choices=DifficultyChoices.choices,
        default=DifficultyChoices.MEDIUM,
    )

    class Meta:
        abstract = True  # This means we won't create a table just for this base model.

class StructuralQuestionSettings(BaseQuestionSettings):
    """
    Settings specific to Structural Questions
    """
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='struct_settings')
    max_num_attempts = models.IntegerField(default=5, validators=[MinValueValidator(1)])
    deduct_per_attempt = models.FloatField(default=0.05, blank=True, null=True)
    margin_error = models.FloatField(default=0.03, blank=False, null=False, validators=[MinValueValidator(0), MaxValueValidator(1)])
    percentage_pts_units = models.FloatField(default=0.03, blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(1)])
    units_num_attempts = models.IntegerField(default=2, validators=[MinValueValidator(1)])

class MCQQuestionSettings(BaseQuestionSettings):
    """
    Settings specific to MCQ Questions
    """
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='mcq_settings')
    mcq_max_num_attempts = models.IntegerField(default=4, validators=[MinValueValidator(1)])
    mcq_deduct_per_attempt = models.FloatField(default=0.25, blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(1)])

class GradingScheme(models.Model):
    """
    Grading scheme for assignments
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="grading_schemes", null=True)
    name = models.CharField(max_length=25, blank=False, null=False, default="Default")
    num_points = models.IntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(25)])
    mcq_num_attempts = models.IntegerField(default=4, validators=[MinValueValidator(1)])
    struct_num_attempts = models.IntegerField(default=5, validators=[MinValueValidator(1)])
    deduct_per_attempt = models.FloatField(default=0.05, blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(1)])
    mcq_deduct_per_attempt = models.FloatField(default=0.25, blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(1)])
    margin_error = models.FloatField(default=0.03, blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(1)])
    percentage_pts_units = models.FloatField(default=0.1, blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(1)])
    units_num_attempts = models.IntegerField(default=2, validators=[MinValueValidator(1)])
    late_sub_deduct = models.FloatField(default=0.25, validators=[MinValueValidator(0), MaxValueValidator(1)])
    floor_percentage = models.FloatField(default=0.35, validators=[MinValueValidator(0), MaxValueValidator(1)])

    def __str__(self):
        return f"Grading scheme {self.name}"
    
    def print_attributes(self):
        for attr_name, attr_value in vars(self).items():
            # The attributes starting with '_' are either private or Django internal attributes.
            # We can skip those to get only the fields we defined.
            if not attr_name.startswith('_'):
                print(f"{attr_name}: {attr_value}")



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
        return f"Hint {self.pk} for {self.question}"
    
class AnswerBase(models.Model):
    """
    Class for structural answers.
    """
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    content = models.TextField(blank=False, null=False)
    answer_unit = models.CharField(max_length=50, blank=True, null=True) # Optional field for the units of the answer
    preface = models.CharField(max_length=20, blank=True, null=True)
    sufface = models.CharField(max_length=20, blank=True, null=True) 
    class Meta:
        abstract = True

    def __str__(self):
        return f"Answer for {self.question}: {self.content}" 
    
    def get_pk_ac(self):
        """
        Returns 'pk_answercode', which is used for question editing and answer validation.
        """
        return f'{self.pk}_{self.get_answer_code()}'
    
class FloatAnswer(AnswerBase):
    """
    Answer to a `structural Question` may be an algebraic expression, a vector, or a float.
    """
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name="float_answer")
    content = models.FloatField(blank=False, null=False)

    def __str__(self):
            
        return f"Float Answer for {self.question}: {self.content}"
    def get_answer_code(self):
        return 1
    
class VariableFloatAnswer(AnswerBase):
    """
    Answer to a `structural Question` or `MCQ Question` may be a variable float. 
    E.g answer = F/m, where F and m are going to have multiple different values assigned
    to different users.
    """
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='variable_float_answer')
    content = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f"Variable Float answer for {self.question}: {self.content}"
        
    def get_answer_code(self):
        return 5   
         
class ExpressionAnswer(AnswerBase):
    """
    An expression for a `structural Question` may just be interpreted as text. The math.js library
    will parse the expression given by the teacher and the resulting text will be stored.
    When a user will input an answer, it will be compared to that text.
    """
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name="expression_answer")
    content = models.CharField(max_length=200) 
    
    def __str__(self):
        
        return f"Expression Answer for {self.question}: {self.content}"
    
    def get_answer_code(self):
        return 0
    
class LatexAnswer(AnswerBase):
    """
    An answer may a latex string that will later be rendered in the JavaScript.
    For now, this is only used for MCQ `Questions`.
    """
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='latex_answer')
    content = models.CharField(max_length=400)

    def __str__(self):

        return f"Latex Answer for {self.question}: {self.content}"
    
    def get_answer_code(self):
        return 2
    
class TextAnswer(AnswerBase):
    """
    Probably less common, but a `Question` may have a text answer.
    Will implement semantic validation for text answers using a transformer later.
    """
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='text_answer')
    content = models.CharField(max_length=1000)

    def __str__(self):
        return f"Text Answer for {self.question}: {self.content}"
    
    def get_answer_code(self):
        return 4

class MCQAnswerBase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField(blank=False, null=False)
    is_answer = models.BooleanField(default=False)
    class Meta:
        abstract = True

    def __str__(self):
        return f"MCQ Answer for {self.question}: {self.content}"
    
    def get_pk_ac(self):
        """
        Returns 'pk_answercode', which is used for question editing and answer validation.
        """
        return f'{self.pk}_{self.get_answer_code()}'

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
    
    def get_answer_code(self):
        return 1    
    
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

    def get_answer_code(self):
        return 8    
            
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

    def get_answer_code(self):
        return 0
    
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
    
    def get_answer_code(self):
        return 2
    
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
    
    def get_answer_code(self):
        return 3
    
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
    
    def get_answer_code(self):
        return 7
    
class MatchingAnswer(models.Model):
    """
    A question may be a matching pairs question
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='matching_pairs')
    part_a = models.CharField(max_length=3000, blank=False, null=False)
    part_b = models.CharField(max_length=3000, blank=False, null=False)
    
    def __str__(self):
        return f"Matching pair answer for {self.question}"
    
    def get_pk_ac(self):
        """
        Returns 'pk_answercode', which is used for question editing and answer validation.
        """
        return f'{self.pk}_{self.get_answer_code()}'
    
    def get_answer_code(self):
        return 9

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
    symbol = models.CharField(max_length=10, blank=False, null=False)
    instances_created = models.BooleanField(default=False)
    step_size = models.FloatField(blank=True, null=True, default=0.0)
    is_integer = models.BooleanField(default=False)

    def __str__(self):
        return f"Variable `{self.symbol}` for question {self.question}"
    def create_instances(self, num = 5, is_int=False):
        """
        Creates num number of random variable instances.
        """
        num = min(5, num) # making sure num is never greater than 5
        intervals = self.intervals.all()
        if intervals:
            for _ in range(min(num, self.get_num_possible_values())):
                bounds = random.choice(intervals)
                lower_bound = bounds.lower_bound
                upper_bound = bounds.upper_bound
                random_float = random.uniform(lower_bound, upper_bound)
                if self.step_size != 0 and self.step_size is not None:
                    step_count = (random_float - lower_bound) // self.step_size
                    random_float = lower_bound + step_count * self.step_size
                if self.is_integer:
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
    def get_num_possible_values(self):
        if self.step_size != 0 and self.step_size is not None:
            intervals_counts = []
            for interval in self.intervals.all():
                num_possible_values = (interval.upper_bound-interval.lower_bound)//self.step_size
                intervals_counts.append(int(num_possible_values))
            return sum(intervals_counts)
        else:
            return 1000 # Just a replacement for "infinity"
        
    
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
    
class EnrollmentCode(models.Model):

    course= models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollment_code")
    code = models.IntegerField(default=0000)
    creation_date = models.DateField(auto_now_add=True)
    expiring_date = models.DateField()
