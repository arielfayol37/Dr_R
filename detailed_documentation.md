# PHOBOS
Here are the two least straight forward phobos views.
## Table of contents
1. [Search Question View](#search_question-View)
2. [Create_Question_View](#create_question-View)
3. [Javascript Documentation for question creation (answer_input.js)](#JavaScript-Code-Documentation-for-Create-Question-in-PHOBOS)
4. [Javascript Documentation for calci (the high precision calculator)](#javascript-documentation-for-calci-the-embedded-high-precision-calculator)
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
