from phobos.models import Topic, SubTopic, Subject

def run():
    # Define a dictionary with topics and their subtopics

    subjects = ['PHYSICS', 'MATHS', 'COMPUTER_SCIENCE']

    topics_subtopics_list = [{
        'Mechanics': [
            'Kinematics',
            'Newton\'s Laws of Motion',
            'Work, Energy, and Power',
            'Momentum and Collisions',
            'Circular and Rotational Motion',
            'Gravitation',
            'Statics of Rigid Bodies',
            'Dynamics of Rigid Bodies',
        ],
        'Thermodynamics': [
            'Thermal Properties of Matter',
            'Thermal Equilibrium and Temperature',
            'First Law of Thermodynamics',
            'Second Law of Thermodynamics',
            'Heat Transfer Methods',
            'Thermodynamic Processes',
            'Entropy and Carnot Cycle',
            'Heat Engines and Refrigerators',
        ],
        'Electricity and Magnetism': [
            'Electrostatics',
            'Electric Potential and Capacitance',
            'Current Electricity',
            'Magnetic Effects of Current',
            'Electromagnetic Induction and AC',
            'Electromagnetic Waves',
            'Maxwell\'s Equations',
        ],
        'Waves': [
            'Wave Basics and Types',
            'Wave Properties and Behavior',
            'Superposition and Standing Waves',
            'Sound Waves',
            'Doppler Effect',
            'Resonance',
        ],
        'Optics': [
            'Reflection and Refraction',
            'Lens, Mirrors, and Optical Instruments',
            'Wave Optics: Interference and Diffraction',
            'Polarization',
            'Dispersion and Spectra',
            'Optical Phenomena in Nature',
        ],
        'Modern Physics': [
            'Quantum Physics and Quantum Mechanics',
            'Dual Nature of Matter and Radiation',
            'Atomic and Nuclear Physics',
            'Special and General Relativity',
            'Particle Physics and Standard Model',
            'Cosmology and Universe',
        ],
        'Fluid Mechanics': [
            'Fluid Properties and Statics',
            'Fluid Dynamics and Bernoulli\'s Principle',
            'Viscosity and Laminar Flow',
            'Surface Tension and Capillarity',
            'Turbulence and Flow Patterns',
        ],
    },
        {
        'Algebra': [
            'Polynomials',
            'Linear Equations',
            'Quadratic Equations',
            'Matrices and Determinants',
            'Complex Numbers',
            'Binomial Theorem',
        ],
        'Calculus': [
            'Limits and Continuity',
            'Differential Calculus',
            'Integral Calculus',
            'Differential Equations',
            'Applications of Derivatives',
            'Applications of Integrals',
        ],
        'Geometry': [
            'Coordinate Geometry',
            'Lines and Angles',
            'Triangles',
            'Quadrilaterals and Polygons',
            'Circles',
            '3D Geometry',
        ],
        'Trigonometry': [
            'Trigonometric Identities',
            'Trigonometric Equations',
            'Inverse Trigonometry',
            'Height and Distances',
        ],
        'Statistics and Probability': [
            'Mean, Median, Mode',
            'Variance and Standard Deviation',
            'Permutations and Combinations',
            'Probability',
            'Probability Distributions',
        ],
        'Vectors': [
            'Vector Algebra',
            'Scalar Product',
            'Vector Product',
            'Linear Independence',
            'Applications in Geometry',
        ]
    },
        {
        'Programming Fundamentals': [
            'Syntax and Semantics',
            'Variables and Data Types',
            'Control Structures',
            'Loops',
            'Functions and Methods',
            'Object-Oriented Programming',
            'Recursion'
        ],
        'Data Structures': [
            'Arrays',
            'Linked Lists',
            'Stacks',
            'Queues',
            'Trees',
            'Graphs',
            'Hash Tables'
        ],
        'Algorithms': [
            'Sorting Algorithms',
            'Searching Algorithms',
            'Graph Algorithms',
            'Dynamic Programming',
            'Greedy Algorithms',
            'Divide and Conquer',
        ],
        'Operating Systems': [
            'Processes and Threads',
            'Memory Management',
            'File Systems',
            'Concurrency',
            'Scheduling',
            'I/O Management',
        ],
        'Database Systems': [
            'Relational Databases',
            'SQL',
            'Normalization',
            'Transactions and Concurrency Control',
            'NoSQL Databases',
            'Database Indexing and Optimization',
        ],
        'Computer Networks': [
            'OSI and TCP/IP Models',
            'Routing and Switching',
            'Network Protocols',
            'Wireless Networks',
            'Security and Cryptography',
        ],
        'Software Engineering': [
            'Software Development Life Cycle',
            'Software Testing',
            'Software Design Patterns',
            'Agile Development',
            'Version Control',
            'Continuous Integration and Continuous Deployment',
        ],
        'Web Development': [
            'HTML, CSS, JavaScript',
            'Front-end Frameworks',
            'Back-end Development',
            'Web Security',
            'APIs and Web Services',
            'Responsive Design',
        ],
        'Artificial Intelligence': [
            'Machine Learning',
            'Neural Networks',
            'Natural Language Processing',
            'Robotics',
            'Expert Systems',
            'Search Algorithms'
        ],
        'Cybersecurity': [
            'Network Security',
            'Cryptography',
            'Penetration Testing',
            'Malware Analysis',
            'Authentication and Authorization',
            'Security Policies and Procedures',
        ]
    }]
    for index, topics_subtopics in enumerate(topics_subtopics_list):
        subject, created = Subject.objects.get_or_create(name=subjects[index])
        # Create instances of subtopics using nested for loops and the dictionary values
        for topic_name, subtopics in topics_subtopics.items():
            # Check if the topic already exists in the database
            topic, created = Topic.objects.get_or_create(name=topic_name, subject=subject)
            
            # If the topic was just created, print a message
            if created:
                print(f"Created new topic: {topic_name}")
            
            for subtopic_name in subtopics:
                SubTopic.objects.create(topic=topic, name=subtopic_name)

    # Verify the creation of objects
    print(Topic.objects.all())
    print(SubTopic.objects.all())
