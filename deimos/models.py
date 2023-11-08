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
    due_date = models.DateTimeField(null=True, blank=True)

    def get_grade(self):
        """
        Computes and returns the grade of a student on an Assignment
        """
        num_points = 0
        total = 0
        for question in self.assignment.questions.all():
            total += question.get_num_points()
            try:
                question_student = QuestionStudent.objects.get(question=question, student=self.student)
                # Taking modified score in to account to compute grade
                question_score_modified, is_created= QuestionModifiedScore.objects.get_or_create(question_student = question_student)
                if not question_score_modified.is_modified:
                    num_points += question_student.get_num_points()
                else:
                    num_points +=  question_score_modified.score
                # End 
            except QuestionStudent.DoesNotExist:
                pass
                # num_points += 0
        if total != 0:
            self.grade = round((num_points/total) * 100, 2)
        else:
            self.grade = 0
        self.assignment.num_points = total
        return self.grade
    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = self.assignment.due_date
        super().save(*args, **kwargs)
        
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
    num_units_attempts = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    def create_instances(self):
        """
        Get variable instances from the variables associated to the question.
        """
        if not self.question.parent_question: # If parent question.
            self.var_instances.clear()
            for var in self.question.variables.all():
                self.var_instances.add(var.get_instance())
        else: # if not parent question.
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
            answer = self.question.variable_float_answer.content
            assert answer.startswith('@{') and answer.endswith('}@')
            answer = answer[2:-2]
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
        if not self.question.parent_question:# if parent question
            var_value_dict = {}
            for var_instance in self.var_instances.all():
                var_value_dict[var_instance.variable.symbol] = var_instance.value
            return var_value_dict
        else:
            parent_question_student = QuestionStudent.objects.get(student=self.student, question=self.question.parent_question)
            return parent_question_student.get_var_value_dict()
    


    def evaluate_var_expressions_in_text(self, text, add_html_style=False):
        """
        Takes a text and evaluates expressions expected to contain variables.
        It looks for text within {} and does the replacements. 
        """
        def replace_match(match):
            expression = match.group(1)  # Extract the expression within the curly braces
            try:
                value = round(eval(transform_expression(expression), var_value_dict), 3) # 3 decimal places.
                if str(value).endswith('.0'):
                    value = int(value)
            except:
                value = expression
            if add_html_style:
                return f"<span class=\"variable-value\">{value}</span>"
            else:
                return str(value)

        regex = re.compile(r'@{(.*?)}@')  # Use non-greedy matching to avoid unexpected results
        # For example, it could be "{expression1} some random text {expression2}" and greedy
        # match will not work since it will include the random text.

        var_value_dict = self.get_var_value_dict()
        replaced_text = regex.sub(replace_match, text)
        
        # Remove the remaining curly braces after replacements
        replaced_text = replaced_text.replace('~', '')
        
        return replaced_text

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
                answers.append(round(eval(transform_expression(answer), var_value_dict), 3))
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
    
class Note(models.Model):
    """
    For any particular question, the Student should have the option to 
    write text and/or upload pictures for their own personal use whenever 
    they are viewing the question in the future. 
    This may be helpful when they are preparing for exams.
    """
    question_student = models.OneToOneField(QuestionStudent, on_delete=models.CASCADE, related_name="note")
    title = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField()
    last_edited = models.DateField(auto_now=True)

class NoteImage(models.Model):
    """
    Stored in `Student`'s Note in case the student upload pictures for notes on a
    particular question.
    """
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='deimos/images/notes_images/', blank=True, null=True)
    
    def delete(self, *args, **kwargs):
        # Delete the image file from storage
        if self.image:
            self.image.delete(save=False)
        super(NoteImage, self).delete(*args, **kwargs)
class NoteTemporary(models.Model):
    """
    Used to store notes temporarily when user uses QR Code to change device.
    """
    title = models.CharField(max_length=200, blank=True, null=True)
    note = models.OneToOneField(Note, on_delete=models.CASCADE, related_name='temp_note')
    content = models.TextField()
    
    
class QuestionAttempt(models.Model):
    """
    Used to manage `Student` attempts on `Question`s
    """
    content = models.CharField(max_length=1000, blank=False, null=False)
    question_student = models.ForeignKey(QuestionStudent, on_delete=models.CASCADE, related_name='attempts')
    success = models.BooleanField(default=False, null=True)
    num_points = models.FloatField(default=0, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    units_success = models.BooleanField(default=False, null=True)
    submitted_units = models.CharField(max_length=10, null=True, blank=True)
    # MCQ answers don't need submitted_answer.
    # Structural questions attempts will be simplified and stored in content
    # while the actual submission will be stored in submitted_answer.
    submitted_answer =models.CharField(max_length=3000, blank=True, null=True)
    def __str__(self):
        return f"{self.question_student.student.username} attempt for {self.question_student.question}"

class QASuccessPairs(models.Model):
    """
    For matching pair questions, we store the pairs that were correct for an attempt
    """
    question_attempt = models.OneToOneField(QuestionAttempt, on_delete=models.CASCADE, related_name='success_pairs')
    pairs = models.CharField(max_length=2000, null=False, blank=False) # will store the pairs as long string
    # of primary keys of `MatchingAnswer  separated by '&'s
    

class QuestionModifiedScore(models.Model): 
    """
    Used to modify `Student` points on `Question`s
    """
    question_student = models.OneToOneField(QuestionStudent, on_delete=models.CASCADE, related_name='modify_question_score')
    is_modified = models.BooleanField(default=False)
    score = models.FloatField(default=0, null=True, blank=True) 

    def __str__(self):
        if self.score == None:
            self.is_modified = False
        return f"{self.question_student.student.username} score: {self.score} is modified? {self.is_modified}"


def transform_expression(expr):
    """Insert multiplication signs between combined characters, except within trig functions."""
    expression = remove_extra_spaces_around_operators(expr)
    expression = expression.replace(', ', '')
    expression = expression.replace(' ', '*')
    expression = re.sub(r'1e\+?(-?\d+)', r'10^\1', expression)
    trig_functions = {
        'asin': 'ò', 'acos': 'ë', 'atan': 'à', 'arcsin': 'ê', 'arccos': 'ä',
        'arctan': 'ï', 'sinh': 'ù', 'cosh': 'ô', 'tanh': 'ü', 'sin': 'î', 'cos': 'â', 'tan': 'ö', 'log': 'ÿ', 'ln': 'è',
        'cosec': 'é', 'sec': 'ç', 'cot': 'û', 'sqrt':'у́', 'pi': 'я',
    }

    expression = encode(expression, trig_functions)
    transformed_expression = ''.join(
        char if index == 0 or not needs_multiplication(expression, index, trig_functions)
        else '*' + char for index, char in enumerate(expression)
    )
    transformed_expression = transformed_expression.replace('^', '**')
    return decode(transformed_expression, trig_functions)

def remove_extra_spaces_around_operators(text):
    pattern = r'(\s*([-+*/^])\s*)'
    return re.sub(pattern, lambda match: match.group(2), text)

def needs_multiplication(expr, index, trig_functions):
    char = expr[index]
    prev_char = expr[index - 1]
    return (
        (char.isalpha() or char in trig_functions.values()) and prev_char.isalnum() or
        char.isdigit() and prev_char.isalpha() or
        char == "(" and (prev_char.isalpha() and not prev_char in trig_functions.values())
    )

def encode(text, trig_functions):
    """Takes a string and replaces trig functions with their corresponding special character."""
    result = text
    for key, value in trig_functions.items():
        result = result.replace(key, value)
    return result

def decode(text, trig_functions):
    """Takes a string and replaces special character with their corresponding trig function."""
    special_chars = {'e':'E', 'i':'((-1)^0.5)'}
    result = text
    # !Important.  special_chars for loop must come before 
    # the trig_functions for loop!
    for sc, value in special_chars.items():
        result = result.replace(sc, value)
    for key, value in trig_functions.items():
        result = result.replace(value, key)
    return result
