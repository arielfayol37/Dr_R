# PHOBOS (Instructor app)

## Table of Contents
0. [Skip To Deimos(student app)](#Deimos-Student-App)
1. [Models](#models-python-code-documentation-for-phobos)
   1.1 [General](#general)
   1.2 [Difficulty and Subject Choices](#difficulty-and-subject-choices)
   1.3 [Course](#course)
   1.4 [Professor](#professor)
   1.5 [Topic and SubTopic](#topic-and-subtopic)
   1.6 [Assignment](#assignment)
   1.7 [Question](#question)
   1.8 [QuestionImage](#questionimage)
   1.9 [Hint](#hint)
   1.10 [FloatAnswer](#floatanswer)
   1.11 [VariableFloatAnswer](#variablefloatanswer)
   1.12 [ExpressionAnswer](#expressionanswer)
   1.13 [LatexAnswer](#latexanswer)
   1.14 [TextAnswer](#textanswer)
   1.15 [MCQFloatAnswer](#mcqfloatanswer)
   1.16 [MCQVariableFloatAnswer](#mcqvariablefloatanswer)
   1.17 [MCQExpressionAnswer](#mcqexpressionanswer)
   1.18 [MCQLatexAnswer](#mcqlatexanswer)
   1.19 [MCQTextAnswer](#mcqtextanswer)
   1.20 [MCQImageAnswer](#mcqimageanswer)
   1.21 [Variable](#variable)
   1.22 [VariableInstance](#variableinstance)
   1.23 [VariableInterval](#variableinterval)
   1.24 [VectorAnswer](#vectoranswer)

2. [Search Question View](#search-question-view)
3. [Create Question View](#create-question-view)
4. [JavaScript Documentation for Question Creation (answer_input.js)](#javascript-code-documentation-for-create-question-in-phobos)
5. [JavaScript Documentation for CALCI (the High Precision Calculator)](#javascript-documentation-for-calci-the-embedded-high-precision-calculator)


# `models` - Python Code Documentation for phobos

`models.py` is part of the Django application for the Phobos platform and contains Django models for various aspects of the platform, such as courses, assignments, questions, and more.

## Difficulty and Subject Choices

Phobos uses the following choices for difficulty and subject:

- Difficulty:
  - Easy
  - Medium
  - Difficult

- Subject:
  - Computer Science
  - Maths
  - Physics

## Course

The `Course` model represents a course on the Phobos platform, with attributes such as name, description, subject, number of students, difficulty level, professors, topics, timestamp, and an optional image.

## Professor

The `Professor` model represents professors on the platform and extends the built-in Django `User` model with a department field.

## Topic and SubTopic

The `Topic` model represents course topics, while the `SubTopic` model represents subtopics associated with topics.

## Assignment

The `Assignment` model represents assignments, including quizzes, homework, and practice tests, with attributes such as name, course, timestamp, due date, assigned date, difficulty level, and category.

## Question

The `Question` model represents questions, which can be standalone or part of an assignment. It includes attributes such as number, text, assignment, category, topic, sub-topic, number of points, parent question, timestamp, difficulty level, answer type, maximum number of attempts, answer, deduction per attempt, margin of error, and due date.

## QuestionImage

The `QuestionImage` model represents images associated with questions, allowing for additional context.

## Hint

The `Hint` model represents hints for questions, providing additional guidance for solving questions.

## FloatAnswer

The `FloatAnswer` model represents float-type answers for structural questions, such as algebraic expressions or numerical values.

## VariableFloatAnswer

The `VariableFloatAnswer` model represents variable float answers for structural questions, allowing variables with different values for different users.

## ExpressionAnswer

The `ExpressionAnswer` model represents expression answers for structural questions, which are compared to teacher-provided expressions.

## LatexAnswer

The `LatexAnswer` model represents Latex answers for multiple-choice questions (MCQs).

## TextAnswer

The `TextAnswer` model represents text answers for questions, which may include semantic validation using transformers.

## MCQFloatAnswer

The `MCQFloatAnswer` model represents float-type answers for MCQs, including correct and incorrect options.

## MCQVariableFloatAnswer

The `MCQVariableFloatAnswer` model represents variable float answers for MCQs, allowing different variable values for different users.

## MCQExpressionAnswer

The `MCQExpressionAnswer` model represents expression answers for MCQs, with both correct and incorrect options.

## MCQLatexAnswer

The `MCQLatexAnswer` model represents Latex answers for MCQs, with both correct and incorrect options.

## MCQTextAnswer

The `MCQTextAnswer` model represents text answers for MCQs, with both correct and incorrect options.

## MCQImageAnswer

The `MCQImageAnswer` model represents image answers for MCQs, including correct and incorrect options.

## Variable

The `Variable` model represents variables associated with questions, allowing different instances of variables to be assigned to different users.

## VariableInstance

The `VariableInstance` model represents instances of variables associated with questions.

## VariableInterval

The `VariableInterval` model represents intervals for variables, defining the range of values for variables.

## VectorAnswer

The `VectorAnswer` model (deprecated) represented vector-type answers for structural questions. It was stored as a float array.

This documentation provides an overview of the Django models used in the Phobos platform for course management, assignments, and questions. For detailed information on each model and its attributes, please refer to the code in `models.py`.


## `search_question` View

The `search_question` view is responsible for enabling users to search for questions that are similar based on a search input. This view utilizes BERT embeddings to compute the cosine similarity between the input text and the text of stored questions. It then presents the top similar questions to the user.

### Usage

Users initiate a POST request to the view, including the `search_question` parameter with the input text they wish to search for.

The view performs the following steps:
- Tokenizes and encodes the input text using a BERT tokenizer.
- Processes the encoded input text through a BERT model to obtain the hidden states of the input.
- Computes the cosine similarity between the encoded input text and the encoded text of each stored question using the `cosine_similarity` function.
- Sorts the questions based on their similarity scores and returns the top N (e.g., 5) most similar questions.

### Template

The associated template (`phobos/search_question.html`) displays the list of top similar questions along with the search input.

---

## `create_question` View

The `create_question` view is used to allow professors to create new questions and associate them with assignments. It supports various types of question answers, including Multiple Choice Questions (MCQs), expression answers, and text answers.

### Usage

Professors can access the `create_question` view either through a link or by submitting a form.

If accessed via a form submission, the view expects POST data containing different parameters such as question text, answer type, options, etc.

The view carries out the following actions:
- Creates a new `Question` object and associated answer objects based on the submitted data and answer type.
- Handles various MCQ answer types (expression, text, float, image, latex) and generates the corresponding answer objects.
- Manages image creation linked to the question using image labels and URLs.
- After question and answer creation, redirects the user to an appropriate page, such as the assignment management page.

### Template

The associated template (`phobos/create_question.html`) provides a form for entering question details, answer choices, and options for attaching images.

# JavaScript Code Documentation for Create Question in PHOBOS

The following explains the functionality and structure of the JavaScript for create question.
The general idea is that creating a question is very dynamic and as such we have to track 1) The type of the answer 2) variables 3) Images. Given that certain answers may be algebraic equations and MCQ answers may be entered in latex format, we make use of MathJs to simplify the expressions entered and convert them into readable format using MathJax.

For variables, each time one is created, hidden input fields associated with the variable which is going to processed
in the backend when the form is submitted.
For images, each time one is uploaded (not submitted), we render the uploaded images and create input fields with information depending on whether is an image for an mcq or just part of the question body.

## Event Listeners

### `DOMContentLoaded` Event Listener

- Listens for the DOM to be fully loaded before executing the code.
- Initializes various variables and sets up event listeners.

### `surveyBtn` Event Listener

- Listens for a click on the "Survey Question" button.
- Sets the mode to 's-answer' (survey answer), but the functionality is marked as not a high priority and to be implemented later.

### `imageUploadInput` Event Listener

- Listens for changes in the file input for image uploads.
- Reads and displays the uploaded image on the page.

### `mcqBtn` Event Listener

- Listens for a click on the "MCQ Question" button.
- Sets the mode to 'm-answer' (multiple-choice answer).
- Displays relevant input fields and options for creating MCQ questions.
- Updates the form's action attribute.

### `mcqOptionBtnsDiv` Event Listener

- Listens for clicks on different MCQ modes (expression, float, text, latex, image).
- Configures the input field and placeholders based on the selected mode.

### `addMcqOptionBtn` Event Listener

- Listens for a click on the "Add MCQ Option" button.
- Adds a new MCQ option to the list of inputed MCQ answers.
- Validates the input and handles errors.

### `inputedMcqAnswersDiv` Event Listener

- Listens for clicks on MCQ options.
- Allows changing the status of an MCQ option (true/false) and deleting options.

### `frBtn` Event Listener

- Listens for a click on the "Free Response" button.
- Sets the mode to 'fr-answer' (free response answer).
- Displays relevant input fields and options for creating free response questions.
- Updates the form's action attribute.

### `expressionBtn` Event Listener

- Listens for a click on the "Expression" button.
- Sets the mode to 'e-answer' (expression answer).
- Displays relevant input fields and options for creating expression-based questions.
- Updates the form's action attribute.

### `floatBtn` Event Listener

- Listens for a click on the "Float" button.
- Sets the mode to 'f-answer' (float answer).
- Displays relevant input fields and options for creating float-based questions.
- Updates the form's action attribute.

### `latexBtn` Event Listener

- Listens for a click on the "LaTeX" button.
- Sets the mode to 'l-answer' (LaTeX answer), although this functionality is not fully used.
- Displays relevant input fields and options for creating LaTeX-based questions.
- Updates the form's action attribute.

### `screen` Event Listener

- Listens for changes in the input field used for expression, float, and LaTeX questions.
- Uses MathJax to display the updated content as formatted mathematical expressions.

### `form` Event Listener

- Listens for the form submission event.
- Performs validation and processing based on the selected mode before allowing the form to submit.

## Utility Functions

### `create_inputed_mcq_div(input_field, answer_type)`

- Creates and returns an HTML div element for an inputed MCQ option.
- Accepts an input field and the answer type as arguments.
- Converts the input value based on the answer type (expression, float, text, LaTeX, image).
- Handles display and encoding of MCQ options.
- Used within the code to add MCQ options.

### `create_img_div(img_input_field, img_label)`

- Creates and returns an HTML div element for an uploaded image.
- Accepts an image input field and an image label as arguments.
- Handles display and encoding of uploaded images.
- Used within the code to add uploaded images.

### `rep(str, index, char)`

- Utility function to replace a character at a specific index in a string.
- Used within the code for string manipulation.

### `setCharAt(str, index, chr)`

- Utility function to set a character at a specific index in a string.
- Used within the code for string manipulation.

## Image Upload Handling (Main Question)

- Allows users to upload images for the main question.
- Provides options to add and delete uploaded images.
- Supports image labels and display previews.


# JAVASCRIPT DOCUMENTATION FOR CALCI (the embedded high precision calculator)


## Variables

- `screen`: Holds a reference to an HTML element with the ID `screen`, presumably an input field for mathematical expressions.
- `btn`: Stores references to all HTML elements with the class `btn`.
- `previousActiveElement`: Keeps track of the previously active element to handle focus.
- `trigMode`: Stores the current trigonometric mode ('deg' or 'rad'), with 'deg' as the default.
- `degModeBtn`: References the HTML element with the ID `deg-mode`.
- `radModeBtn`: References the HTML element with the ID `rad-mode`.
- `cursorPosition`: Tracks the cursor position within the `screen` input field.
- `invBtn`: References the HTML element with the ID `inv-mode`.
- `trigBtns`: Stores references to all HTML elements with the class `trig`.
- `specialBtns`: Stores references to all HTML elements with the class `special`.
- `replacementDict`: A dictionary that maps special characters (e.g., 'π' and '√') to their corresponding replacements (e.g., 'pi' and 'sqrt').
- `specialBtnsTextDict`: A dictionary that maps special button text (e.g., 'x y', '√', 'log', etc.) to their corresponding mathematical representations.

## Event Listeners

- The `DOMContentLoaded` event listener initializes various elements and sets up additional event listeners when the DOM is fully loaded.

- A loop iterates over each `btn` element (excluding those with the 'exempt' class) and sets up a click event listener. These buttons represent mathematical operations and functions. When clicked, the respective text is inserted into the `screen` input field, updating the cursor position accordingly.

- `degModeBtn` and `radModeBtn` event listeners handle the switch between degree and radian trigonometric modes. The active button is highlighted.

- The `screen` input field's focus event listener updates `previousActiveElement` when it receives focus.

- Special buttons (e.g., trigonometric and mathematical functions) have event listeners that insert their corresponding representations into the `screen` input field when clicked.

- `invBtn` toggles the inverse mode for trigonometric functions by prefixing 'a' to the button text or removing it.

## Functions

- `backspc()`: Removes the last character from the `screen` input field.

- `mathjsEval()`: Evaluates the mathematical expression entered in the `screen` input field using the Math.js library and updates the input field with the result.

- `replaceChars(str, charA, charB)`: Replaces all occurrences of `charA` with `charB` in the given string `str`.

- `processString(str)`: Processes the input string by replacing characters defined in the `replacementDict` dictionary with their corresponding replacements.

  # DEIMOS (Student app)
0.0 [Models](#Deimos-MODELS)
1.1 [Index View](#index-view)
1.2 [Course Management View](#course-management-view)
1.3 [Assignment Management View](#assignment-management-view)
1.4 [Course Enrollment View](#course-enrollment-view)
1.5 [Answer Question View](#answer-question-view)
1.6 [Validate Answer View (API Endpoint)](#validate-answer-view-api-endpoint)
1.7 [Authentication Views](#authentication-views)
2.0 [Helper Functions](#helper-functions)
2.1 [is_student_enrolled(student_id, course_id)](#is_student_enrolledstudent_id-course_id)
2.3 [extract_numbers(text)](#extract_numberstext)
2.4 [compare_expressions(expression1, expression2)](#compare_expressionsexpression1-expression2)
2.5 [compare_floats(f1, f2, margin_error=0.0)](#compare_floatsf1-f2-margin_error0.0)
2.6 [replace_links_with_html(text)](#replace_links_with_htmltext)
2.7 [replace_vars_with_values(text, variable_dict)](#replace_vars_with_valuestext-variable_dict)
2.8 [replace_image_labels_with_links(text, labels_url_pairs)](#replace_image_labels_with_linkstext-labels_url_pairs)

## `Deimos MODELS`
## Student Class

The `Student` class is used to represent students on the platform. It extends the `User` class.

### Attributes

- `courses`: A many-to-many relationship with `Course` through the `Enrollment` model.
- `assignments`: A many-to-many relationship with `Assignment` through the `AssignmentStudent` model.
- `questions`: A many-to-many relationship with `Question` through the `QuestionStudent` model.

### TODOs

- Profile pictures can be added if needed.
- School name may be added if the platform scales.

## Note Class

The `Note` class is used to allow students to write notes for questions.

### Attributes

- `student`: A foreign key to the `Student` model.
- `question`: A foreign key to the `Question` model.
- `content`: Text content of the note.

## NoteImage Class

The `NoteImage` class is used to store images in a student's notes for a particular question.

### Attributes

- `note`: A foreign key to the `Note` model.
- `image`: An image field for uploading images related to the note.

## Resource Class

The `Resource` class is used to store resources suggested by students.

### Attributes

- `url`: A URL field for the suggested resource.
- `description`: A text field for the description of the resource.
- `student`: A foreign key to the `Student` model.
- `question`: A foreign key to the `Question` model.
- `is_approved`: A boolean field indicating whether the resource is approved.

## BonusPoint Class

The `BonusPoint` class represents bonus points gained by students.

### Attributes

- `points`: An integer representing the number of bonus points.
- `resource`: A one-to-one relationship with the `Resource` model.
- `student`: A foreign key to the `Student` model.

## Enrollment Class

The `Enrollment` class is used to handle a student's enrollment in a particular course.

### Attributes

- `student`: A foreign key to the `Student` model.
- `course`: A foreign key to the `Course` model.
- `grade`: A float representing the student's grade in the course.
- `registration_date`: A date and time field indicating the date of enrollment.

## AssignmentStudent Class

The `AssignmentStudent` class manages the relationship between assignments and students.

### Attributes

- `student`: A foreign key to the `Student` model.
- `assignment`: A foreign key to the `Assignment` model.
- `grade`: A float representing the student's grade for the assignment.

### Methods

- `get_grade()`: Computes and returns the grade of a student on an assignment.

## QuestionStudent Class

The `QuestionStudent` class manages the relationship between questions and students.

### Attributes

- `student`: A foreign key to the `Student` model.
- `question`: A foreign key to the `Question` model.
- `num_points`: A float representing the number of points earned by the student.
- `success`: A boolean indicating if the question was successfully answered.
- `var_instances`: A many-to-many relationship with `VariableInstance`.
- `instances_created`: A boolean indicating if variable instances have been created.

### Methods

- `create_instances()`: Creates variable instances for the question.
- `compute_structural_answer()`: Computes the answer to the question if it has variable answers.
- `get_var_value_dict()`: Returns a dictionary of variable symbols and values.
- `evaluate_var_expressions_in_text(text, add_html_style)`: Evaluates expressions containing variables in text.
- `compute_mcq_answers()`: Computes the float answers to an MCQ question if they are variables.
- `get_num_points()`: Calculates and returns the number of points earned by a student.
- `get_num_attempts()`: Returns the number of attempts on a question by a student.

## QuestionAttempt Class

The `QuestionAttempt` class is used to manage student attempts on questions.

### Attributes

- `content`: Text content of the attempt.
- `question_student`: A foreign key to the `QuestionStudent` model.
- `success`: A boolean indicating if the attempt was successful.
- `num_points`: A float representing the number of points earned.
- `timestamp`: A date and time field indicating the timestamp of the attempt.

### Methods

- `__str__()`: Returns a string representation of the attempt.

## Utility Function: transform_expression(expr)

The `transform_expression` function is a utility function that inserts multiplication signs between combined characters in a mathematical expression.

## `Deimos Views`

## Index View

- **URL Route**: `/deimos/index`
- **Description**: Displays the main dashboard for students.
- **User Access**: Requires user authentication. Redirects to the login page if not authenticated.
- **Functionality**:
  - Retrieves courses associated with the authenticated student.
  - Displays a list of courses.
- **Template**: `deimos/index.html`

## Course Management View

- **URL Route**: `/deimos/course_management/<course_id>`
- **Description**: Manages a specific course, displaying assignments and related information.
- **User Access**: Requires user authentication. Redirects to the login page if not authenticated.
- **Functionality**:
  - Checks if the authenticated student is enrolled in the specified course.
  - Retrieves assignments associated with the course.
- **Template**: `deimos/course_management.html`

## Assignment Management View

- **URL Route**: `/deimos/assignment_management/<assignment_id>`
- **Description**: Manages a specific assignment, displaying questions and related information.
- **User Access**: Requires user authentication. Redirects to the login page if not authenticated.
- **Functionality**:
  - Validates if the authenticated student is assigned to the specified assignment.
  - Retrieves questions associated with the assignment.
- **Template**: `deimos/assignment_management.html`

## Course Enrollment View

- **URL Route**: `/deimos/course_enroll/<course_id>`
- **Description**: Allows students to enroll in a specific course.
- **User Access**: Requires user authentication. Redirects to the login page if not authenticated.
- **Functionality**:
  - Checks if the authenticated student is already enrolled in the course.
  - Creates a new enrollment instance if not enrolled.
- **Template**: N/A

## Answer Question View

- **URL Route**: `/deimos/answer_question/<question_id>`
- **Description**: Allows students to answer a specific question within an assignment.
- **User Access**: Requires user authentication. Redirects to the login page if not authenticated.
- **Functionality**:
  - Retrieves the question and associated answers.
  - Handles different types of questions, including MCQ and structural questions.
- **Template**: `deimos/answer_question.html`

## Validate Answer View (API Endpoint)

- **URL Route**: `/deimos/validate_answer/<question_id>`
- **Description**: Validates a student's answer to a specific question.
- **User Access**: Requires user authentication. Redirects to the login page if not authenticated.
- **Functionality**:
  - Validates submitted answers, considering question types and attempts.
  - Returns a JSON response indicating correctness.
- **Template**: N/A

## Authentication Views

### Login View

- **URL Route**: `/deimos/login`
- **Description**: Handles user authentication and login.
- **User Access**: Available for all users, including guests and authenticated users.
- **Functionality**:
  - Validates email and password.
  - Logs in the user if credentials are correct.
- **Template**: `astros/login.html`

### Logout View

- **URL Route**: `/deimos/logout`
- **Description**: Logs out the currently authenticated user.
- **User Access**: Available for authenticated users.
- **Functionality**:
  - Logs out the user and redirects to the homepage.
- **Template**: N/A

### Register View

- **URL Route**: `/deimos/register`
- **Description**: Handles user registration.
- **User Access**: Available for all users, including guests and authenticated users.
- **Functionality**:
  - Validates and registers new students.
  - Performs password confirmation.
- **Template**: `astros/register.html`

## Helper Functions

### `is_student_enrolled(student_id, course_id)`

- **Description**: Checks if a student is enrolled in a specific course.
- **Parameters**:
  - `student_id`: The ID of the student to check enrollment for.
  - `course_id`: The ID of the course to check enrollment in.
- **Returns**:
  - `is_enrolled`: Boolean value indicating enrollment status.

### `extract_numbers(text)`

- **Description**: Extracts numbers and subscripted characters from a string.
- **Parameters**:
  - `text`: The input text to extract numbers and characters from.
- **Returns**:
  - `matches`: A list of extracted numbers and characters.

### `compare_expressions(expression1, expression2)`

- **Description**: Compares two algebraic expressions for equivalence.
- **Parameters**:
  - `expression1`: The first algebraic expression.
  - `expression2`: The second algebraic expression.
- **Returns**:
  - `True`: If the expressions are algebraically equivalent.
  - `False`: Otherwise.

### `compare_floats(f1, f2, margin_error=0.0)`

- **Description**: Compares two floating-point numbers for equality with a specified margin of error.
- **Parameters**:
  - `f1`: The first floating-point number.
  - `f2`: The second floating-point number.
  - `margin_error`: Margin of error for the comparison (default is 0.0).
- **Returns**:
  - `True`: If the numbers are equal or close within the margin of error.
  - `False`: Otherwise.

### `replace_links_with_html(text)`

- **Description**: Finds links in text and replaces them with HTML `a` tags.
- **Parameters**:
  - `text`: The input text containing links.
- **Returns**:
  - `text`: The text with links replaced by HTML `a` tags.

### `replace_vars_with_values(text, variable_dict)`

- **Description**: Replaces variables in text with colored values.
- **Parameters**:
  - `text`: The input text containing variables.
  - `variable_dict`: A dictionary of variables and their values.
- **Returns**:
  - `text`: The text with variables replaced by colored values.

### `replace_image_labels_with_links(text, labels_url_pairs)`

- **Description**: Replaces labels in text with HTML links.
- **Parameters**:
  - `text`: The input text containing labels.
  - `labels_url_pairs`: A list of label-url pairs.
- **Returns**:
  - `text`: The text with labels replaced by HTML links.


