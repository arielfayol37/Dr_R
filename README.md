# Dr_R
Web platform for Physics Assigments System.

This is the README file for the Dr_R web application built using Django. The application is designed to provide different functionalities for students (Deimos), instructors (Phobos), and general users (Astros).

## PreRequisites
You must have installed python3 on your machine.
As of now, the system only supports 3.11 versions. Beyond that,
`torch` which is used for the search engine, won't be able to install.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/arielfayol37/Dr_r
```

2. Change into the project directory:
```bash
cd Dr_r
```

3. Create virtual environment (optional):
```bash
python3 -m venv venv
```

4. Activate the virtual environment (skip if you skipped step 3)
  a. On macOS and Linux:
  ```bash
  source venv/bin/activate
  ```
  b. On Windows:
  ```bash
  venv\Scripts\activate
  ```

5. Install required packages:
```bash
pip install -r requirements.txt
```

6. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

7. Run the development server:
```bash
python manage.py runserver
```
Then copy and paste the url from the terminal to your browser.

### NOTE
- MAC users: I have not tested those instructions on MAC, so I recommend that you skip setting up a
virtual environment if the command does not work (skip step 3 and 4). 
- Window users: if the command at step 3 does not work for you, just skip it. Or use "python" instead of
  "python3."

### Testing
In case you want to test without having to create accounts, courses, etc, don't worry. A copy 
of the site is running at https://mars-valpo.com. You can use the following credentials:
- Instructor test account: email - arielfayol1@gmail.com, password - ernestodelaCruz23789
- Student test account: email - fayol.ateufackzeudom@valpo.edu, password - ernestodelaCruz23789

## Impressive Features
- Algebraic expressions symbolic comparisons
- Semantic search engine
- Ability to take Notes for any question and come back to the later
- Supports latex input for equations
- Randomized variables for both multiple choice and structural questions
- High precision calculator
- Supports images in question body and mcq input
- Coming soon: customized automated practice tests
### Deimos (Student Interface)

- Students can access various courses.
- View course details, including name, description, subject, number of students, and difficulty level.
- Enroll in courses.
- View assignments and questions.
- Submit answers to questions.
- Receive hints for questions.
- View their progress and grades.

### Phobos (Instructor Interface)

- Instructors can create and manage courses.
- Create assignments with different categories (quiz, homework, practice test).
- Add questions to assignments, with various answer types (float, variable float, expression, etc.).
- Set/extend due dates for assignments.
- Assign weights to questions for grading purposes.
- View student progress and grades.

### Astros (General Interface)

- General users can browse courses and their details.
- No login is required to access these features.
## Contributing

Contributions are welcome! If you'd like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Create a pull request to the main repository.

We appreciate your contributions and thank you for helping make this project better!

## Code Style

When contributing code, please adhere to the project's coding style and conventions. This ensures that the codebase remains consistent and easy to maintain.

## Bug Reports and Feature Requests

If you encounter a bug in the application or have a feature request, please [open an issue](https://github.com/arielfayol37/Dr_r/issues). We value your feedback and appreciate your input.

## Contact

If you have any questions or need assistance, feel free to reach out to the project maintainers (317-720-7186, arielfayol1@gmail.com) or open a discussion in the repository.

## License

This project is licensed under the Creative Commons Legal Code License. By contributing to this project, you agree to abide by the terms of this license. See the [LICENSE](LICENSE) file for details.

