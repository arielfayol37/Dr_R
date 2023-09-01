# PHOBOS
Here are the two least straight forward phobos views.
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

Please note that these views should be further adapted to fulfill the specific requirements of your application. Additional logic and template elements may be necessary to align the views with your design and functionality preferences.
