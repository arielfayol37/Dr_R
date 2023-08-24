from django.db import models
from phobos.models import Course, Question, User, Assignment, VariableInstance, QuestionChoices
from django.core.validators import MaxValueValidator, MinValueValidator
import re
class Student(User):
    """
    Student class to handle students in the platform.
    
    # TODO: Can add profile pictures if deemed fit. 
    # TODO: May add school name if platform scales.
    """
    courses = models.ManyToManyField(Course, through='Enrollment')
    assignments = models.ManyToManyField(Assignment, through='AssignmentStudent')
    questions = models.ManyToManyField(Question, through='QuestionStudent')

class Note(models.Model):
    """
    For any particular question, the Student should have the option to 
    write text and/orupload pictures for their own personal use whenever 
    they are viewing the question in the future. 
    This may be helpful when they are preparing for exams.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="notes")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()

class NoteImage(models.Model):
    """
    Stored in `Student`'s Note in case the student upload pictures for notes on a
    particular question.
    """
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='deimos/images/notes_images/', blank=True, null=True)
 

class Resource(models.Model):
    """
    Used to store resources suggested by Student.

    For example, if the Student has a web page that he/she deemed
    helpful for a particular question, he/she may submit it.

    This will be later validated by the Professor, and can be
    suggested to other students automatically.
    
    If there are many suggested Resources for the question, 
    an algorithm will take care of the order of recommendation, based
    on other students ratings of the Resource, and/or the student answering
    the question particular needs.
    """
    url = models.URLField(blank=False, null=False) # User must input URL
    description = models.TextField(blank = False) # User must provide description
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='resources')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False, null=True)

class BonusPoint(models.Model):
    """
    These are bonus points gained by the Student, upon approval of suggested
    resources. 

    These bonus points may be used in two ways:
        1) Direct increase in the Student's grade
        2) To give more attempts(with no deductions per attempt) to the Student
           for any question they would like.
           For example, there maybe a button at the top of the page to click,
           which will 'detect' the question the user is on, and give more attempts
           (page maybe reloaded with updated info-new attempts- or 
           that can be handled dynamically using fetch() in JS, while updating the display
           for a better experience)

    """
    points = models.IntegerField()
    resource = models.OneToOneField(Resource, on_delete=models.CASCADE, related_name='bonuses')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

class Enrollment(models.Model):
    """
    Used to handle a `Student`'s enrollment for a particular course.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.FloatField(validators=[MaxValueValidator(100)], default=0, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)

class AssignmentStudent(models.Model):
    """
    Used to manage `Assigment` - `Student` relationship.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='assignments_intermediate')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    grade = models.FloatField(validators=[MaxValueValidator(100)], default=0, null=True)

    def get_grade(self):
        """
        Computes and returns the grade of a student on an Assignment
        """
        num_points = 0
        total = 0
        for question in self.assignment.questions.all():
            total += question.num_points
            try:
                question_student = QuestionStudent.objects.get(\
                    question=question, student=self.student)
                num_points += question_student.get_num_points()  
            except QuestionStudent.DoesNotExist:
                num_points += 0
        self.grade = (num_points/total) * 100
        return self.grade
class QuestionStudent(models.Model):
    """
    Used to manage `Question` - `Student` relationship.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    num_points = models.FloatField(default=0)
    success = models.BooleanField(default=False)
    var_instances = models.ManyToManyField(VariableInstance, related_name='question_students')
    instances_created = models.BooleanField(default=False)
    def create_instances(self):
        """
        Get variable instances from the variables associated to the question.
        """
        if not self.question.parent_question:
            self.var_instances.clear()
            for var in self.question.variables.all():
                self.var_instances.add(var.get_instance())
        else:
            parent_question_student = QuestionStudent.objects.get(question=self.question.parent_question,\
                                                                   student=self.student)
            if not parent_question_student.instances_created:
                parent_question_student.create_instances()
        self.instances_created = True
    def compute_structural_answer(self):
        """
        Computes the answer to the question if it's a `Question` with `Variable` answers.
        """
        if not self.instances_created:
            self.create_instances()
        if self.question.answer_type == QuestionChoices.STRUCTURAL_VARIABLE_FLOAT:
            assert self.question.variable_float_answers.count() == 1
            answer = self.question.variable_float_answers.first().content
        # TODO: Add a clause here if the answer type is different
        # TODO: Add another clause here to make sure the answer evaluates to a float.
        # Possible reasons why it won't evaluate:
            # 1: missing multiplication signs. E.g ab instead of a*b. transform_expression() handles that
            # 2: a symbol/character(s) that is among the variables. Fix: make sure on the frontEnd that
            #    an answer never contains symbols that are not defined variables.
            return eval(transform_expression(answer), self.get_var_value_dict())
    def get_var_value_dict(self):
        """
        Returns a dictionary of variable symbols and the corresponding instance value for
        this particular `Question`-`Student`.
        """
        # Note: We could have created a permanent dictionary for this instead of computing
        # each time, but this is the best to do it in case the professor changes the value/intervals
        # of variables.

        # TODO: !important Alternatively, we could just update the permanent dictionary whenever the professor
        # makes changes to question.
        var_value_dict = {}
        for var_instance in self.var_instances:
            var_value_dict[var_instance.variable.symbol] = var_instance.value
        return var_value_dict
    
    def evaluate_var_expressions_in_text(self, text, add_html_style=False):
        """
        Takes a text and evaluates expressions expected to contain variables.
        It looks for text within {} and do the replacements. 
        """
        regex = re.compile(r'{(.*)}') # Expecting anything within those curly braces to be variable symbols
                                      # and real numbers.
        # TODO: Do this more efficiently.
        var_value_dict = self.get_var_value_dict()
        matches = regex.findall(text)
        if not add_html_style:
            for match in matches:
                text = text.replace(match, eval(transform_expression(match), var_value_dict))
        else:
            for match in matches:
                replacement = f"<em class=\"variable\">{eval(transform_expression(match), var_value_dict)}</em>"
                text  = text.replace(match, replacement)
        return text
    def compute_mcq_answers(self):
        """
        Computes the float anwers to an MCQ question if they were variables.
        """
        if self.question.answer_type.startswith('MCQ'):
            mcq_var_floats = self.question.mcq_variable_float_answers.all()
            answers = []
            var_value_dict = self.get_var_value_dict()
            for mcq_var_float in mcq_var_floats:
                answer = mcq_var_float.content
                answers.append(eval(transform_expression(answer), var_value_dict))
            return answers
        
    def get_num_points(self):
        """
        Calculates and returns the number of points a student gets from a question
        """
        total = 0
        for attempt in self.attempts.all():
            # The idea here is that at some point
            # the student may get points even if attempts
            # are not successful. Maybe due to a new functionality
            # or the teacher manually giving points for that attempt
            total += attempt.num_points
        self.num_points = total
        return total 
    
    def get_num_attempts(self):
        """
        Calculates and returns the number of attempts on a question by a user.
        """
        return self.attempts.count()
    def __str__(self):
        return f"Question-Student:{self.question} {self.student.username}"
    
    
class QuestionAttempt(models.Model):
    """
    Used to manage `Student` attempts on `Question`s
    """
    content = models.CharField(max_length=1000, blank=False, null=False)
    question_student = models.ForeignKey(QuestionStudent, on_delete=models.CASCADE, related_name='attempts')
    success = models.BooleanField(default=False, null=True)
    num_points = models.FloatField(default=0, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question_student.student.username} attempt for {self.question_student.question}"
    

def transform_expression(expr):
    """Insert multiplication signs between combined characters"""
    expression = expr.replace(' ','')
    strs = []
    for index, character in enumerate(expression):
        string = character
        if index > 0:
            if character.isalpha() and expression[index-1].isalnum():
                string = '*' + character
            elif character.isdigit() and expression[index-1].isalpha():
                string = '*' + character
        strs.append(string)
    transformed_expression = ''.join(strs)   
    return transformed_expression